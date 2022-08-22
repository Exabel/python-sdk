import unittest

from exabel_data_sdk.scripts.export_data import ExportData


class TestExportData(unittest.TestCase):
    def test_args(self):
        export_data = ExportData(
            [
                "script",
                "--query",
                "query",
                "--filename",
                "filename",
                "--format",
                "format",
                "--reauthenticate",
                "--backend",
                "backend",
                "--auth0",
                "auth0",
                "--client-id",
                "client-id",
            ]
        )
        args = export_data.parse_arguments()
        self.assertEqual(args.query, "query")
        self.assertEqual(args.filename, "filename")
        self.assertEqual(args.format, "format")
        self.assertTrue(args.reauthenticate)
        self.assertEqual(args.backend, "backend")
        self.assertEqual(args.auth0, "auth0")
        self.assertEqual(args.client_id, "client-id")
