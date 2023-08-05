"""Tests for PyTorch-specific utils."""
import contextlib
from importlib import reload
from io import BytesIO
import logging
import re
from typing import Callable, ContextManager, Generator
from unittest.mock import Mock, call, create_autospec

import pytest
from pytest import LogCaptureFixture, MonkeyPatch, fixture
from pytest_mock import MockerFixture
import torch.cuda

import bitfount.backends.pytorch.utils
from bitfount.backends.pytorch.utils import autodetect_gpu, enhanced_torch_load
import bitfount.config
from bitfount.data.datafactory import _get_default_data_factory
from tests.utils import PytestRequest
from tests.utils.helper import backend_test, get_debug_logs, get_warning_logs, unit_test


def mock_device_count(count: int = 0) -> Callable[[], int]:
    """Mock device counter for CUDA."""

    def f() -> int:
        return count

    return f


@backend_test
@unit_test
class TestAutodetectGPU:
    """Tests for `_autodetect_gpu` function."""

    @fixture(autouse=True)
    def clear_cache(self) -> Generator:
        """Clears the cache before each test."""
        reload(bitfount.backends.pytorch.utils)
        autodetect_gpu.cache_clear()
        yield
        autodetect_gpu.cache_clear()

    def test_autodetect_gpu_cpu_only(
        self, caplog: LogCaptureFixture, monkeypatch: MonkeyPatch
    ) -> None:
        """Tests auto-detecting GPU count when only CPU."""
        # Mock out CUDA device count
        caplog.set_level("INFO")
        monkeypatch.setattr("torch.cuda.device_count", mock_device_count(0))

        gpu_info = autodetect_gpu()

        assert gpu_info == {"accelerator": "cpu", "devices": None}
        assert (
            caplog.records[0].msg == "No supported GPU detected. Running model on CPU."
        )

    def test_autodetect_1_gpu(
        self, caplog: LogCaptureFixture, monkeypatch: MonkeyPatch
    ) -> None:
        """Tests auto-detecting GPU when only one GPU."""
        # Mock out CUDA device count
        caplog.set_level("INFO")
        monkeypatch.setattr("torch.cuda.device_count", mock_device_count(1))
        monkeypatch.setattr("torch.cuda.get_device_name", lambda x: f"GPU_{x}")

        gpu_info = autodetect_gpu()

        assert gpu_info == {"accelerator": "gpu", "devices": 1}
        assert (
            caplog.records[0].msg == "CUDA support detected. GPU (GPU_0) will be used."
        )

    def test_autodetect_multiple_gpu(
        self, caplog: LogCaptureFixture, monkeypatch: MonkeyPatch
    ) -> None:
        """Tests auto-detecting GPU when multiple GPUs."""
        # Mock out CUDA device count
        caplog.set_level("INFO")
        monkeypatch.setattr("torch.cuda.device_count", mock_device_count(2))
        monkeypatch.setattr("torch.cuda.get_device_name", lambda x: f"GPU_{x}")

        gpu_info = autodetect_gpu()

        assert gpu_info == {"accelerator": "gpu", "devices": 1}
        assert caplog.records[0].levelname == "WARNING"
        assert (
            caplog.records[0].msg
            == "Bitfount model currently only supports one GPU. Will use GPU 0 (GPU_0)."
        )
        assert (
            caplog.records[1].msg == "CUDA support detected. GPU (GPU_0) will be used."
        )

    def test_mps_detected_and_used(
        self, caplog: LogCaptureFixture, mocker: MockerFixture, monkeypatch: MonkeyPatch
    ) -> None:
        """Tests that MPS is detected and used."""
        caplog.set_level("INFO")
        monkeypatch.setattr("bitfount.config.BITFOUNT_USE_MPS", True)
        reload(bitfount.backends.pytorch.utils)
        mock_torch = mocker.patch("bitfount.backends.pytorch.utils.torch")
        mocker.patch(
            "bitfount.backends.pytorch.utils.platform.processor", return_value="arm64"
        )
        mock_torch.backends.mps.is_available.return_value = True

        gpu_info = autodetect_gpu()

        assert gpu_info == {"accelerator": "mps", "devices": 1}
        assert caplog.records[0].levelname == "INFO"
        assert (
            caplog.records[0].msg
            == "Metal support detected. Running model on Apple GPU."
        )

    def test_mps_detected_but_not_used(
        self, caplog: LogCaptureFixture, mocker: MockerFixture, monkeypatch: MonkeyPatch
    ) -> None:
        """Tests that MPS is detected but not used."""
        caplog.set_level("INFO")
        monkeypatch.setattr("bitfount.config.BITFOUNT_USE_MPS", False)
        reload(bitfount.backends.pytorch.utils)
        mock_torch = mocker.patch("bitfount.backends.pytorch.utils.torch")
        mocker.patch(
            "bitfount.backends.pytorch.utils.platform.processor", return_value="arm64"
        )
        mock_torch.backends.mps.is_available.return_value = True
        mock_torch.cuda.device_count.return_value = 0

        gpu_info = autodetect_gpu()

        assert gpu_info == {"accelerator": "cpu", "devices": None}
        assert caplog.records[0].levelname == "INFO"
        assert (
            caplog.records[0].msg
            == "Metal support detected, but has been switched off."
        )

    @pytest.mark.parametrize(
        argnames="mps_pytorch_support",
        argvalues=(True, False),
    )
    def test_mps_not_supported(
        self,
        caplog: LogCaptureFixture,
        mocker: MockerFixture,
        mps_pytorch_support: bool,
    ) -> None:
        """Tests handling if MPS is not supported.

        Tests the cases where:
        - it is supported by pytorch but not available
        - it is not supported by pytorch
        """
        mock_torch = mocker.patch("bitfount.backends.pytorch.utils.torch")
        # Mock out there being no explicit GPUs
        mock_torch.cuda.device_count.return_value = 0
        if mps_pytorch_support:
            # Mark the support as not available even if the pytorch version supports
            # it, i.e. as though running on Intel metal
            mock_torch.backends.mps.is_available.return_value = False
        else:
            # This will force an AttributeError to be raised on `.mps` access
            # i.e. as though pytorch version doesn't support MPS at all
            del mock_torch.backends.mps

        caplog.set_level("DEBUG")
        gpu_info = autodetect_gpu()

        assert gpu_info == {"accelerator": "cpu", "devices": None}

        if not mps_pytorch_support:
            assert "Pytorch version does not support MPS." in get_debug_logs(caplog)

    def test_autodetect_caching_with_mps(
        self, mocker: MockerFixture, monkeypatch: MonkeyPatch
    ) -> None:
        """Tests that autodetect caching works with MPS."""
        monkeypatch.setattr("bitfount.config.BITFOUNT_USE_MPS", True)
        reload(bitfount.backends.pytorch.utils)
        mock_torch = mocker.patch("bitfount.backends.pytorch.utils.torch")
        mocker.patch(
            "bitfount.backends.pytorch.utils.platform.processor", return_value="arm64"
        )
        mock_torch.backends.mps.is_available.return_value = True

        gpu_info = autodetect_gpu()
        assert gpu_info == {"accelerator": "mps", "devices": 1}
        mock_torch.backends.mps.is_available.assert_called_once()
        gpu_info2 = autodetect_gpu()
        assert gpu_info2 == {"accelerator": "mps", "devices": 1}
        # Ensure that the MPS check is still only called once even though the function
        # is called twice
        mock_torch.backends.mps.is_available.assert_called_once()


