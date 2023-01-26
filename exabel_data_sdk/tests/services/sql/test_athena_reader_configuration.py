import argparse
import unittest

from exabel_data_sdk.services.sql.athena_reader_configuration import (
    AthenaReaderConfiguration,
    AwsAccessKeyId,
    AwsSecretAccessKey,
    Catalog,
    Region,
    S3StagingDir,
    Schema,
    Workgroup,
)


class TestAthenaReaderConfiguration(unittest.TestCase):
    def setUp(self) -> None:
        self.config_minimal = AthenaReaderConfiguration(
            region=Region("region"),
            s3_staging_dir=S3StagingDir("staging/dir"),
        )
        self.config = AthenaReaderConfiguration(
            region=Region("region"),
            s3_staging_dir=S3StagingDir("staging/dir"),
            workgroup=Workgroup("workgroup"),
            catalog=Catalog("catalog"),
            schema=Schema("schema"),
            aws_access_key_id=AwsAccessKeyId("aws_access_key_id"),
            aws_secret_access_key=AwsSecretAccessKey("aws_secret_access_key"),
        )

    def test_athena_reader_configuration__key_without_secret_should_fail(self):
        with self.assertRaises(ValueError):
            AthenaReaderConfiguration(
                region="region",
                s3_staging_dir="staging/dir",
                aws_access_key_id="key",
            )

    def test_athena_reader_configuration__secret_without_key_should_fail(self):
        with self.assertRaises(ValueError):
            AthenaReaderConfiguration(
                region="region",
                s3_staging_dir="staging/dir",
                aws_secret_access_key="secret",
            )

    def test_athena_reader_configuration__key_and_profile_should_fail(self):
        with self.assertRaises(ValueError):
            AthenaReaderConfiguration(
                region="region",
                s3_staging_dir="staging/dir",
                aws_access_key_id="key",
                profile="profile",
            )

    def test_from_args(self):
        args = argparse.Namespace(
            region="region",
            s3_staging_dir="staging/dir",
            workgroup="workgroup",
            catalog="catalog",
            schema="schema",
            aws_access_key_id="aws_access_key_id",
            aws_secret_access_key="aws_secret_access_key",
            profile=None,
        )
        athena_reader_configuration = AthenaReaderConfiguration.from_args(args)
        self.assertEqual(
            self.config,
            athena_reader_configuration,
        )

    def test_from_args__missing_arg(self):
        args = argparse.Namespace()
        with self.assertRaises(AttributeError):
            AthenaReaderConfiguration.from_args(args)

    def test_get_connection_string(self):
        self.assertSequenceEqual(
            "awsathena+arrow://"
            "aws_access_key_id:aws_secret_access_key@athena.region.amazonaws.com:443/schema"
            "?unload=true&s3_staging_dir=staging%2Fdir&work_group=workgroup&catalog_name=catalog",
            self.config.get_connection_string(),
        )

    def test_get_connection_string__minimal(self):
        self.assertEqual(
            "awsathena+arrow://:@athena.region.amazonaws.com:443/?unload=true"
            "&s3_staging_dir=staging%2Fdir",
            self.config_minimal.get_connection_string(),
        )

    def test_get_connection_string__with_profile(self):
        config = AthenaReaderConfiguration(
            region="region", s3_staging_dir="staging/dir", profile="profile"
        )
        self.assertEqual(
            "awsathena+arrow://:@athena.region.amazonaws.com:443/?unload=true"
            "&s3_staging_dir=staging%2Fdir&profile_name=profile",
            config.get_connection_string(),
        )
