import unittest
from unittest.mock import MagicMock

from leanit_mweb.orm.model import Model
from leanit_mweb.orm.fields import IntegerField, StringField


class TestModel(unittest.TestCase):
    def setUp(self):
        # Create a mock database connection
        self.mock_db = MagicMock()

        class MyModel(Model):
            _table = "my_table"
            name = StringField()
            age = IntegerField()
            type = StringField()

        self.model = MyModel

        # Set the _db attribute of the Model class to the mock database connection
        self.model._db = self.mock_db

    def test_delete_all(self):
        # Call the delete_all method with some arguments
        self.model.delete_all(name__in=["foo", "bar"], age__lt=30, type="baz")

        # Assert that the execute method of the mock database connection was called with the correct SQL and values
        expected_sql = 'DELETE FROM "my_table" WHERE name IN %s AND age < %s AND type = %s'
        expected_values = (["foo", "bar"], 30, "baz")
        self.mock_db.execute.assert_called_once_with(expected_sql, expected_values, {})

if __name__ == '__main__':
    unittest.main()