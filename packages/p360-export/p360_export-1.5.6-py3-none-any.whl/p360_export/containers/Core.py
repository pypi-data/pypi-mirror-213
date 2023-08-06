from pyspark.sql import SparkSession

from dependency_injector import containers, providers
from p360_export.data.DataPicker import DataPicker

from p360_export.data.ColumnMappingGetter import ColumnMappingGetter
from p360_export.data.build.FeatureStoreDataBuilder import FeatureStoreDataBuilder
from p360_export.data.type.resolve.DataFrameTypeResolver import DataFrameTypeResolver
from p360_export.data.type.validate.EmailValidator import EmailValidator
from p360_export.data.type.validate.PhoneNumberValidator import PhoneNumberValidator
from p360_export.export.AudienceNameGetter import AudienceNameGetter
from p360_export.query.QueryBuilder import QueryBuilder
from p360_export.utils.ColumnHasher import ColumnHasher
from p360_export.utils.ColumnSampleGetter import ColumnSampleGetter
from p360_export.utils.secret_getters.DbutilsSecretsSecretGetter import DbutilsSecretsSecretGetter
from p360_export.utils.secret_getters.EnvVariableSecretGetter import EnvVariableSecretGetter
from p360_export.utils.utils import resolve_dbutils


class Core(containers.DeclarativeContainer):
    __self__ = providers.Self()
    config = providers.Configuration()

    spark = providers.Object(SparkSession.getActiveSession())
    dbutils = providers.Object(resolve_dbutils())

    query_builder = providers.Singleton(QueryBuilder, config=config)
    data_builder = providers.Singleton(FeatureStoreDataBuilder, config=config, spark=spark)
    data_picker = providers.Singleton(DataPicker, spark=spark)

    column_mapping_getter = providers.Singleton(ColumnMappingGetter, config=config)
    dataframe_type_resolver = providers.Singleton(DataFrameTypeResolver)

    # Validators
    email_validator = providers.Singleton(EmailValidator)
    phone_number_validator = providers.Singleton(
        PhoneNumberValidator,
        min_phone_number_digit_count=config.p360_export.data.type.validate.min_phone_number_digit_count,
        max_phone_number_digit_count=config.p360_export.data.type.validate.max_phone_number_digit_count,
        phone_number_regex=config.p360_export.data.type.validate.phone_number_regex,
    )

    # Utils
    column_hasher = providers.Singleton(ColumnHasher)
    column_sample_getter = providers.Singleton(ColumnSampleGetter)
    audience_name_getter = providers.Singleton(AudienceNameGetter, config=config)

    # Secret getter
    env_variable_secret_getter = providers.Singleton(EnvVariableSecretGetter)
    dbutils_secret_getter = providers.Singleton(
        DbutilsSecretsSecretGetter, dbutils=dbutils, scope=config.p360_export.config.dbutils_secrets_scope
    )
    secret_getter = providers.Selector(
        config.p360_export.config.secret_getter,
        dbutils_secrets=dbutils_secret_getter,
        env_variable=env_variable_secret_getter,
    )