@backend_test
@unit_test
class TestDefaultDataFactoryLoading:
    """Tests for loading the default data factory when PyTorch installed."""

    def test_load_pytorch_default_data_factory(self, monkeypatch: MonkeyPatch) -> None:
        """Test that the default data factory can load."""
        # Ensure PyTorch is set as the engine variable
        monkeypatch.setattr(
            "bitfount.config.BITFOUNT_ENGINE", bitfount.config._PYTORCH_ENGINE
        )

        # Create a fake class and set that as the PyTorch data factory
        class FakeDataFactory:
            pass

        monkeypatch.setattr(
            "bitfount.backends.pytorch.data.datafactory._PyTorchDataFactory",
            FakeDataFactory,
        )

        df = _get_default_data_factory()
        assert isinstance(df, FakeDataFactory)


@backend_test
@unit_test
class TestEnhancedTorchLoadFunction:
    """Tests for enhanced_torch_load()."""

    @fixture
    def set_default_torch_device(self, monkeypatch: MonkeyPatch) -> str:
        """Sets the default torch device as though set via envvar."""
        default_device = "a_device"
        monkeypatch.setattr(
            bitfount.backends.pytorch.utils,
            "BITFOUNT_DEFAULT_TORCH_DEVICE",
            default_device,
        )
        return default_device

    @fixture(params=(str, BytesIO), ids=[f"file_type={i}" for i in ("str", "BytesIO")])
    def mock_model_file(self, request: PytestRequest) -> Mock:
        """The "model file" that is being loaded.

        Will either be mocked as though it were a str-based file path or a BytesIO
        stream of a loaded file.
        """
        mock_model_file: Mock = create_autospec(request.param)
        return mock_model_file

    @fixture
    def patch_shimmed_torch_load_call(self, mocker: MockerFixture) -> Mock:
        """Patch the torch_load call within the utils module."""
        mock_torch_load: Mock = mocker.patch.object(
            bitfount.backends.pytorch.utils, "torch_load", autospec=True
        )
        return mock_torch_load

    def test_default_torch_device_is_set(
        self,
        caplog: LogCaptureFixture,
        mock_model_file: Mock,
        patch_shimmed_torch_load_call: Mock,
        set_default_torch_device: str,
    ) -> None:
        """Test that default device is set if requested.

        If the default device config option is set, and enhanced_torch_load() is
        called without a map_location, the default device should be used instead.
        """
        caplog.set_level(logging.DEBUG)

        enhanced_torch_load(mock_model_file, map_location=None)

        # Check change is logged
        assert (
            f'Setting torch.load() device to "{set_default_torch_device}"'
            in caplog.text
        )
        # Check underlying call made with new device
        patch_shimmed_torch_load_call.assert_called_once_with(
            f=mock_model_file,
            map_location=set_default_torch_device,
            pickle_module=None,
            weights_only=False,
        )

    @pytest.mark.parametrize("has_cuda", [True, False], ids=lambda x: f"has_cuda={x}")
    @pytest.mark.parametrize("has_mps", [True, False], ids=lambda x: f"has_mps={x}")
    @pytest.mark.parametrize(
        "cpu_load_failure", [True, False], ids=lambda x: f"cpu_load_failure={x}"
    )
    def test_tries_different_device_if_first_failure(
        self,
        caplog: LogCaptureFixture,
        cpu_load_failure: bool,
        has_cuda: bool,
        has_mps: bool,
        mock_model_file: Mock,
        mocker: MockerFixture,
        patch_shimmed_torch_load_call: Mock,
    ) -> None:
        """Tests the device retry capability of enhanced_torch_load().

        If unable to load the model file on the supplied device/map location,
        enhanced_torch_load() should determine which other device types are available
        and try to load the model on those instead, defaulting to CPU as the last
        port of call.
        """
        caplog.set_level(logging.DEBUG)

        # This device is always available
        potential_devices = ["cpu"]

        # Set the expected devices that are available and mark that they should
        # all fail to load the model (except maybe cpu)
        map_location = "a_map_location"
        failures = [map_location]
        # Patch MPS check
        mocker.patch.object(
            bitfount.backends.pytorch.utils,
            "has_mps",
            return_value=has_mps,
            autospec=True,
        )
        if has_mps is True:
            failures.append("mps")
            potential_devices.append("mps")
        # Patch CUDA check
        mocker.patch.object(
            torch.cuda, "is_available", return_value=has_cuda, autospec=True
        )
        if has_cuda is True:
            failures.append("cuda")
            potential_devices.append("cuda")

        # Devices will be tried in order of map_location->CUDA->mps->cpu so make
        # sure lists are arranged correctly
        failures = [failures[0]] + list(reversed(failures[1:]))
        potential_devices.reverse()  # map_location isn't in this list so just reverse

        # Set torch_load call to fail on multiple devices then, potentially, succeed
        # on CPU
        side_effect = [RuntimeError(f"LOAD_MODEL_ERROR_{i}") for i in failures]
        loaded_model_return = Mock()
        if not cpu_load_failure:
            side_effect.append(loaded_model_return)
        else:
            side_effect.append(RuntimeError("LOAD_MODEL_ERROR_cpu"))
        patch_shimmed_torch_load_call.side_effect = side_effect

        # Create context manager depending on if we expect overall success
        test_context_manager: ContextManager
        if cpu_load_failure:
            test_context_manager = pytest.raises(
                RuntimeError,
                match=re.escape(
                    f"Unable to load model as requested,"
                    f" or on any of these alternative devices:"
                    f" {', '.join(potential_devices)}"
                ),
            )
        else:
            test_context_manager = contextlib.nullcontext()

        # Call enhanced_torch_load()
        with test_context_manager:
            model = enhanced_torch_load(mock_model_file, map_location=map_location)
            assert model is loaded_model_return

        # Test follow-up calls were made correctly AND _only_ those calls were made
        torch_load_calls = [
            call(
                f=mock_model_file,
                map_location=device,
                pickle_module=None,
                weights_only=False,
            )
            for device in [map_location] + potential_devices
        ]
        patch_shimmed_torch_load_call.assert_has_calls(
            torch_load_calls, any_order=False
        )
        assert patch_shimmed_torch_load_call.call_count == len(torch_load_calls)

        # Test expected warning log entries exist for failures and/or successes
        warning_logs = get_warning_logs(caplog)
        assert (
            f"Error whilst trying to load model with map_location={map_location}:"
            f' "LOAD_MODEL_ERROR_{map_location}"' in warning_logs
        )
        if has_mps:
            assert (
                'Error loading model on mps device: "LOAD_MODEL_ERROR_mps"'
                in warning_logs
            )
        if has_cuda:
            assert (
                'Error loading model on cuda device: "LOAD_MODEL_ERROR_cuda"'
                in warning_logs
            )
        if not cpu_load_failure:
            assert "Successfully loaded model on cpu device" in warning_logs
        else:
            assert (
                'Error loading model on cpu device: "LOAD_MODEL_ERROR_cpu"'
                in warning_logs
            )

        # If dealing with a stream-based model file, ensure it was reset the correct
        # number of times and that this was logged
        if isinstance(mock_model_file, BytesIO):
            assert mock_model_file.seek.mock_calls == [call(0)] * len(failures)
            debug_logs = get_debug_logs(caplog)
            assert (
                "Reset model stream to position 0 to retry torch.load()" in debug_logs
            )
