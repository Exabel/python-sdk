import math
import unittest
from typing import Optional

import pandas as pd
from dateutil import tz

from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.client.api.data_classes.entity_type import EntityType
from exabel_data_sdk.scripts.load_time_series_from_file import LoadTimeSeriesFromFile
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import SearchEntitiesResponse, SearchTerm
from exabel_data_sdk.tests.client.exabel_mock_client import ExabelMockClient
from exabel_data_sdk.tests.decorators import requires_modules

common_args = ["script-name", "--sep", ";", "--api-key", "123"]


@requires_modules("openpyxl")
class TestUploadTimeSeries(unittest.TestCase):
    def setUp(self) -> None:
        self.client = ExabelMockClient(namespace="ns")

    def check_import(
        self,
        filename,
        *expected_calls,
        pit_from_file: bool = False,
        entity_type: Optional[str] = None,
        identifier_type: Optional[str] = None
    ):
        """Check that the file can be imported and that it produces the given time series."""
        args = common_args + [
            "--filename",
            filename,
            "--namespace",
            "ns",
            "--no-create-library-signal",
            "--create-missing-signals",
        ]
        if entity_type is not None:
            args += ["--entity-type", entity_type]
        if identifier_type is not None:
            args += ["--identifier-type", identifier_type]
        if not pit_from_file:
            args += ["--pit-current-time"]

        script = LoadTimeSeriesFromFile(args)
        script.run_script(self.client, script.parse_arguments())

        call_args_list = (
            self.client.time_series_api.bulk_upsert_time_series.call_args_list  # type: ignore
        )
        self.assertEqual(len(expected_calls), len(call_args_list))
        for call, expected_series in enumerate(expected_calls):
            series = {s.name: s for s in call_args_list[call][0][0]}
            self.assertEqual(len(expected_series), len(series))

            for expected in expected_series:
                pd.testing.assert_series_equal(
                    expected,
                    series[expected.name],
                    check_freq=False,
                    check_dtype=False,
                )

    def test_read_excel__entities_in_columns_1(self):
        self.check_import(
            "./exabel_data_sdk/tests/resources/data/entities_in_columns_example_1.xlsx",
            [
                pd.Series(
                    [1, 2, 3],
                    pd.date_range("2020-10-10", periods=3, tz=tz.tzutc()),
                    name="entityTypes/brand/entities/ns.brand1/signals/ns.mysig1",
                ),
                pd.Series(
                    [4, 6],
                    pd.DatetimeIndex(["2020-10-10", "2020-10-12"], tz=tz.tzutc()),
                    name="entityTypes/brand/entities/ns.brand2/signals/ns.mysig1",
                ),
                pd.Series(
                    [10.1, 10.2],
                    pd.date_range("2020-10-10", periods=2, tz=tz.tzutc()),
                    name="entityTypes/brand/entities/ns.brand1/signals/ns.mysig2",
                ),
            ],
        )

    def test_read_excel__entities_in_columns_1__override_entity_type_should_fail(self):
        with self.assertRaises(SystemExit) as cm:
            self.check_import(
                "./exabel_data_sdk/tests/resources/data/entities_in_columns_example_1.xlsx",
                entity_type="anything_should_fail",
            )
        self.assertEqual(cm.exception.code, 1)

    def test_read_excel__entities_in_columns_2(self):
        self.check_import(
            "./exabel_data_sdk/tests/resources/data/entities_in_columns_example_2.xlsx",
            [
                pd.Series(
                    [1, 2],
                    pd.date_range("2020-10-10", periods=2, tz=tz.tzutc()),
                    name="entityTypes/brand/entities/b1/signals/ns.mysig1",
                ),
                pd.Series(
                    [4, 5, 6],
                    pd.date_range("2020-10-10", periods=3, tz=tz.tzutc()),
                    name="entityTypes/brand/entities/b2/signals/ns.mysig1",
                ),
                pd.Series(
                    [10.1, 10.2, 10.3],
                    pd.date_range("2020-10-10", periods=3, tz=tz.tzutc()),
                    name="entityTypes/brand/entities/b1/signals/ns.mysig2",
                ),
            ],
        )

    def test_read_excel__companies_in_columns_1(self):
        company1 = Entity(name="entityTypes/company/entities/ENT-1", display_name="ENT 1")
        company2 = Entity(name="entityTypes/company/entities/ENT-2", display_name="ENT 2")
        self.client.entity_api.create_entity(
            company1,
            "entityTypes/company",
        )
        self.client.entity_api.create_entity(
            company2,
            "entityTypes/company",
        )
        self.client.entity_api.search.entities_by_terms.return_value = [
            SearchEntitiesResponse.SearchResult(entities=[company1.to_proto()]),
            SearchEntitiesResponse.SearchResult(entities=[company2.to_proto()]),
        ]
        self.check_import(
            "./exabel_data_sdk/tests/resources/data/companies_in_columns_example_1.xlsx",
            [
                pd.Series(
                    [1, 2, 3],
                    pd.date_range("2020-10-10", periods=3, tz=tz.tzutc()),
                    name="entityTypes/company/entities/ENT-1/signals/ns.mysig1",
                ),
                pd.Series(
                    [4, 6],
                    pd.DatetimeIndex(["2020-10-10", "2020-10-12"], tz=tz.tzutc()),
                    name="entityTypes/company/entities/ENT-2/signals/ns.mysig2",
                ),
            ],
        )

    def test_read_excel__companies_in_columns_unmappable(self):
        company1 = Entity(name="entityTypes/company/entities/ENT-1", display_name="ENT 1")
        self.client.entity_api.create_entity(
            company1,
            "entityTypes/company",
        )
        self.client.entity_api.search.entities_by_terms.return_value = [
            SearchEntitiesResponse.SearchResult(entities=[company1.to_proto()]),
        ]
        self.check_import(
            "./exabel_data_sdk/tests/resources/data/companies_in_columns_example_1.xlsx",
            [
                pd.Series(
                    [1, 2, 3],
                    pd.date_range("2020-10-10", periods=3, tz=tz.tzutc()),
                    name="entityTypes/company/entities/ENT-1/signals/ns.mysig1",
                ),
            ],
        )

    def test_read_excel__signal_in_row_1(self):
        company1 = Entity(name="entityTypes/company/entities/ENT-1", display_name="ENT 1")
        company2 = Entity(name="entityTypes/company/entities/ENT-2", display_name="ENT 2")
        self.client.entity_api.create_entity(
            company1,
            "entityTypes/company",
        )
        self.client.entity_api.create_entity(
            company2,
            "entityTypes/company",
        )
        self.client.entity_api.search.entities_by_terms.return_value = [
            SearchEntitiesResponse.SearchResult(entities=[company1.to_proto()]),
            SearchEntitiesResponse.SearchResult(entities=[company2.to_proto()]),
        ]
        self.check_import(
            "./exabel_data_sdk/tests/resources/data/signal_in_row_example_1.xlsx",
            [
                pd.Series(
                    [1, 1.1, 1.2, math.nan, 1.4],
                    pd.date_range("2022-10-10", periods=5, tz=tz.tzutc()),
                    name="entityTypes/company/entities/ENT-1/signals/ns.my_sig",
                ),
                pd.Series(
                    [40.1, 40.2],
                    pd.date_range("2022-10-10", periods=2, tz=tz.tzutc()),
                    name="entityTypes/company/entities/ENT-2/signals/ns.other_sig",
                ),
            ],
        )

    def test_read_excel__signal_in_row_1__override_entity_type__with_identifier_type(self):
        company1 = Entity(name="entityTypes/company/entities/ENT-1", display_name="ENT 1")
        company2 = Entity(name="entityTypes/company/entities/ENT-2", display_name="ENT 2")
        self.client.entity_api.create_entity(
            company1,
            "entityTypes/company",
        )
        self.client.entity_api.create_entity(
            company2,
            "entityTypes/company",
        )
        self.client.entity_api.search.entities_by_terms.return_value = [
            SearchEntitiesResponse.SearchResult(entities=[company1.to_proto()]),
            SearchEntitiesResponse.SearchResult(entities=[company2.to_proto()]),
        ]
        self.check_import(
            "./exabel_data_sdk/tests/resources/data/signal_in_row_example_1.xlsx",
            [
                pd.Series(
                    [1, 1.1, 1.2, math.nan, 1.4],
                    pd.date_range("2022-10-10", periods=5, tz=tz.tzutc()),
                    name="entityTypes/company/entities/ENT-1/signals/ns.my_sig",
                ),
                pd.Series(
                    [40.1, 40.2],
                    pd.date_range("2022-10-10", periods=2, tz=tz.tzutc()),
                    name="entityTypes/company/entities/ENT-2/signals/ns.other_sig",
                ),
            ],
            entity_type="company",
            identifier_type="bloomberg_symbol",
        )
        search_kwargs = self.client.entity_api.search.entities_by_terms.call_args[1]
        self.assertEqual("entityTypes/company", search_kwargs.get("entity_type"))
        self.assertCountEqual(
            [
                SearchTerm(field="bloomberg_symbol", query="AAPL US"),
                SearchTerm(field="bloomberg_symbol", query="MSFT US"),
            ],
            search_kwargs.get("terms"),
        )

    def test_read_excel__signal_in_row_1__unmappable_entity(self):
        company1 = Entity(name="entityTypes/company/entities/ENT-1", display_name="ENT 1")
        self.client.entity_api.create_entity(
            company1,
            "entityTypes/company",
        )
        self.client.entity_api.search.entities_by_terms.return_value = [
            SearchEntitiesResponse.SearchResult(entities=[company1.to_proto()]),
        ]
        self.check_import(
            "./exabel_data_sdk/tests/resources/data/signal_in_row_example_1.xlsx",
            [
                pd.Series(
                    [1, 1.1, 1.2, math.nan, 1.4],
                    pd.date_range("2022-10-10", periods=5, tz=tz.tzutc()),
                    name="entityTypes/company/entities/ENT-1/signals/ns.my_sig",
                ),
            ],
        )

    def test_read_excel__signal_in_row_2(self):
        def timestamp(t: str):
            return pd.Timestamp(t, tz=tz.tzutc())

        self.check_import(
            "./exabel_data_sdk/tests/resources/data/signal_in_row_example_2.xlsx",
            [
                pd.Series(
                    [1, 1.1, 1.2, math.nan, 1.4],
                    pd.MultiIndex.from_tuples(
                        [
                            (timestamp("2022-10-10"), timestamp("2022-10-20")),
                            (timestamp("2022-10-11"), timestamp("2022-10-21")),
                            (timestamp("2022-10-11"), timestamp("2022-10-22")),
                            (timestamp("2022-10-10"), timestamp("2022-10-23")),
                            (timestamp("2022-10-14"), timestamp("2022-10-24")),
                        ]
                    ),
                    name="entityTypes/brand/entities/ns.brand1/signals/ns.my_sig",
                ),
                pd.Series(
                    [40.1, 40.2],
                    pd.MultiIndex.from_tuples(
                        [
                            (timestamp("2022-10-10"), timestamp("2022-10-20")),
                            (timestamp("2022-10-11"), timestamp("2022-10-21")),
                        ]
                    ),
                    name="entityTypes/brand/entities/ns.brand2/signals/ns.other_sig",
                ),
            ],
            pit_from_file=True,
        )

    def test_read_excel__signal_in_row_3(self):
        self.check_import(
            "./exabel_data_sdk/tests/resources/data/signal_in_row_example_3.xlsx",
            [
                pd.Series(
                    [1],
                    pd.date_range("2022-10-10", periods=1, tz=tz.tzutc()),
                    name="entityTypes/brand/entities/ns.0001/signals/ns.my_sig",
                ),
                pd.Series(
                    [1.1],
                    pd.date_range("2022-10-11", periods=1, tz=tz.tzutc()),
                    name="entityTypes/brand/entities/ns.0002/signals/ns.my_sig",
                ),
            ],
        )

    def test_read_excel__signal_in_row_3__override_entity_type(self):
        self.check_import(
            "./exabel_data_sdk/tests/resources/data/signal_in_row_example_3.xlsx",
            [
                pd.Series(
                    [1],
                    pd.date_range("2022-10-10", periods=1, tz=tz.tzutc()),
                    name="entityTypes/business_segment/entities/0001/signals/ns.my_sig",
                ),
                pd.Series(
                    [1.1],
                    pd.date_range("2022-10-11", periods=1, tz=tz.tzutc()),
                    name="entityTypes/business_segment/entities/0002/signals/ns.my_sig",
                ),
            ],
            entity_type="business_segment",
        )

    def test_read_excel__signal_in_row_4__global_entity(self):
        def timestamp(t: str):
            return pd.Timestamp(t, tz=tz.tzutc())

        self.check_import(
            "./exabel_data_sdk/tests/resources/data/signal_in_row_example_4.xlsx",
            [
                pd.Series(
                    [1, 1.1, 1.2, math.nan, 1.4],
                    pd.MultiIndex.from_tuples(
                        [
                            (timestamp("2022-10-10"), timestamp("2022-10-20")),
                            (timestamp("2022-10-11"), timestamp("2022-10-21")),
                            (timestamp("2022-10-11"), timestamp("2022-10-22")),
                            (timestamp("2022-10-10"), timestamp("2022-10-23")),
                            (timestamp("2022-10-14"), timestamp("2022-10-24")),
                        ]
                    ),
                    name="entityTypes/global/entities/global/signals/ns.my_sig",
                ),
                pd.Series(
                    [40.1, 40.2],
                    pd.MultiIndex.from_tuples(
                        [
                            (timestamp("2022-10-10"), timestamp("2022-10-20")),
                            (timestamp("2022-10-11"), timestamp("2022-10-21")),
                        ]
                    ),
                    name="entityTypes/global/entities/global/signals/ns.other_sig",
                ),
            ],
            pit_from_file=True,
        )

    def test_read_excel__signal_in_row_6__namespaced_entity_type(self):
        self.client.entity_api.create_entity_type(
            EntityType("entityTypes/ns.brand", "Brands", "Brands")
        )

        def timestamp(t: str):
            return pd.Timestamp(t, tz=tz.tzutc())

        self.check_import(
            "./exabel_data_sdk/tests/resources/data/signal_in_row_example_6.xlsx",
            [
                pd.Series(
                    [1, 1.1, 1.4],
                    index=[
                        timestamp("2022-10-10"),
                        timestamp("2022-10-11"),
                        timestamp("2022-10-14"),
                    ],
                    name="entityTypes/ns.brand/entities/ns.brand1/signals/ns.my_sig",
                ),
                pd.Series(
                    [40.1, 40.2],
                    index=[
                        timestamp("2022-10-10"),
                        timestamp("2022-10-11"),
                    ],
                    name="entityTypes/ns.brand/entities/ns.brand2/signals/ns.other_sig",
                ),
            ],
        )

    def test_read_excel__signal_in_column_example_1(self):
        company1 = Entity(name="entityTypes/company/entities/ENT-1", display_name="ENT 1")
        company2 = Entity(name="entityTypes/company/entities/ENT-2", display_name="ENT 2")
        self.client.entity_api.create_entity(
            company1,
            "entityTypes/company",
        )
        self.client.entity_api.create_entity(
            company2,
            "entityTypes/company",
        )
        self.client.entity_api.search.entities_by_terms.return_value = [
            SearchEntitiesResponse.SearchResult(entities=[company1.to_proto()]),
            SearchEntitiesResponse.SearchResult(entities=[company2.to_proto()]),
        ]
        self.check_import(
            "./exabel_data_sdk/tests/resources/data/signal_in_column_example_1.xlsx",
            [
                pd.Series(
                    [1.2, 1.3, 1.4, 1.5],
                    pd.date_range("2022-10-10", periods=4, tz=tz.tzutc()),
                    name="entityTypes/company/entities/ENT-1/signals/ns.signal1",
                ),
                pd.Series(
                    [1.6, 1.7],
                    pd.date_range("2022-10-10", periods=2, tz=tz.tzutc()),
                    name="entityTypes/company/entities/ENT-2/signals/ns.signal1",
                ),
                pd.Series(
                    [9.1, 8.1, 7.1, 6.1, 5.1],
                    pd.date_range("2022-10-10", periods=5, tz=tz.tzutc()),
                    name="entityTypes/company/entities/ENT-1/signals/ns.signal2",
                ),
                pd.Series(
                    [1, 2],
                    pd.date_range("2022-10-10", periods=2, tz=tz.tzutc()),
                    name="entityTypes/company/entities/ENT-2/signals/ns.signal2",
                ),
            ],
        )

    def test_read_excel__signal_in_column_example_1__unmappable_entity(self):
        company1 = Entity(name="entityTypes/company/entities/ENT-1", display_name="ENT 1")
        self.client.entity_api.create_entity(
            company1,
            "entityTypes/company",
        )
        self.client.entity_api.search.entities_by_terms.return_value = [
            SearchEntitiesResponse.SearchResult(entities=[company1.to_proto()]),
        ]
        self.check_import(
            "./exabel_data_sdk/tests/resources/data/signal_in_column_example_1.xlsx",
            [
                pd.Series(
                    [1.2, 1.3, 1.4, 1.5],
                    pd.date_range("2022-10-10", periods=4, tz=tz.tzutc()),
                    name="entityTypes/company/entities/ENT-1/signals/ns.signal1",
                ),
                pd.Series(
                    [9.1, 8.1, 7.1, 6.1, 5.1],
                    pd.date_range("2022-10-10", periods=5, tz=tz.tzutc()),
                    name="entityTypes/company/entities/ENT-1/signals/ns.signal2",
                ),
            ],
        )

    def test_read_excel__signal_in_column_example_3__global_entity(self):
        self.check_import(
            "./exabel_data_sdk/tests/resources/data/signal_in_column_example_3.xlsx",
            [
                pd.Series(
                    [1.3, 1.4, 1.5, math.nan],
                    pd.date_range("2022-10-11", periods=4, tz=tz.tzutc()),
                    name="entityTypes/global/entities/global/signals/ns.signal1",
                ).dropna(),
                pd.Series(
                    [8.1, math.nan, 6.1, 5.1],
                    pd.date_range("2022-10-11", periods=4, tz=tz.tzutc()),
                    name="entityTypes/global/entities/global/signals/ns.signal2",
                ).dropna(),
            ],
        )

    def test_read_excel__signal_in_column_example_3__override_entity_type_should_fail(self):
        with self.assertRaises(SystemExit) as cm:
            self.check_import(
                "./exabel_data_sdk/tests/resources/data/signal_in_column_example_3.xlsx",
                entity_type="anything_should_fail",
            )
        self.assertEqual(cm.exception.code, 1)

    def test_read_excel__multiple_sheets_1(self):
        company1 = Entity(name="entityTypes/company/entities/ENT-1", display_name="ENT 1")
        company2 = Entity(name="entityTypes/company/entities/ENT-2", display_name="ENT 2")
        self.client.entity_api.create_entity(
            company1,
            "entityTypes/company",
        )
        self.client.entity_api.create_entity(
            company2,
            "entityTypes/company",
        )
        self.client.entity_api.search.entities_by_terms.return_value = [
            SearchEntitiesResponse.SearchResult(entities=[company1.to_proto()]),
            SearchEntitiesResponse.SearchResult(entities=[company2.to_proto()]),
        ]
        self.check_import(
            "./exabel_data_sdk/tests/resources/data/multiple_sheets_example_1.xlsx",
            [
                pd.Series(
                    [1.0, 1.1, 1.2, math.nan, 1.4],
                    pd.date_range("2022-10-10", periods=5, tz=tz.tzutc()),
                    name="entityTypes/company/entities/ENT-1/signals/ns.my_sig",
                ),
                pd.Series(
                    [40.1, 40.2],
                    pd.date_range("2022-10-10", periods=2, tz=tz.tzutc()),
                    name="entityTypes/company/entities/ENT-2/signals/ns.other_sig",
                ),
            ],
            [
                pd.Series(
                    [1.3, 1.4, 1.5],
                    pd.date_range("2022-05-11", periods=3, tz=tz.tzutc()),
                    name="entityTypes/brand/entities/ns.b1/signals/ns.signal1",
                ),
                pd.Series(
                    [8.1, 7.1, 6.1, 5.1],
                    pd.date_range("2022-05-11", periods=4, tz=tz.tzutc()),
                    name="entityTypes/brand/entities/ns.b1/signals/ns.signal2",
                ),
            ],
        )

    def test_read_excel__no_data_rows_1(self):
        self.check_import("./exabel_data_sdk/tests/resources/data/no_data_1.xlsx", [])
        result = self.client.signal_api.list_signals()
        self.assertCountEqual(
            ["signals/ns.signal1", "signals/ns.signal2"], [s.name for s in result]
        )

    def test_read_excel__no_data_rows_2(self):
        self.check_import("./exabel_data_sdk/tests/resources/data/no_data_2.xlsx", [])
        result = self.client.signal_api.list_signals()
        self.assertCountEqual(
            ["signals/ns.signal1", "signals/ns.signal2"], [s.name for s in result]
        )

    def test_read_excel__no_data_rows_3(self):
        self.check_import("./exabel_data_sdk/tests/resources/data/no_data_3.xlsx", [])
        result = self.client.signal_api.list_signals()
        self.assertCountEqual(
            ["signals/ns.signal1", "signals/ns.signal2"], [s.name for s in result]
        )

    def test_read_excel__no_data_rows_4(self):
        self.check_import("./exabel_data_sdk/tests/resources/data/no_data_4.xlsx", [])
        result = self.client.signal_api.list_signals()
        self.assertEqual(0, result.total_size)


if __name__ == "__main__":
    unittest.main()
