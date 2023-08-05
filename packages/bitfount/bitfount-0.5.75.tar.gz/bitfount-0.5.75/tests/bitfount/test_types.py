"""Tests for bitfount.types module."""
from pathlib import Path

from marshmallow import Schema

from bitfount.types import BinaryFile
from tests.utils.helper import unit_test


class TestSchema(Schema):
    """Dummy schema for testing."""

    file = BinaryFile()


@unit_test
def test_binary_file_serialization_deserialization(tmp_path: Path) -> None:
    """Tests that binary file serialization and deserialization works."""
    with open(tmp_path / "test.bin", "wb") as f:
        f.write(b"test")
    schema = TestSchema()
    dumped_schema = schema.dump({"file": tmp_path / "test.bin"})
    assert dumped_schema == {"file": b"test".hex()}
    loaded_object = schema.load(dumped_schema)
    # The deserialization still keeps the file as binary
    assert loaded_object == {"file": b"test".hex()}
