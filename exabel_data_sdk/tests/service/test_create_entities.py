import argparse
import sys
from collections import defaultdict
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.service.import_service import CsvImportService
from exabel_data_sdk.service.import_service import ResourceCreationStatus
from exabel_data_sdk.scripts.base_script import BaseScript

class LoadEntities(BaseScript):
  """
  Run this with :

  python -m test_create_entities
  --api-key <api-key>
  --filename <input.csv>
  """

  def __init__(self, argv: Sequence[str], description: str):
    super().__init__(argv, description)
    self.parser.add_argument("--filename", type=str, required=True, help="Input filename")
    self.parser.add_argument(
        "--sep",
        required=False,
        type=str,
        default=';',
        help="Separator used in input file, defaults to ';'"
    )

  def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
    service = CsvImportService(client)
    result = service.create_entities_from_csv(args.filename, args.sep)
    result_stats = {}
    for key, value in result.items():
      if value.status.name in result_stats:
        result_stats[value.status.name].append(key)
      else:
        result_stats[value.status.name] = [key]

    if ResourceCreationStatus.CREATED.name in result_stats and len(result_stats[ResourceCreationStatus.CREATED.name]) == len(result.items()):
      print(f"All entities uploaded")
    else:
      if ResourceCreationStatus.FAILED.name in result_stats:
        print(f"FAILED: {result_stats[ResourceCreationStatus.FAILED.name]}")
      if ResourceCreationStatus.EXISTS.name in result_stats:
        print(f"EXISTS: {result_stats[ResourceCreationStatus.EXISTS.name]}")

if __name__ == "__main__":
  LoadEntities(sys.argv, "Load entities").run()