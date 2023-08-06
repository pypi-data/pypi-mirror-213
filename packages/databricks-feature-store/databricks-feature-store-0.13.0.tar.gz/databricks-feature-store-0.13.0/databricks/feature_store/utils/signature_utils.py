import logging
from typing import Dict, Optional

import mlflow
from mlflow.models import ModelSignature
from mlflow.types import ColSpec
from mlflow.types import DataType as MlflowDataType
from mlflow.types import Schema

from databricks.feature_store.entities.feature_column_info import FeatureColumnInfo
from databricks.feature_store.entities.feature_spec import FeatureSpec
from databricks.feature_store.entities.on_demand_column_info import OnDemandColumnInfo
from databricks.feature_store.entities.source_data_column_info import (
    SourceDataColumnInfo,
)

_logger = logging.getLogger(__name__)

# These types are unsupported due to MLflow signatures lacking any equivalent types.
# We thus cannot construct a ColSpec for any column that uses these types.
UNSUPPORTED_SPARK_TYPE_PREFIXES = ["array", "decimal", "map"]
# All supported feature store types must be either in this map or in
# UNSUPPORTED_SPARK_TYPE_PREFIXES
TYPE_MAP = {
    "smallint": MlflowDataType.integer,  # Upcast to integer
    "int": MlflowDataType.integer,
    "bigint": MlflowDataType.long,
    "float": MlflowDataType.float,
    "double": MlflowDataType.double,
    "boolean": MlflowDataType.boolean,
    "date": MlflowDataType.datetime,
    "timestamp": MlflowDataType.datetime,
    "string": MlflowDataType.string,
    "binary": MlflowDataType.binary,
}


def is_unsupported_type(type_str: str):
    return any(
        [type_str.startswith(prefix) for prefix in UNSUPPORTED_SPARK_TYPE_PREFIXES]
    )


def convert_spark_data_type_to_mlflow_signature_type(spark_type):
    """
    Maps Databricks SQL types to MLflow signature types.
    docs.databricks.com/sql/language-manual/sql-ref-datatypes.html#language-mappings
    """
    return TYPE_MAP.get(spark_type)


def get_input_schema_from_feature_spec(feature_spec: FeatureSpec) -> Optional[Schema]:
    """
    Produces an MLflow signature schema from a feature spec.
    Source data columns are marked as required inputs and feature columns
    (both lookups and on-demand features) are marked as optional inputs.

    :param feature_spec: FeatureSpec object with datatypes for each column.
    """
    # If we're missing any data types for any column, we are likely dealing with a
    # malformed feature spec and should halt signature construction.
    if any([ci.data_type is None for ci in feature_spec.column_infos]):
        _logger.warning(
            "The model could not be logged with an MLflow signature because the "
            "training set does not contain column data types."
        )
        return None

    source_data_cols = [
        ci
        for ci in feature_spec.column_infos
        if isinstance(ci.info, SourceDataColumnInfo)
    ]
    # Don't create signature if any source data columns (required) are of complex types.
    if any(
        [
            ci.data_type is None or is_unsupported_type(ci.data_type)
            for ci in source_data_cols
        ]
    ):
        _logger.warning(
            "Model was not logged with a signature because the input DataFrame"
            " contains column data types not supported by MLflow model signatures."
        )
        return None
    required_input_colspecs = [
        ColSpec(
            convert_spark_data_type_to_mlflow_signature_type(ci.data_type),
            ci.info.output_name,
            optional=False,
        )
        for ci in source_data_cols
    ]
    feature_cols = [
        ci
        for ci in feature_spec.column_infos
        if isinstance(ci.info, (FeatureColumnInfo, OnDemandColumnInfo))
    ]
    unsupported_feature_cols = [
        ci for ci in feature_cols if is_unsupported_type(ci.data_type)
    ]
    optional_input_colspecs = [
        ColSpec(
            convert_spark_data_type_to_mlflow_signature_type(ci.data_type),
            ci.output_name,
            optional=True,
        )
        for ci in feature_cols
        if not is_unsupported_type(ci.data_type)
    ]
    if unsupported_feature_cols:
        feat_string = ", ".join(
            [f"{ci.output_name} ({ci.data_type})" for ci in unsupported_feature_cols]
        )
        _logger.warning(
            f"The following features will not be included in the model signature because their"
            f" data types are not supported by MLflow model signatures: {feat_string}"
        )
    return Schema(required_input_colspecs + optional_input_colspecs)


def get_output_schema_from_labels(label_type_map: Optional[Dict[str, str]]) -> Schema:
    """
    Produces an MLflow signature schema from the provided label type map.
    :param label_type_map: Map label column name -> data type
    """
    if not label_type_map:
        _logger.warning(
            "The auto-generated model signature will not include an output schema"
            " because the training set did not contain a label."
        )
        return None
    if any([is_unsupported_type(dtype) for dtype in label_type_map.values()]):
        _logger.warning(
            "The auto-generated model signature will not include output schema because the labels are"
            "of data types not supported by MLflow model signatures."
        )
        return None
    else:
        output_colspecs = [
            ColSpec(
                convert_spark_data_type_to_mlflow_signature_type(spark_type),
                col_name,
                optional=False,
            )
            for col_name, spark_type in label_type_map.items()
        ]
        return Schema(output_colspecs)


def get_mlflow_signature_from_feature_spec(
    feature_spec: FeatureSpec,
    label_type_map: Optional[Dict[str, str]],
    override_output_schema: Optional[Schema],
) -> Optional[ModelSignature]:
    """
    Produce an MLflow signature from a feature spec and label type map.
    Source data columns are marked as required inputs and feature columns
    (both lookups and on-demand features) are marked as optional inputs.

    Reads output types from the cached label -> datatype map in the training set.
    If override_output_schema is provided, it will always be used as the output schema.

    :param feature_spec: FeatureSpec object with datatypes for each column.
    :param label_type_map: Map of label column name -> datatype
    :param override_output_schema: User-provided output schema to use if provided.
    """
    input_schema = get_input_schema_from_feature_spec(feature_spec)
    if not input_schema:
        return None
    output_schema = get_output_schema_from_labels(label_type_map)
    return mlflow.models.ModelSignature(
        inputs=input_schema,
        outputs=override_output_schema or output_schema,
    )
