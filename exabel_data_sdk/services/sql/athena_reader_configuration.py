import argparse
import urllib.parse
from dataclasses import dataclass
from typing import MutableMapping, NewType, Optional

from exabel_data_sdk.services.sql.sql_reader_configuration import (
    ConnectionString,
    SqlReaderConfiguration,
)

Region = NewType("Region", str)
S3StagingDir = NewType("S3StagingDir", str)
Workgroup = NewType("Workgroup", str)
Catalog = NewType("Catalog", str)
Schema = NewType("Schema", str)
AwsAccessKeyId = NewType("AwsAccessKeyId", str)
AwsSecretAccessKey = NewType("AwsSecretAccessKey", str)
Profile = NewType("Profile", str)


_BASE_CONNECTION_STRING = (
    "awsathena+arrow://{aws_access_key_id}:{aws_secret_access_key}"
    "@athena.{region_name}.amazonaws.com:443/{schema_name}"
)


def _get_base_connection_string(
    aws_access_key_id: str,
    aws_secret_access_key: str,
    region_name: str,
    schema_name: str,
) -> str:
    return _BASE_CONNECTION_STRING.format(
        region_name=region_name,
        schema_name=schema_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )


@dataclass
class AthenaReaderConfiguration(SqlReaderConfiguration):
    """SQL configuration for Athena."""

    region: Region
    s3_staging_dir: S3StagingDir
    workgroup: Optional[Workgroup] = None
    catalog: Optional[Catalog] = None
    schema: Optional[Schema] = None
    aws_access_key_id: Optional[AwsAccessKeyId] = None
    aws_secret_access_key: Optional[AwsSecretAccessKey] = None
    profile: Optional[Profile] = None

    def __post_init__(self) -> None:
        if self.profile is not None and (
            (self.aws_access_key_id or self.aws_secret_access_key) is not None
        ):
            raise ValueError(
                "profile and aws_access_key_id/aws_secret_access_key cannot both be set"
            )
        if self.aws_access_key_id is None and self.aws_secret_access_key is not None:
            raise ValueError(
                "aws_access_key_id must be provided if aws_secret_access_key is provided"
            )
        if self.aws_access_key_id is not None and self.aws_secret_access_key is None:
            raise ValueError(
                "aws_secret_access_key must be provided if aws_access_key_id is provided"
            )

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> "AthenaReaderConfiguration":
        return cls(
            region=args.region,
            s3_staging_dir=args.s3_staging_dir,
            workgroup=args.workgroup,
            catalog=args.catalog,
            schema=args.schema,
            aws_access_key_id=args.aws_access_key_id,
            aws_secret_access_key=args.aws_secret_access_key,
            profile=args.profile,
        )

    def get_connection_string(self) -> ConnectionString:
        """Return the connection string."""
        params: MutableMapping[str, str] = {"unload": "true", "s3_staging_dir": self.s3_staging_dir}
        if self.workgroup is not None:
            params["work_group"] = self.workgroup
        if self.catalog is not None:
            params["catalog_name"] = self.catalog
        if self.profile is not None:
            params["profile_name"] = self.profile
        connection_string = _get_base_connection_string(
            aws_access_key_id=self.aws_access_key_id or "",
            aws_secret_access_key=self.aws_secret_access_key or "",
            region_name=self.region,
            schema_name=self.schema or "",
        ) + (f"?{urllib.parse.urlencode(params)}" if params else "")
        return ConnectionString(connection_string)
