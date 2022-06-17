import abc
from typing import Sequence, Type

from exabel_data_sdk.scripts.command_line_script import CommandLineScript
from exabel_data_sdk.services.sql.sql_reader import SqlReader
from exabel_data_sdk.services.sql.sql_reader_configuration import SqlReaderConfiguration


class SqlScript(CommandLineScript, abc.ABC):
    """
    Base class for scripts that perform a query against a SQL database and optionally store the
    result to a file.
    """

    def __init__(
        self,
        argv: Sequence[str],
        description: str,
        reader_configuration_class: Type[SqlReaderConfiguration],
    ):
        super().__init__(argv, description)
        self.reader_configuration_class = reader_configuration_class
        self.parser.add_argument(
            "--query",
            required=True,
            help="The query to execute.",
        )
        self.parser.add_argument(
            "--output-file",
            help=(
                "The file to write the result to. If no output file is specified, a sample is "
                "printed."
            ),
        )

    def run(self) -> None:
        args = self.parse_arguments()
        self.setup_logging()
        configuration = self.reader_configuration_class.from_args(args)
        reader = SqlReader(configuration.get_connection_string())
        reader.read_sql_query_and_write_result(args.query, args.output_file)
