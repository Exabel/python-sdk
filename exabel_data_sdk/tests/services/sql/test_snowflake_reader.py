import unittest

from exabel_data_sdk.services.sql.snowflake_reader import SnowflakeReader


class TestSnowflakeReader(unittest.TestCase):
    def test_snowflake_reader_constructor(self):
        connection_args = {
            "account": "account",
            "user": "username",
            "password": "password",
            "warehouse": "warehouse",
            "database": "database",
            "schema": "schema",
            "role": "role",
            "login_timeout": 15,
        }
        kwargs = {"kwarg1": "value1", "kwarg2": "value2"}
        reader = SnowflakeReader(connection_args, kwargs=kwargs)

        self.assertDictEqual(connection_args, reader.connection_args)
        self.assertDictEqual(kwargs, reader.kwargs)
