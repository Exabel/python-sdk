import argparse
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from math import ceil
from typing import List, Sequence

from tqdm import tqdm

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.client.api.data_classes.paging_result import PagingResult
from exabel_data_sdk.client.api.data_classes.request_error import RequestError
from exabel_data_sdk.scripts.base_script import BaseScript
from exabel_data_sdk.scripts.utils import (
    ERROR,
    MAX_WORKERS,
    PAGE_SIZE,
    SUCCESS,
    conditional_progress_bar,
)


class DeleteTimeSeries(BaseScript):
    """
    Deletes all time series for a signal, entity type or entity, or a combination of these.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--signal",
            required=False,
            type=str,
            help="The signal, for example 'signals/ns.signalIdentifier'",
        )
        self.parser.add_argument(
            "--entity",
            required=False,
            type=str,
            help=("The entity, for example 'entityTypes/ns.entityType/entities/ns.identifier'"),
        )
        self.parser.add_argument(
            "--entity-type",
            required=False,
            type=str,
            help="The entity type, for example 'entityTypes/ns.entityType'",
        )
        self.parser.add_argument(
            "--dry-run",
            required=False,
            action="store_true",
            default=False,
            help="Only print to console instead of deleting",
        )
        self.parser.add_argument(
            "--show-progress",
            required=False,
            action="store_true",
            default=False,
            help="Show progress bar",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        if (args.signal is None) == (args.entity is None) == (args.entity_type is None):
            raise ValueError(
                "Specify either: signal and entity type, or signal and entity, or "
                "only signal, entity-type or entity, but not all three."
            )

        all_time_series: List[str] = []
        all_entities: List[str] = []

        if args.entity_type is not None:
            if not args.entity_type.startswith("entityTypes/"):
                args.entity_type = f"entityTypes/{args.entity_type}"
            print(f"Deleting time series for entity type: {args.entity_type}")

        if args.entity is not None:
            if not args.entity.startswith("entityTypes/"):
                args.entity = f"entityTypes/{args.entity}"
            if args.signal is not None:
                if not args.signal.startswith("signals/"):
                    args.signal = f"signals/{args.signal}"
                ts = f"{args.entity}/{args.signal}"
                all_time_series.append(ts)
                print(f"Deleting time series: {ts}")
            else:
                all_entities.append(args.entity)
                print(f"Deleting time series for entity: {args.entity}")

        elif args.signal is not None:
            if not args.signal.startswith("signals/"):
                args.signal = f"signals/{args.signal}"
            print(f"Deleting time series for signal: {args.signal}")

            page_token = None
            result: PagingResult[str] = client.time_series_api.get_signal_time_series(
                args.signal, page_size=PAGE_SIZE, page_token=page_token
            )
            num_time_series = result.total_size
            if not num_time_series:
                print("No time series found")
                return

            print(f"Total number of time series for given signal: {num_time_series}")
            print(f"Fetching time series in pages of size {PAGE_SIZE}...")

            for _ in conditional_progress_bar(
                range(1, ceil(num_time_series / PAGE_SIZE) + 1),
                desc="Fetching time series: ",
                show_progress=args.show_progress,
                initial=1,
            ):
                if args.entity_type is not None:
                    result.results = [
                        time_series
                        for time_series in result.results
                        if args.entity_type in time_series
                    ]
                all_time_series.extend(result.results)
                page_token = result.next_page_token
                if page_token is None or len(all_time_series) == num_time_series:
                    break
                result = client.time_series_api.get_signal_time_series(
                    args.signal, page_size=PAGE_SIZE, page_token=page_token
                )

        elif args.entity_type is not None:
            page_token = None
            entities_result: PagingResult[Entity] = client.entity_api.list_entities(
                args.entity_type, page_size=PAGE_SIZE, page_token=page_token
            )
            num_entities = entities_result.total_size
            if not num_entities:
                print("No entities found")
                return

            print(f"Total number of entities for given entity type: {num_entities}")
            print(f"Fetching entities in pages of size {PAGE_SIZE}...")

            for _ in conditional_progress_bar(
                range(1, ceil(num_entities / PAGE_SIZE) + 1),
                desc="Fetching entities: ",
                show_progress=args.show_progress,
                initial=1,
            ):
                entity_names = [entity.name for entity in entities_result.results]
                all_entities.extend(entity_names)
                page_token = entities_result.next_page_token
                if page_token is None or len(all_entities) == num_entities:
                    break
                entities_result = client.entity_api.list_entities(
                    args.entity_type, page_size=PAGE_SIZE, page_token=page_token
                )

        if all_entities and not all_time_series:
            for entity in conditional_progress_bar(
                all_entities, desc="Fetching time series: ", show_progress=args.show_progress
            ):
                page_token = None
                while True:
                    result = client.time_series_api.get_entity_time_series(
                        entity, page_size=PAGE_SIZE, page_token=page_token
                    )
                    if args.signal is not None:
                        result.results = [
                            time_series
                            for time_series in result.results
                            if args.signal in time_series
                        ]
                    all_time_series.extend(result.results)
                    page_token = result.next_page_token
                    if len(all_time_series) == result.total_size or len(result.results) == 0:
                        break

        if all_time_series:
            num_time_series = len(all_time_series)
            print(f"Number of time series to delete: {num_time_series}")
            num_deleted = num_failed = 0

            def delete_time_series(time_series: str) -> int:
                try:
                    client.time_series_api.delete_time_series(time_series)
                    return SUCCESS
                except RequestError as e:
                    tqdm.write(f"Failed to delete: {time_series} / {e.error_type}")
                    return ERROR

            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                for i in conditional_progress_bar(
                    range(0, num_time_series, PAGE_SIZE),
                    desc="Deleting time series: ",
                    show_progress=args.show_progress,
                ):
                    batch = (
                        all_time_series[i : i + PAGE_SIZE]
                        if i + PAGE_SIZE < num_time_series
                        else all_time_series[i:]
                    )

                    if not args.dry_run:
                        api_results = executor.map(delete_time_series, batch)
                        api_results_counter = Counter(api_results)
                        num_deleted += api_results_counter[SUCCESS]
                        num_failed += api_results_counter[ERROR]
                    else:
                        for time_series in batch:
                            tqdm.write(f"Delete: {time_series}")
                        num_deleted += len(batch)

            if args.dry_run:
                print(f"Would have deleted {num_deleted} time series.")
            else:
                print(f"Successfully deleted {num_deleted} time series.")
                if num_failed > 0:
                    print(f"Failed to delete {num_failed} time series.")
        else:
            print("No time series to delete.")


if __name__ == "__main__":
    DeleteTimeSeries(
        sys.argv,
        "Deletes all time series for a signal, entity type or entity, or a combination of these.",
    ).run()
