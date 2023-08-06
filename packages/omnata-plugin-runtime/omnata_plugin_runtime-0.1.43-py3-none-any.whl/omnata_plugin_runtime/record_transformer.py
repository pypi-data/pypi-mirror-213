
from typing import Dict, List
from pydantic import parse_obj_as # pylint:disable=no-name-in-module
from logging import getLogger
from .configuration import StoredConfigurationValue, StoredMappingValue, StoredFieldMapping
logger = getLogger(__name__)

class RecordTransformerResult(dict):
    """
    The result of transforming an individual record
    """
    def __init__(self, success:bool,errors:List[str] = None,transformed_record:dict = None):
        """
        Constructs a RecordTransformerResult
        """
        if success:
            dict.__init__(self, success=success,transformed_record=transformed_record)
        else:
            dict.__init__(self, success=success,errors=errors)

class RecordTransformer():
    """
    The default record transformer, used to convert Snowflake records into an app-specific representation
    using the configured field mappings, and optionally perform data validation so that source failures occur
    """
    def transform_record(self,source_metadata:dict,sync_parameters:Dict[str, StoredConfigurationValue],field_mappings:StoredMappingValue,source_record:dict) -> RecordTransformerResult:
        """
        Default transformer.
        When the visual field mapper is used, simply picks out the columns and renames them.
        When the jinja mapper is used, copies the template into the output
        """
        transformed_record = {}
        errors = []
        if field_mappings.mapper_type == 'jinja_template':
            transformed_record['jinja_template'] = field_mappings.jinja_template
            transformed_record['source_record'] = source_record
        elif field_mappings.mapper_type == 'field_mapping_selector':
            parsed_field_mappings:List[StoredFieldMapping] = parse_obj_as(List[StoredFieldMapping],field_mappings.field_mappings)
            for field_mapping in parsed_field_mappings:
                if field_mapping.source_column not in source_record:
                    errors.append(f"Column '{field_mapping.source_column}' not found in record")
                else:
                    transformed_record[field_mapping.app_field] = source_record[field_mapping.source_column]
        else:
            errors.append(f"Unrecognised mapper type: {field_mappings.mapper_type}")
        logger.debug(f"Transformed record: {transformed_record}")
        if len(errors) > 0:
            logger.info(f"Record transformer errors: {errors}")
            return dict(RecordTransformerResult(success=False, errors=errors))
        return dict(RecordTransformerResult(success=True, transformed_record=transformed_record))
