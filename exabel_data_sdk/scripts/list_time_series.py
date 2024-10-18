import argparse
import sys
from math import ceil
from typing import List, Optional, Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.client.api.data_classes.paging_result import PagingResult
from exabel_data_sdk.scripts import utils
from exabel_data_sdk.scripts.base_script import BaseScript
from exabel_data_sdk.scripts.utils import PAGE_SIZE, conditional_progress_bar


class ListTimeSeries(BaseScript):
    """
    Lists all time series.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--signal",
            required=False,
            type=utils.signal_resource_name,
            help="The resource name of a signal, for example 'signals/ns.signalIdentifier'",
        )
        self.parser.add_argument(
            "--entity",
            required=False,
            type=utils.entity_resource_name,
            help=(
                "The resource name of an entity, "
                "for example 'entityTypes/ns.brand/entities/ns.identifier'"
            ),
        )
        self.parser.add_argument(
            "--entity-type",
            required=False,
            type=utils.entity_type_resource_name,
            help="The resource name of an entity type, for example 'entityTypes/ns.brand'",
        )
        self.parser.add_argument(
            "--show-progress",
            required=False,
            action="store_true",
            default=False,
            help="Show progress bar",
        )

    def _filter_ts_list(
        self, ts_list: Sequence[str], ts_filter: Optional[str] = None
    ) -> Sequence[str]:
        if ts_filter:
            return [ts for ts in ts_list if ts_filter in ts]
        return ts_list

    def _list_time_series(
        self,
        client: ExabelClient,
        entity: Optional[str] = None,
        signal: Optional[str] = None,
        entity_type: Optional[str] = None,
        show_progress: bool = False,
    ) -> Sequence[str]:
        if (signal is None) == (entity is None) == (entity_type is None):
            raise ValueError(
                "Specify either: signal and entity type, or signal and entity, or "
                "only signal, entity-type or entity, but not all three."
            )

        all_time_series: List[str] = []
        all_entities: List[Entity] = []

        if entity:
            if signal:
                all_time_series.append(f"{entity}/{signal}")
            else:
                all_entities.append(Entity(name=entity, display_name=entity))

        elif signal:
            page_token = None
            result: PagingResult[str] = client.time_series_api.get_signal_time_series(
                signal, page_size=PAGE_SIZE, page_token=page_token
            )
            num_time_series = result.total_size
            if not num_time_series:
                print("No time series found")
                return []

            print(f"Total number of time series for given signal: {num_time_series}")
            print(f"Fetching time series in pages of size {PAGE_SIZE}...")
            for _ in conditional_progress_bar(
                range(1, ceil(num_time_series / PAGE_SIZE) + 1),
                desc="Fetching time series: ",
                show_progress=show_progress,
                initial=1,
            ):
                all_time_series.extend(self._filter_ts_list(result.results, entity_type))
                if len(result.results) < PAGE_SIZE:
                    break
                result = client.time_series_api.get_signal_time_series(
                    signal, page_size=PAGE_SIZE, page_token=result.next_page_token
                )

        elif entity_type:
            page_token = None
            entities_result: PagingResult[Entity] = client.entity_api.list_entities(
                entity_type, page_size=PAGE_SIZE, page_token=page_token
            )
            num_entities = entities_result.total_size
            if not num_entities:
                print("No entities found")
                return []

            print(f"Total number of entities for given entity type: {num_entities}")
            print(f"Fetching entities in pages of size {PAGE_SIZE}...")

            for _ in conditional_progress_bar(
                range(1, ceil(num_entities / PAGE_SIZE) + 1),
                desc="Fetching entities: ",
                show_progress=show_progress,
                initial=1,
            ):
                all_entities.extend(entities_result.results)
                if len(entities_result.results) < PAGE_SIZE:
                    break
                entities_result = client.entity_api.list_entities(
                    entity_type, page_size=PAGE_SIZE, page_token=entities_result.next_page_token
                )

        if all_entities and not all_time_series:
            for item in conditional_progress_bar(
                all_entities, desc="Fetching time series: ", show_progress=show_progress
            ):
                page_token = None
                while True:
                    result = client.time_series_api.get_entity_time_series(
                        item.name, page_size=PAGE_SIZE, page_token=page_token
                    )
                    all_time_series.extend(self._filter_ts_list(result.results, signal))
                    page_token = result.next_page_token
                    if len(result.results) < PAGE_SIZE:
                        break

        return all_time_series

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        all_time_series = self._list_time_series(
            client,
            entity=args.entity,
            signal=args.signal,
            entity_type=args.entity_type,
            show_progress=args.show_progress,
        )

        for time_series in all_time_series:
            print(time_series)

        print(f"Found {len(all_time_series)} time series")


if __name__ == "__main__":
    ListTimeSeries(sys.argv, "Lists time series.").run()
