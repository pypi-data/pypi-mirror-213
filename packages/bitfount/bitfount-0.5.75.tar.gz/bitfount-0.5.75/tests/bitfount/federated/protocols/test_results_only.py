"""Tests for the results only protocol."""
import math
from pathlib import Path
import re
from typing import Callable, cast
from unittest.mock import Mock, create_autospec

import pandas as pd
import pytest
from pytest import LogCaptureFixture, fixture
from pytest_mock import MockerFixture

from bitfount.backends.pytorch.models.models import PyTorchTabularClassifier
from bitfount.data.datasources.base_source import BaseSource
from bitfount.data.datasources.dataframe_source import DataFrameSource
from bitfount.data.datasplitters import PercentageSplitter
from bitfount.data.schema import BitfountSchema
from bitfount.federated.aggregators.aggregator import Aggregator
from bitfount.federated.aggregators.secure import SecureAggregator
from bitfount.federated.algorithms.column_avg import ColumnAverage
from bitfount.federated.algorithms.model_algorithms.base import (
    _BaseModellerModelAlgorithm,
    _BaseWorkerModelAlgorithm,
)
from bitfount.federated.algorithms.model_algorithms.evaluate import ModelEvaluation
from bitfount.federated.algorithms.model_algorithms.train_and_evaluate import (
    ModelTrainingAndEvaluation,
)
from bitfount.federated.algorithms.private_sql_query import PrivateSqlQuery
from bitfount.federated.algorithms.sql_query import SqlQuery
from bitfount.federated.exceptions import (
    AlgorithmError,
    BitfountTaskStartError,
    ProtocolError,
)
from bitfount.federated.helper import TaskContext
from bitfount.federated.protocols import results_only
from bitfount.federated.protocols.base import (
    BaseModellerProtocol,
    BaseWorkerProtocol,
    _BaseProtocol,
)
import bitfount.federated.protocols.base as protocols
from bitfount.federated.protocols.results_only import (
    ResultsOnly,
    _ModellerSide,
    _ResultsOnlyCompatibleAlgoFactory_,
    _ResultsOnlyCompatibleModelAlgoFactory,
    _ResultsOnlyCompatibleModellerAlgorithm,
    _ResultsOnlyDataCompatibleWorkerAlgorithm,
    _ResultsOnlyDataIncompatibleWorkerAlgorithm,
    _WorkerSide,
)
from bitfount.federated.transport.modeller_transport import _ModellerMailbox
from bitfount.federated.transport.worker_transport import (
    _InterPodWorkerMailbox,
    _WorkerMailbox,
)
from bitfount.hooks import _HOOK_DECORATED_ATTRIBUTE
from bitfount.schemas.utils import bf_dump, bf_load
from tests.utils import PytestRequest
from tests.utils.helper import (
    backend_test,
    create_dataset,
    create_datasource,
    create_datastructure,
    create_schema,
    integration_test,
    unit_test,
)


