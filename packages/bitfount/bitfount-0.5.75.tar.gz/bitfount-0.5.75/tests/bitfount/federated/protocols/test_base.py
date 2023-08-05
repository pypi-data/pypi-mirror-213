"""Tests base protocols module."""
from abc import ABC
import importlib
import inspect
import pkgutil
from unittest.mock import Mock, create_autospec

import pytest
from pytest import fixture

from bitfount.federated.aggregators.aggregator import Aggregator
import bitfount.federated.algorithms.model_algorithms
from bitfount.federated.algorithms.model_algorithms.base import (
    _BaseModelAlgorithmFactory,
)
from bitfount.federated.protocols.base import _BaseProtocol
from bitfount.federated.protocols.model_protocols.federated_averaging import (
    FederatedAveraging,
)
from bitfount.federated.protocols.results_only import ResultsOnly
from bitfount.hooks import _HOOK_DECORATED_ATTRIBUTE
from tests.utils.helper import unit_test


@unit_test
class TestBase:
    """Test protocol base module."""

    @fixture
    def mock_aggregator(self) -> Mock:
        """Returns mock aggregator."""
        mock_aggregator: Mock = create_autospec(Aggregator, instance=True)
        return mock_aggregator

    def test_base_protocol_methods_are_not_decorated(self) -> None:
        """Tests that base protocol methods are not decorated.

        They should not be decorated because the base protocol is abstract. We can only
        test this with the constructor because the base protocol has no `run` method.
        """
        base = _BaseProtocol(algorithm=Mock(), mailbox=Mock())
        with pytest.raises(AttributeError):
            getattr(base.__init__, _HOOK_DECORATED_ATTRIBUTE)  # type: ignore[misc] # Reason: This is a test. # noqa: B950

    def test_protocol_initialises_pretrained_file_on_modeller_side(
        self, mock_aggregator: Mock, mock_modeller_mailbox: Mock
    ) -> None:
        """Test all protocols initialise pretrained file on modeller side."""
        pretrained_file_path = "mock/path"

        model_alg_modules = pkgutil.walk_packages(
            path=bitfount.federated.algorithms.model_algorithms.__path__,
            prefix=bitfount.federated.algorithms.model_algorithms.__name__ + ".",
        )

        for module_info in model_alg_modules:
            for _, cls in inspect.getmembers(
                importlib.import_module(module_info.name), inspect.isclass
            ):
                if (
                    issubclass(cls, _BaseModelAlgorithmFactory)
                    and ABC not in cls.__bases__
                ):
                    federated_algorithm = cls(
                        model=Mock(), pretrained_file=pretrained_file_path
                    )

                    for protocol_cls in [ResultsOnly, FederatedAveraging]:
                        protocol_factory = protocol_cls(
                            algorithm=federated_algorithm,
                            aggregator=mock_aggregator,
                            steps_between_parameter_updates=2,
                        )
                        protocol = protocol_factory.modeller(
                            mailbox=mock_modeller_mailbox
                        )

                        assert hasattr(protocol.algorithm, "pretrained_file")
                        assert (
                            protocol.algorithm.pretrained_file == pretrained_file_path
                        )
