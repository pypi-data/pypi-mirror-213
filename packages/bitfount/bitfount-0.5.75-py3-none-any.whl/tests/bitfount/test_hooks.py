"""Tests bitfount.hooks module."""
from __future__ import annotations

import inspect
import logging
from typing import Any, Type
from unittest.mock import Mock

import pytest
from pytest import LogCaptureFixture

from bitfount.federated.helper import TaskContext
from bitfount.federated.pod import Pod
from bitfount.federated.protocols.base import BaseModellerProtocol, _BaseProtocol
from bitfount.hooks import (
    _HOOK_DECORATED_ATTRIBUTE,
    HOOK_TYPE_TO_PROTOCOL_MAPPING,
    BaseAlgorithmHook,
    BaseHook,
    BasePodHook,
    BaseProtocolHook,
    HookType,
    _registry,
    get_hooks,
    registry,
)
from tests.utils.helper import unit_test


@unit_test
class TestHooks:
    """Tests bitfount.hooks module."""

    @pytest.fixture(autouse=True)
    def cleanup_registry(self) -> None:
        """Cleans up the registry."""
        _registry.clear()

    @pytest.fixture
    def custom_pod_hook(self) -> BasePodHook:
        """Returns a custom pod hook."""

        class MyPodHook(BasePodHook):
            """Custom pod hook."""

            def on_pod_startup_start(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
                """Dummy method implementation."""
                print("on_pod_startup_start")

        return MyPodHook()

    @pytest.fixture
    def custom_protocol_hook(self) -> BaseProtocolHook:
        """Returns a custom protocol hook."""

        class MyProtocolHook(BaseProtocolHook):
            """Custom protocol hook."""

            def on_init_start(
                self, protocol: _BaseProtocol, *args: Any, **kwargs: Any
            ) -> None:
                """Dummy method implementation."""
                print("on_init_start")

            def on_init_end(
                self, protocol: _BaseProtocol, *args: Any, **kwargs: Any
            ) -> None:
                """Dummy method implementation."""
                print("on_init_end")

            def on_run_start(
                self,
                protocol: _BaseProtocol,
                context: TaskContext,
                *args: Any,
                **kwargs: Any,
            ) -> None:
                """Dummy method implementation."""
                print("on_run_start")

            def on_run_end(
                self,
                protocol: _BaseProtocol,
                context: TaskContext,
                *args: Any,
                **kwargs: Any,
            ) -> None:
                """Dummy method implementation."""
                print("on_run_end")

        return MyProtocolHook()

    @pytest.fixture
    def dummy_protocol(self) -> Type[_BaseProtocol]:
        """Returns a dummy protocol."""

        class DummyProtocol(BaseModellerProtocol):
            """Dummy modeller side protocol."""

            def __init__(self, *, algorithm: Any, mailbox: Any, **kwargs: Any):
                super().__init__(algorithm=algorithm, mailbox=mailbox, **kwargs)

            async def run(self, **kwargs: Any) -> Any:
                """Runs Modeller side of the protocol."""
                return None

        return DummyProtocol

    def test_all_hook_types_have_a_protocol(self) -> None:
        """Tests that all hook types have a protocol."""
        for hook_type in HookType:
            assert hook_type in HOOK_TYPE_TO_PROTOCOL_MAPPING

    @pytest.mark.parametrize("base_hook", [BasePodHook, BaseAlgorithmHook])
    def test_base_hooks_implement_protocol_correctly(
        self, base_hook: Type[BaseHook]
    ) -> None:
        """Tests that base hooks implement the protocol correctly."""
        assert not inspect.isabstract(base_hook)
        assert issubclass(base_hook, BaseHook)
        base_hook_obj = base_hook()

        if base_hook == BasePodHook:
            assert base_hook_obj.type == HookType.POD
        elif base_hook == BaseAlgorithmHook:
            assert base_hook_obj.type == HookType.ALGORITHM
        assert isinstance(
            base_hook_obj, HOOK_TYPE_TO_PROTOCOL_MAPPING[base_hook_obj.type]
        )
        assert base_hook_obj.hook_name == base_hook_obj.__class__.__name__

    def test_base_pod_hook_methods_are_decorated(self) -> None:
        """Tests that base pod hook methods are decorated."""
        hook = BasePodHook()
        assert getattr(hook.on_pod_shutdown_end, _HOOK_DECORATED_ATTRIBUTE)
        assert getattr(hook.on_pod_shutdown_start, _HOOK_DECORATED_ATTRIBUTE)
        assert getattr(hook.on_pod_startup_end, _HOOK_DECORATED_ATTRIBUTE)
        assert getattr(hook.on_pod_startup_error, _HOOK_DECORATED_ATTRIBUTE)
        assert getattr(hook.on_pod_startup_start, _HOOK_DECORATED_ATTRIBUTE)
        assert getattr(hook.on_pod_init_end, _HOOK_DECORATED_ATTRIBUTE)
        assert getattr(hook.on_pod_init_error, _HOOK_DECORATED_ATTRIBUTE)
        assert getattr(hook.on_pod_init_start, _HOOK_DECORATED_ATTRIBUTE)
        assert getattr(hook.on_task_end, _HOOK_DECORATED_ATTRIBUTE)
        assert getattr(hook.on_task_start, _HOOK_DECORATED_ATTRIBUTE)

    def test_base_algorithm_hook_methods_are_decorated(self) -> None:
        """Tests that base algorithm hook methods are decorated."""
        hook = BaseAlgorithmHook()
        assert getattr(hook.on_init_end, _HOOK_DECORATED_ATTRIBUTE)
        assert getattr(hook.on_init_start, _HOOK_DECORATED_ATTRIBUTE)
        assert getattr(hook.on_run_start, _HOOK_DECORATED_ATTRIBUTE)
        assert getattr(hook.on_run_end, _HOOK_DECORATED_ATTRIBUTE)

    def test_base_protocol_hook_methods_are_decorated(self) -> None:
        """Tests that base protocol hook methods are decorated."""
        hook = BaseProtocolHook()
        assert getattr(hook.on_init_end, _HOOK_DECORATED_ATTRIBUTE)
        assert getattr(hook.on_init_start, _HOOK_DECORATED_ATTRIBUTE)
        assert getattr(hook.on_run_start, _HOOK_DECORATED_ATTRIBUTE)
        assert getattr(hook.on_run_end, _HOOK_DECORATED_ATTRIBUTE)

    @pytest.mark.parametrize("base_hook", [BasePodHook, BaseAlgorithmHook])
    def test_hook_registration(self, base_hook: Type[BaseHook]) -> None:
        """Tests that hooks are registered correctly."""
        hook = base_hook()
        hook.register()
        assert hook.registered
        assert len(registry[hook.type]) == 1
        assert hook.hook_name in [i.hook_name for i in registry[hook.type]]

    @pytest.mark.parametrize("base_hook", [BasePodHook, BaseAlgorithmHook])
    def test_same_hook_cant_be_registered_multiple_times(
        self, base_hook: Type[BaseHook], caplog: LogCaptureFixture
    ) -> None:
        """Tests that the same hook can't be registered multiple times."""
        hook = base_hook()
        hook.register()
        hook.register()
        assert len(registry[hook.type]) == 1
        assert "hook already registered" in caplog.text

    def test_hook_type_can_have_multiple_hooks_registered_against_it(
        self, custom_pod_hook: BasePodHook
    ) -> None:
        """Tests that a hook type can have multiple hooks registered against it.

        The hook names have to be different.
        """
        pod_hook = BasePodHook()
        pod_hook.register()
        assert pod_hook.registered
        custom_pod_hook.register()
        assert custom_pod_hook.registered
        assert len(registry[HookType.POD]) == 2

    def test_hook_exception_is_automatically_caught_and_logged(
        self, caplog: LogCaptureFixture
    ) -> None:
        """Tests that hook exceptions are automatically caught and logged."""

        class MyHook(BasePodHook):
            """Custom hook."""

            def on_pod_startup_start(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
                """Dummy method implementation."""
                raise ValueError("Test")

        hook = MyHook()
        hook.on_pod_startup_start(Mock())
        assert "Exception in hook on_pod_startup_start" in caplog.text

    def test_hook_runs_successfully_and_is_logged(
        self, caplog: LogCaptureFixture
    ) -> None:
        """Tests that hook runs successfully and is logged."""
        caplog.set_level(logging.DEBUG)

        class MyHook(BasePodHook):
            """Custom hook."""

            def on_pod_startup_start(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
                """Dummy method implementation."""
                print("on_pod_startup_start")

        hook = MyHook()
        hook.on_pod_startup_start(Mock())
        assert "Calling hook on_pod_startup_start" in caplog.text
        assert "Called hook on_pod_startup_start" in caplog.text

    async def test_protocol_init_hooks_called_as_expected(
        self,
        caplog: LogCaptureFixture,
        custom_protocol_hook: BaseProtocolHook,
        dummy_protocol: Type[BaseModellerProtocol],
    ) -> None:
        """Tests that protocol hooks are called as expected."""
        caplog.set_level(logging.DEBUG)

        # Register the custom hook.
        custom_protocol_hook.register()

        # Calling the init method of the protocol should call the
        # on_init_start and on_init_end hooks.
        proto = dummy_protocol(algorithm=Mock(), mailbox=Mock())
        assert "Calling hook on_init_start" in caplog.text
        assert "Called hook on_init_start" in caplog.text
        assert "Calling hook on_init_end" in caplog.text
        assert "Called hook on_init_end" in caplog.text

        # Awaiting on the run method of the protocol which should call the
        # on_run_start and on_run_end hooks.
        await proto.run()
        assert "Calling hook on_run_start" in caplog.text
        assert "Called hook on_run_start" in caplog.text
        assert "Calling hook on_run_end" in caplog.text
        assert "Called hook on_run_end" in caplog.text

    def test_get_hooks_with_unknown_hook_type(self) -> None:
        """Tests that a ValueError is raised when an unknown hook type is passed."""
        with pytest.raises(ValueError):
            get_hooks("unknown_hook_type")  # type: ignore[call-overload] # Reason: Purpose of test. # noqa: B950