class TestWorkerSide:
    """Tests worker-side of ResultsOnly."""

    @fixture
    def datasource(self) -> DataFrameSource:
        """Returns datasource."""
        dataset = create_dataset()
        datasource = DataFrameSource(dataset)
        datasource.load_data()
        return datasource

    @fixture
    def mock_datasource(self) -> Mock:
        """Mock BaseSource."""
        mock_datasource: Mock = create_autospec(BaseSource, instance=True)
        return mock_datasource

    @fixture
    def mock_mailbox(self) -> Mock:
        """Mock WorkerMailbox."""
        mock_mailbox: Mock = create_autospec(_WorkerMailbox, instance=True)
        return mock_mailbox

    @fixture
    def worker_side_factory(self, mock_mailbox: Mock) -> Callable[[Mock], _WorkerSide]:
        """Factory to create WorkerSide instances from mock algorithms."""

        def _create(algo: Mock) -> _WorkerSide:
            return _WorkerSide(algorithm=algo, mailbox=mock_mailbox, aggregator=None)

        return _create

    @unit_test
    async def test_run_with_data_algo(
        self,
        mock_datasource: Mock,
        mock_mailbox: Mock,
        worker_side_factory: Callable[[Mock], _WorkerSide],
    ) -> None:
        """Tests WorkerSide.run() with an algorithm needing data."""
        mock_data_algorithm: Mock = create_autospec(
            _ResultsOnlyDataCompatibleWorkerAlgorithm, instance=True
        )
        worker_side: _WorkerSide = worker_side_factory(mock_data_algorithm)

        await worker_side.run(datasource=mock_datasource)

        mock_data_algorithm.initialise.assert_called_once()
        mock_data_algorithm.run.assert_called_once_with(data=mock_datasource)
        mock_mailbox.send_evaluation_results.assert_awaited_once_with(
            mock_data_algorithm.run.return_value
        )

    @unit_test
    async def test_run_with_non_data_algo(
        self,
        mock_datasource: Mock,
        mock_mailbox: Mock,
        worker_side_factory: Callable[[Mock], _WorkerSide],
    ) -> None:
        """Tests WorkerSide.run() with an algorithm not needing data."""
        mock_algorithm: Mock = create_autospec(
            _ResultsOnlyDataIncompatibleWorkerAlgorithm, instance=True
        )
        worker_side: _WorkerSide = worker_side_factory(mock_algorithm)

        await worker_side.run(datasource=mock_datasource)

        mock_algorithm.initialise.assert_called_once()
        mock_algorithm.run.assert_called_once_with()
        mock_mailbox.send_evaluation_results.assert_awaited_once_with(
            mock_algorithm.run.return_value
        )

    @unit_test
    async def test_run_with_model_algorithm(
        self,
        mock_datasource: Mock,
        mock_mailbox: Mock,
        mocker: MockerFixture,
        worker_side_factory: Callable[[Mock], _WorkerSide],
    ) -> None:
        """Tests WorkerrSide.run() receives parameters if model algo."""
        mock_algorithm: Mock = create_autospec(_BaseWorkerModelAlgorithm, instance=True)
        mock_algorithm.model = Mock()
        mock_algorithm.run = Mock()
        worker_side: _WorkerSide = worker_side_factory(mock_algorithm)
        mock_receive_parameters = mocker.patch.object(
            worker_side, "_receive_parameters"
        )

        await worker_side.run(datasource=mock_datasource)

        mock_receive_parameters.assert_awaited_once()
        mock_algorithm.initialise.assert_called_once()
        mock_algorithm.run.assert_called_once()
        mock_mailbox.send_evaluation_results.assert_awaited_once_with(
            mock_algorithm.run.return_value
        )

    @unit_test
    async def test_algorithm_error_gets_re_raised(
        self,
        mock_datasource: Mock,
        worker_side_factory: Callable[[Mock], _WorkerSide],
    ) -> None:
        """Tests that AlgorithmError gets re-raised."""
        mock_algorithm: Mock = create_autospec(
            _ResultsOnlyDataIncompatibleWorkerAlgorithm, instance=True
        )
        worker_side: _WorkerSide = worker_side_factory(mock_algorithm)
        mock_algorithm.run.side_effect = AlgorithmError("test")

        with pytest.raises(AlgorithmError, match="test"):
            await worker_side.run(datasource=mock_datasource)

        mock_algorithm.initialise.assert_called_once()
        mock_algorithm.run.assert_called_once_with()

    @unit_test
    async def test_non_algorithm_error_gets_re_raised_as_a_protocol_error(
        self,
        mock_datasource: Mock,
        worker_side_factory: Callable[[Mock], _WorkerSide],
    ) -> None:
        """Tests that non-AlgorithmError gets re-raised as a ProtocolError.

        In this test, we will raise it as part of the algorithm's run method
        for simplicity, but in reality the error would be raised elsewhere.
        """
        mock_algorithm: Mock = create_autospec(
            _ResultsOnlyDataIncompatibleWorkerAlgorithm, instance=True
        )
        worker_side: _WorkerSide = worker_side_factory(mock_algorithm)
        mock_algorithm.run.side_effect = ValueError("test")

        with pytest.raises(
            ProtocolError,
            match="Protocol _WorkerSide raised the following exception: test",
        ):
            await worker_side.run(datasource=mock_datasource)

        mock_algorithm.initialise.assert_called_once()
        mock_algorithm.run.assert_called_once_with()

    @unit_test
    async def test_run_with_batched_execution_and_iterable_datasource(
        self,
        mock_datasource: Mock,
        worker_side_factory: Callable[[Mock], _WorkerSide],
    ) -> None:
        """Tests that this raises an error.

        Only file system iterable datasources are supported with batched execution.
        """
        mock_algorithm: Mock = create_autospec(_BaseWorkerModelAlgorithm, instance=True)
        mock_algorithm.model = Mock()
        mock_algorithm.run = Mock()
        worker_side: _WorkerSide = worker_side_factory(mock_algorithm)
        mock_datasource.iterable = True
        mock_datasource.data_splitter = None

        with pytest.raises(
            BitfountTaskStartError,
            match=re.compile(
                "Batched execution is not supported for non-filesystem "
                "iterable sources.",
            ),
        ):
            await worker_side.run(
                datasource=mock_datasource,
                batched_execution=True,
                context=TaskContext.WORKER,
            )

    @unit_test
    async def test_run_with_batched_execution_and_no_datasource(
        self,
        mock_datasource: Mock,
        worker_side_factory: Callable[[Mock], _WorkerSide],
    ) -> None:
        """Tests that this raises an error.

        Datasource must be provided as a keyword argument for batched execution in the
        worker context.
        """
        mock_algorithm: Mock = create_autospec(_BaseWorkerModelAlgorithm, instance=True)
        mock_algorithm.model = Mock()
        mock_algorithm.run = Mock()
        worker_side: _WorkerSide = worker_side_factory(mock_algorithm)
        mock_datasource.iterable = True
        mock_datasource.data_splitter = None

        with pytest.raises(
            BitfountTaskStartError,
            match=(
                "Datasource must be provided as a keyword argument for "
                "batched execution."
            ),
        ):
            await worker_side.run(  # type: ignore[call-arg] # Reason: purpose of test.
                batched_execution=True,
                context=TaskContext.WORKER,
            )

    @unit_test
    async def test_run_with_batched_execution_and_no_context(
        self,
        mock_datasource: Mock,
        mock_mailbox: Mock,
        worker_side_factory: Callable[[Mock], _WorkerSide],
    ) -> None:
        """Tests that this raises an error.

        A Modeller/Worker context must be provided for batched execution.
        """
        mock_algorithm: Mock = create_autospec(_BaseWorkerModelAlgorithm, instance=True)
        mock_algorithm.model = Mock()
        mock_algorithm.run = Mock()
        worker_side: _WorkerSide = worker_side_factory(mock_algorithm)

        with pytest.raises(
            BitfountTaskStartError,
            match="Context must be provided for batched execution.",
        ):
            await worker_side.run(datasource=mock_datasource, batched_execution=True)

    @unit_test
    @pytest.mark.parametrize(
        "batch_size, test_pct", [(1, 10), (1, 100), (100, 10), (100, 100)]
    )
    async def test_run_with_batched_execution(
        self,
        batch_size: int,
        mock_datasource: Mock,
        mock_mailbox: Mock,
        mocker: MockerFixture,
        test_pct: int,
        worker_side_factory: Callable[[Mock], _WorkerSide],
    ) -> None:
        """Tests that batching is done correctly with batched execution."""
        mocker.patch(
            "bitfount.federated.protocols.base.BITFOUNT_TASK_BATCH_SIZE", batch_size
        )
        mock_algorithm: Mock = create_autospec(_BaseWorkerModelAlgorithm, instance=True)
        mock_algorithm.model = Mock()
        mock_algorithm.run = Mock()
        worker_side: _WorkerSide = worker_side_factory(mock_algorithm)
        mock_receive_parameters = mocker.patch.object(
            worker_side, "_receive_parameters"
        )
        mock_datasource.data_splitter = PercentageSplitter(0, test_pct)
        mock_datasource.iterable = False
        mock_datasource.data = pd.DataFrame({"a": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
        mock_datasource._test_idxs = None
        await worker_side.run(
            datasource=mock_datasource,
            batched_execution=True,
            context=TaskContext.WORKER,
        )
        dataset_length = len(mock_datasource.data)
        num_iterations = math.ceil((test_pct * dataset_length / 100) / batch_size)

        # Make sure the correct number of batches are run
        assert mock_algorithm.initialise.call_count == num_iterations
        assert mock_receive_parameters.await_count == num_iterations
        assert mock_algorithm.initialise.call_count == num_iterations
        assert mock_algorithm.run.call_count == num_iterations
        assert mock_mailbox.send_evaluation_results.await_count == num_iterations

    @unit_test
    async def test_batched_execution_restores_datasource_to_original_state(
        self,
        mock_datasource: Mock,
        mock_mailbox: Mock,
        mocker: MockerFixture,
        worker_side_factory: Callable[[Mock], _WorkerSide],
    ) -> None:
        """Tests that datasource is restored to its original state.

        This ensures that a batched execution task can be run multiple times
        sequentially.
        """
        mock_algorithm: Mock = create_autospec(_BaseWorkerModelAlgorithm, instance=True)
        mock_algorithm.model = Mock()
        mock_algorithm.run = Mock()
        worker_side: _WorkerSide = worker_side_factory(mock_algorithm)
        mock_receive_parameters = mocker.patch.object(
            worker_side, "_receive_parameters"
        )
        mock_datasource.iterable = False
        mock_datasource.data_splitter = PercentageSplitter(0, 50)
        mock_datasource.data = pd.DataFrame({"a": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
        mock_datasource._test_idxs = None
        await worker_side.run(
            datasource=mock_datasource,
            batched_execution=True,
            context=TaskContext.WORKER,
        )
        # Make sure the correct number of batches are run
        assert mock_mailbox.send_evaluation_results.await_count == 1
        assert mock_receive_parameters.await_count == 1

        # Make sure the datasource is restored to its original state
        assert len(mock_datasource.data) == 10
        assert mock_datasource._test_idxs is not None
        assert len(mock_datasource._test_idxs) == 5

    @unit_test
    async def test_receive_parameters(
        self,
        mock_mailbox: Mock,
        mocker: MockerFixture,
        worker_side_factory: Callable[[Mock], _WorkerSide],
    ) -> None:
        """Test _receive_parameters awaits _get_model_parameters."""
        mock_algorithm: Mock = create_autospec(
            _ResultsOnlyDataIncompatibleWorkerAlgorithm, instance=True
        )
        mock_get_model_parameters = mocker.patch(
            "bitfount.federated.protocols.results_only._get_model_parameters"
        )
        worker_side: _WorkerSide = worker_side_factory(mock_algorithm)
        await worker_side._receive_parameters()
        mock_get_model_parameters.assert_awaited_once_with(mock_mailbox)

    @integration_test
    async def test_batched_execution_with_model_evaluation(
        self,
        datasource: DataFrameSource,
        mocker: MockerFixture,
        worker_side_factory: Callable[[Mock], _WorkerSide],
    ) -> None:
        """Test batched execution with ModelEvaluation."""
        model = PyTorchTabularClassifier(
            datastructure=create_datastructure(),
            schema=create_schema(classification=True),
            epochs=2,
        )
        algorithm_factory = ModelEvaluation(model=model)
        algorithm = algorithm_factory.worker(Mock())
        mocker.patch.object(algorithm, "initialise")
        mocker.patch.object(algorithm, "run", return_value=[1, 2, 3, 4])
        worker_side: _WorkerSide = worker_side_factory(algorithm)  # type: ignore[arg-type] # Reason: integration test. # noqa: B950
        mock_receive_parameters = mocker.patch.object(
            worker_side, "_receive_parameters"
        )
        results = await worker_side.run(
            datasource=datasource,
            batched_execution=True,
            context=TaskContext.WORKER,
        )
        # The number of batches/results should be 4
        assert len(results) == 4
        assert mock_receive_parameters.await_count == 4


class TestModellerSide:
    """Tests modeller-side of ResultsOnly."""

    @fixture
    def mock_datasource(self) -> Mock:
        """Mock DataSource."""
        mock_datasource: Mock = create_autospec(BaseSource, instance=True)
        return mock_datasource

    @fixture
    def mock_mailbox(self) -> Mock:
        """Mock ModellerMailbox."""
        mock_mailbox: Mock = create_autospec(_ModellerMailbox, instance=True)
        return mock_mailbox

    @fixture
    def modeller_side_factory(
        self, mock_mailbox: Mock
    ) -> Callable[[Mock], _ModellerSide]:
        """Factory to create ModellerSide instances from mock algorithms."""

        def _create(algo: Mock) -> _ModellerSide:
            return _ModellerSide(algorithm=algo, mailbox=mock_mailbox, aggregator=None)

        return _create

    @unit_test
    async def test_run(
        self,
        mock_mailbox: Mock,
        modeller_side_factory: Callable[[Mock], _ModellerSide],
    ) -> None:
        """Tests ModellerSide.run() with an algorithm not needing data."""
        mock_algorithm: Mock = create_autospec(
            _ResultsOnlyCompatibleModellerAlgorithm, instance=True
        )
        modeller_side: _ModellerSide = modeller_side_factory(mock_algorithm)

        await modeller_side.run()

        mock_algorithm.initialise.assert_called_once()
        mock_algorithm.run.assert_called_once()
        mock_mailbox.get_evaluation_results_from_workers.assert_awaited_once()

    @unit_test
    async def test_run_with_model_algorithm(
        self,
        mock_mailbox: Mock,
        mocker: MockerFixture,
        modeller_side_factory: Callable[[Mock], _ModellerSide],
    ) -> None:
        """Tests ModellerSide.run() sends parameters if model algo."""
        mock_algorithm: Mock = create_autospec(
            _BaseModellerModelAlgorithm, instance=True
        )
        mock_algorithm.model = Mock()
        mock_algorithm.run = Mock()
        modeller_side: _ModellerSide = modeller_side_factory(mock_algorithm)
        mock_send_parameters = mocker.patch.object(modeller_side, "_send_parameters")

        await modeller_side.run()

        mock_send_parameters.assert_awaited_once()
        mock_algorithm.initialise.assert_called_once()
        mock_algorithm.run.assert_called_once()
        mock_mailbox.get_evaluation_results_from_workers.assert_awaited_once()

    @unit_test
    async def test_send_parameters(
        self,
        mock_mailbox: Mock,
        mocker: MockerFixture,
        modeller_side_factory: Callable[[Mock], _ModellerSide],
    ) -> None:
        """Test _send_parameters awaits _send_model_parameters."""
        mock_algorithm: Mock = create_autospec(
            _ResultsOnlyDataIncompatibleWorkerAlgorithm, instance=True
        )
        new_parameters = Mock()
        mock_send_model_parameters = mocker.patch(
            "bitfount.federated.protocols.results_only._send_model_parameters"
        )
        modeller_side: _ModellerSide = modeller_side_factory(mock_algorithm)

        await modeller_side._send_parameters(new_parameters)

        mock_send_model_parameters.assert_awaited_once_with(
            new_parameters, mock_mailbox
        )

    @integration_test
    async def test_run_model_with_batched_execution(
        self,
        mock_mailbox: Mock,
        mocker: MockerFixture,
        modeller_side_factory: Callable[[Mock], _ModellerSide],
    ) -> None:
        """Tests ModellerSide.run() with a real model with batched execution."""
        mock_mailbox.get_num_batches_message.return_value = 4
        mock_mailbox.get_evaluation_results_from_workers.return_value = {"AUC": 0.9}
        mock_send_model_parameters = mocker.patch(
            "bitfount.federated.protocols.results_only._send_model_parameters"
        )
        model = PyTorchTabularClassifier(
            datastructure=create_datastructure(),
            schema=create_schema(classification=True),
            epochs=2,
        )
        algorithm_factory = ModelEvaluation(model=model)
        algorithm = algorithm_factory.modeller()
        modeller_side: _ModellerSide = modeller_side_factory(algorithm)  # type: ignore[arg-type] # Reason: integration test. # noqa: B950
        await modeller_side.run(batched_execution=True, context=TaskContext.MODELLER)
        assert mock_send_model_parameters.await_count == 4


@unit_test
class TestResultsOnly:
    """Test Results Only protocol."""

    @fixture(scope="function", params=[None, "/mock/file"])
    def remote_algorithm(self, request: PytestRequest) -> ModelTrainingAndEvaluation:
        """Returns remote algorithm."""
        return ModelTrainingAndEvaluation(model=Mock(), pretrained_file=request.param)

    def test_results_only_methods_are_decorated(self) -> None:
        """Tests that protocol methods are decorated.

        The `__init__` and `run` methods should be auto-decorated with a function which
        calls the relevant hooks before and after.
        """
        protocol_factory = ResultsOnly(algorithm=Mock())
        worker_protocol = protocol_factory.worker(mailbox=Mock(), hub=Mock())
        modeller_protocol = protocol_factory.modeller(mailbox=Mock())
        for protocol in (worker_protocol, modeller_protocol):
            assert isinstance(protocol, (_WorkerSide, _ModellerSide))
            assert getattr(protocol.__init__, _HOOK_DECORATED_ATTRIBUTE)  # type: ignore[misc] # Reason: This is a test. # noqa: B950
            assert getattr(protocol.run, _HOOK_DECORATED_ATTRIBUTE)

    def test_init_method_with_aggregator(
        self, remote_algorithm: ModelTrainingAndEvaluation
    ) -> None:
        """Tests init method with aggregator."""
        aggregator: Mock = Mock()
        protocol = ResultsOnly(algorithm=remote_algorithm, aggregator=aggregator)
        assert protocol.aggregator is aggregator

    def test_init_method_with_secure_aggregation(
        self, remote_algorithm: ModelTrainingAndEvaluation
    ) -> None:
        """Tests init method with aggregator."""
        protocol = ResultsOnly(algorithm=remote_algorithm, secure_aggregation=True)
        assert isinstance(protocol.aggregator, SecureAggregator)

    def test_init_method_without_aggregator(
        self, caplog: LogCaptureFixture, remote_algorithm: ModelTrainingAndEvaluation
    ) -> None:
        """Tests init method with aggregator."""
        caplog.set_level("INFO")
        protocol = ResultsOnly(algorithm=remote_algorithm)
        assert protocol.aggregator is None
        assert (
            "No aggregator specified. Will return a dictionary of results."
            in caplog.text
        )

    def test_modeller(
        self, mock_modeller_mailbox: Mock, remote_algorithm: ModelTrainingAndEvaluation
    ) -> None:
        """Test modeller method."""
        protocol_factory = ResultsOnly(algorithm=remote_algorithm)
        protocol = protocol_factory.modeller(mailbox=mock_modeller_mailbox)
        for type_ in [
            _BaseProtocol,
            BaseModellerProtocol,
            results_only._ModellerSide,
        ]:
            assert isinstance(protocol, type_)

    def test_worker(
        self,
        mock_hub: Mock,
        mock_worker_mailbox: Mock,
        remote_algorithm: ModelTrainingAndEvaluation,
    ) -> None:
        """Test worker method."""
        protocol_factory = ResultsOnly(algorithm=remote_algorithm)
        protocol = protocol_factory.worker(mailbox=mock_worker_mailbox, hub=mock_hub)
        for type_ in [
            _BaseProtocol,
            BaseWorkerProtocol,
            results_only._WorkerSide,
        ]:
            assert isinstance(protocol, type_)

    def test_worker_with_aggregator(
        self,
        mock_hub: Mock,
        mock_worker_mailbox: Mock,
        remote_algorithm: ModelTrainingAndEvaluation,
    ) -> None:
        """Test worker method with aggregator."""
        aggregator = Mock(spec=Aggregator)
        protocol_factory = ResultsOnly(
            algorithm=remote_algorithm, aggregator=aggregator
        )
        protocol: _WorkerSide = protocol_factory.worker(
            mailbox=mock_worker_mailbox, hub=mock_hub
        )
        assert protocol.aggregator is not None
        aggregator.worker.assert_called_once()

    async def test_worker_with_aggregator_privatesql_results(
        self,
        mock_hub: Mock,
        mock_worker_mailbox: Mock,
        mocker: MockerFixture,
    ) -> None:
        """Test worker method with aggregator."""
        aggregator_factory = Aggregator()
        algorithm_factory = PrivateSqlQuery(
            query="SELECT AVG(G) AS AVG_OF_G FROM df.df",
            epsilon=0.1,
            delta=0.001,
            column_ranges={},
        )
        protocol_factory = ResultsOnly(
            algorithm=algorithm_factory, aggregator=aggregator_factory
        )
        protocol: _WorkerSide = protocol_factory.worker(
            mailbox=mock_worker_mailbox, hub=mock_hub
        )
        mock_aggregator_run = mocker.patch.object(protocol.aggregator, "run")
        mocker.patch.object(protocol.algorithm, "run", return_value=42)
        await protocol.run(
            datasource=create_datasource(classification=True),
        )
        assert protocol.aggregator is not None
        mock_aggregator_run.assert_called_once()

    def test_worker_with_secure_aggregator(
        self,
        mock_hub: Mock,
        remote_algorithm: ModelTrainingAndEvaluation,
    ) -> None:
        """Test worker method with secure aggregator."""
        aggregator = Mock(spec=SecureAggregator)
        mailbox = Mock(spec=_InterPodWorkerMailbox)
        protocol_factory = ResultsOnly(
            algorithm=remote_algorithm, aggregator=aggregator
        )

        protocol: _WorkerSide = protocol_factory.worker(mailbox=mailbox, hub=mock_hub)
        assert protocol.aggregator is not None
        aggregator.worker.assert_called_once_with(mailbox=mailbox)

    def test_worker_with_secure_aggregator_raises_type_error(
        self,
        mock_hub: Mock,
        mock_worker_mailbox: Mock,
        remote_algorithm: ModelTrainingAndEvaluation,
    ) -> None:
        """Test worker method with secure aggregator raises TypeError.

        This happens if the mailbox is not compatible with the aggregator.
        """
        aggregator = Mock(spec=SecureAggregator)
        protocol_factory = ResultsOnly(
            algorithm=remote_algorithm, aggregator=aggregator
        )
        with pytest.raises(
            TypeError,
            match="Inter-pod aggregators require an inter-pod worker mailbox.",
        ):
            protocol_factory.worker(mailbox=mock_worker_mailbox, hub=mock_hub)

    def test_worker_with_unrecognised_aggregator_raises_type_error(
        self,
        mock_hub: Mock,
        mock_worker_mailbox: Mock,
        remote_algorithm: ModelTrainingAndEvaluation,
    ) -> None:
        """Test worker method with unrecognised aggregator raises TypeError."""
        aggregator = Mock()
        protocol_factory = ResultsOnly(
            algorithm=remote_algorithm, aggregator=aggregator
        )
        with pytest.raises(
            TypeError,
            match=re.escape(
                f"Unrecognised aggregator factory ({type(aggregator)}); "
                f"unable to determine how to call .worker() factory method."
            ),
        ):
            protocol_factory.worker(mailbox=mock_worker_mailbox, hub=mock_hub)

    def test__validate_algorithm_accepts(self) -> None:
        """Tests _validate_algorithm accepts compatible."""
        # Test with ResultsOnlyCompatibleAlgoFactory
        mock_algorithm: Mock = create_autospec(
            _ResultsOnlyCompatibleAlgoFactory_, instance=True
        )
        ResultsOnly._validate_algorithm(mock_algorithm)

        # Test with ResultsOnlyCompatibleModelAlgoFactory
        mock_algorithm = create_autospec(
            _ResultsOnlyCompatibleModelAlgoFactory, instance=True
        )
        ResultsOnly._validate_algorithm(mock_algorithm)

    def test__validate_algorithm_rejects(self) -> None:
        """Tests _validate_algorithm rejects incompatible."""
        mock_algorithm: Mock = Mock(spec_set=["__name__"])
        with pytest.raises(
            TypeError,
            match=re.escape(
                f"The {ResultsOnly.__name__} protocol does not "
                f"support the {type(mock_algorithm).__name__} algorithm."
            ),
        ):
            ResultsOnly._validate_algorithm(mock_algorithm)

    @unit_test
    def test_run_protocol(self, mocker: MockerFixture) -> None:
        """Tests we can run a protocol."""
        algorithm = ColumnAverage(field="TARGET", table_name="fake")
        # Mock out Modeller creation
        mock_modeller = mocker.patch(
            "bitfount.federated.protocols.base._Modeller", autospec=True
        )
        mock_modeller.return_value = mock_modeller  # for __init__
        mock_modeller.run.return_value = None

        protocol = ResultsOnly(algorithm=algorithm)
        protocol.run(
            pod_identifiers=["fake/fake"],
            hub=Mock(),
            message_service=Mock(),
            private_key_or_file=Path("fake.pem"),
        )

        mock_modeller.run.assert_called_once_with(
            ["fake/fake"],
            require_all_pods=False,
            model_out=None,
            project_id=None,
            run_on_new_data_only=False,
            batched_execution=False,
        )

    @unit_test
    def test_run_protocol_idp_is_set(self, mocker: MockerFixture) -> None:
        """Tests that the idp url gets initialized."""
        algorithm = ColumnAverage(field="TARGET", table_name="fake")

        # Mock out Modeller creation
        mock_modeller = mocker.patch(
            "bitfount.federated.protocols.base._Modeller", autospec=True
        )
        mock_modeller.return_value = mock_modeller  # for __init__
        mock_modeller.run.return_value = None
        mock_idp_url = mocker.patch(
            "bitfount.federated.protocols.base._get_idp_url",
            return_value="https://idp-url.unit-test.bitfount.com",
        )

        protocol = ResultsOnly(algorithm=algorithm)
        protocol.run(
            pod_identifiers=["fake/fake"],
            hub=Mock(),
            message_service=Mock(),
            private_key_or_file=Path("fake.pem"),
        )

        mock_idp_url.assert_called_once()


@backend_test
@unit_test
class TestMarshmallowSerialization:
    """Test Marshmallow Serialization for column average algorithm."""

    def test_serialization_model_algorithm(self) -> None:
        """Test Marshmallow Serialization for a model algorithm."""
        model = PyTorchTabularClassifier(
            datastructure=create_datastructure(),
            schema=BitfountSchema(),
            epochs=2,
        )
        algorithm_factory = ModelEvaluation(model=model)
        results_only = ResultsOnly(algorithm=algorithm_factory)
        dumped = bf_dump(results_only)
        loaded = bf_load(dumped, protocols.registry)
        assert results_only.class_name == loaded.class_name
        from tests.bitfount.backends.pytorch.models.test_models import assert_vars_equal

        assert_vars_equal(
            vars(
                cast(
                    _ResultsOnlyCompatibleModelAlgoFactory, results_only.algorithm
                ).model
            ),
            vars(loaded.algorithm.model),
        )

    def test_serialization_sql_algorithm(self) -> None:
        """Test Marshmallow Serialization for sql query algorithm."""
        algorithm_factory = SqlQuery(query="SELECT * FROM df")
        results_only = ResultsOnly(algorithm=algorithm_factory)
        dumped = bf_dump(results_only)
        loaded = bf_load(dumped, protocols.registry)
        assert results_only.class_name == loaded.class_name
        assert results_only.algorithm.__dict__ == loaded.algorithm.__dict__
