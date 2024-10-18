import argparse
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from typing import Sequence

from tqdm import tqdm

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.request_error import RequestError
from exabel_data_sdk.scripts.list_time_series import ListTimeSeries
from exabel_data_sdk.scripts.utils import (
    ERROR,
    MAX_WORKERS,
    PAGE_SIZE,
    SUCCESS,
    conditional_progress_bar,
)


class DeleteTimeSeries(ListTimeSeries):
    """
    Deletes all time series for a signal, entity type or entity, or a combination of these.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--dry-run",
            required=False,
            action="store_true",
            default=False,
            help="Only print to console instead of deleting",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        all_time_series = self._list_time_series(
            client,
            entity=args.entity,
            signal=args.signal,
            entity_type=args.entity_type,
            show_progress=args.show_progress,
        )

        if not all_time_series:
            print("No time series to delete.")
            return

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

                if args.dry_run:
                    for time_series in batch:
                        tqdm.write(f"Delete: {time_series}")
                    num_deleted += len(batch)
                    continue

                api_results = executor.map(delete_time_series, batch)
                api_results_counter = Counter(api_results)
                num_deleted += api_results_counter[SUCCESS]
                num_failed += api_results_counter[ERROR]

        if args.dry_run:
            print(f"Would have deleted {num_deleted} time series.")
            return
        print(f"Successfully deleted {num_deleted} time series.")
        if num_failed > 0:
            print(f"Failed to delete {num_failed} time series.")


if __name__ == "__main__":
    DeleteTimeSeries(
        sys.argv,
        "Deletes all time series for a signal, entity type or entity, or a combination of these.",
    ).run()
