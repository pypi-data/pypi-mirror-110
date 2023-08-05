from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import ArrayType
from pyspark.sql.types import BooleanType
from pyspark.sql.types import DataType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class ProcessRequestSchema:
    """
    This resource provides the target, request and response, and action details
    for an action to be performed by the target on or about existing resources.
    """

    # noinspection PyDefaultArgument
    @staticmethod
    def get_schema(
        max_nesting_depth: Optional[int] = 6,
        nesting_depth: int = 0,
        nesting_list: List[str] = [],
        max_recursion_limit: Optional[int] = 2,
        include_extension: Optional[bool] = False,
    ) -> Union[StructType, DataType]:
        """
        This resource provides the target, request and response, and action details
        for an action to be performed by the target on or about existing resources.


        resourceType: This is a ProcessRequest resource

        identifier: The ProcessRequest business identifier.

        status: The status of the resource instance.

        action: The type of processing action being requested, for example Reversal,
            Readjudication, StatusRequest,PendedRequest.

        target: The organization which is the target of the request.

        created: The date when this resource was created.

        provider: The practitioner who is responsible for the action specified in this request.

        organization: The organization which is responsible for the action speccified in this
            request.

        request: Reference of resource which is the target or subject of this action.

        response: Reference of a prior response to resource which is the target or subject of
            this action.

        nullify: If true remove all history excluding audit.

        reference: A reference to supply which authenticates the process.

        item: List of top level items to be re-adjudicated, if none specified then the
            entire submission is re-adjudicated.

        include: Names of resource types to include.

        exclude: Names of resource types to exclude.

        period: A period of time during which the fulfilling resources would have been
            created.

        """
        from spark_fhir_schemas.stu3.complex_types.identifier import IdentifierSchema
        from spark_fhir_schemas.stu3.complex_types.reference import ReferenceSchema
        from spark_fhir_schemas.stu3.complex_types.processrequest_item import (
            ProcessRequest_ItemSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.period import PeriodSchema

        if (
            max_recursion_limit
            and nesting_list.count("ProcessRequest") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["ProcessRequest"]
        schema = StructType(
            [
                # This is a ProcessRequest resource
                StructField("resourceType", StringType(), True),
                # The ProcessRequest business identifier.
                StructField(
                    "identifier",
                    ArrayType(
                        IdentifierSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                        )
                    ),
                    True,
                ),
                # The status of the resource instance.
                StructField("status", StringType(), True),
                # The type of processing action being requested, for example Reversal,
                # Readjudication, StatusRequest,PendedRequest.
                StructField("action", StringType(), True),
                # The organization which is the target of the request.
                StructField(
                    "target",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # The date when this resource was created.
                StructField("created", StringType(), True),
                # The practitioner who is responsible for the action specified in this request.
                StructField(
                    "provider",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # The organization which is responsible for the action speccified in this
                # request.
                StructField(
                    "organization",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # Reference of resource which is the target or subject of this action.
                StructField(
                    "request",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # Reference of a prior response to resource which is the target or subject of
                # this action.
                StructField(
                    "response",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
                # If true remove all history excluding audit.
                StructField("nullify", BooleanType(), True),
                # A reference to supply which authenticates the process.
                StructField("reference", StringType(), True),
                # List of top level items to be re-adjudicated, if none specified then the
                # entire submission is re-adjudicated.
                StructField(
                    "item",
                    ArrayType(
                        ProcessRequest_ItemSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                        )
                    ),
                    True,
                ),
                # Names of resource types to include.
                # Names of resource types to exclude.
                # A period of time during which the fulfilling resources would have been
                # created.
                StructField(
                    "period",
                    PeriodSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension,
                    ),
                    True,
                ),
            ]
        )
        if not include_extension:
            schema.fields = [
                c
                if c.name != "extension"
                else StructField("extension", StringType(), True)
                for c in schema.fields
            ]
        return schema
