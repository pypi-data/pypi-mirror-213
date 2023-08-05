"""Tests regarding the torch shims."""
import importlib
import pickle
import sys
from types import ModuleType
from typing import Final, Generator, Optional
from unittest.mock import Mock

from pytest import LogCaptureFixture, MonkeyPatch, fixture
from pytest_mock import MockerFixture
import torch

from tests.utils.helper import backend_test, get_warning_logs, unit_test

TORCH_SHIM_MODULE_PATH: Final[str] = "bitfount.backends.pytorch._torch_shims"


@fixture
def fix_torch_version(monkeypatch: MonkeyPatch) -> None:
    """Patches the version that torch claims to be."""
    monkeypatch.setattr(torch, "__version__", "1.8.1")


@fixture
def _torch_shim_module(
    # Force ordering dependency between these fixtures so that the torch version
    # is fixed before this "import" happens
    fix_torch_version: None,
) -> Generator[ModuleType, None, None]:
    """Forces a (re)import of _torch_shims to guarantee correct load() call.

    Will replace the original _torch_shims (if it was already imported) at the end.
    """
    original__torch_shim: Optional[ModuleType] = None
    try:
        original__torch_shim = sys.modules.get(TORCH_SHIM_MODULE_PATH)
    except KeyError:
        pass

    try:
        if original__torch_shim:
            yield importlib.reload(original__torch_shim)
        else:
            import bitfount.backends.pytorch._torch_shims as _torch_shims

            yield _torch_shims
    finally:
        if original__torch_shim:
            sys.modules[TORCH_SHIM_MODULE_PATH] = original__torch_shim
        else:
            del sys.modules[TORCH_SHIM_MODULE_PATH]


@unit_test
@backend_test
def test_torch_load_1_8(
    _torch_shim_module: ModuleType,
    caplog: LogCaptureFixture,
    fix_torch_version: None,
    mocker: MockerFixture,
) -> None:
    """Tests that the <1.13 version of torch.load() is called correctly.

    Checks that `pickle_module` is set as expected and that `weights_only` is ignored
    and flagged.
    """
    # Mock out underlying torch.load() call
    mock_torch_load = mocker.patch.object(
        _torch_shim_module.torch, "load", autospec=True
    )

    mock_f = Mock()
    mock_map_location = Mock()
    _torch_shim_module.torch_load(
        f=mock_f,
        map_location=mock_map_location,
        pickle_module=None,
        weights_only=True,
        fake_other_args=1,
    )

    # Check underlying torch.load() call is made with the correctly set arguments
    mock_torch_load.assert_called_once_with(
        f=mock_f,
        map_location=mock_map_location,
        pickle_module=pickle,
        fake_other_args=1,
    )
    # Check that warning about `weights_only` is logged
    warning_logs = get_warning_logs(caplog)
    assert (
        "The weights_only kwarg is not supported in this version of torch; ignoring..."
        in warning_logs
    )
