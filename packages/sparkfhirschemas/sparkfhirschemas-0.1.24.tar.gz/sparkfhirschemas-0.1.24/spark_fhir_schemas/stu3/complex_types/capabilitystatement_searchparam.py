from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import DataType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class CapabilityStatement_SearchParamSchema:
    """
    A Capability Statement documents a set of capabilities (behaviors) of a FHIR
    Server that may be used as a statement of actual server functionality or a
    statement of required or desired server implementation.
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
        A Capability Statement documents a set of capabilities (behaviors) of a FHIR
        Server that may be used as a statement of actual server functionality or a
        statement of required or desired server implementation.


        name: The name of the search parameter used in the interface.

        definition: An absolute URI that is a formal reference to where this parameter was first
            defined, so that a client can be confident of the meaning of the search
            parameter (a reference to [[[SearchParameter.url]]]).

        type: The type of value a search parameter refers to, and how the content is
            interpreted.

        documentation: This allows documentation of any distinct behaviors about how the search
            parameter is used.  For example, text matching algorithms.

        """
        if (
            max_recursion_limit
            and nesting_list.count("CapabilityStatement_SearchParam")
            >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["CapabilityStatement_SearchParam"]
        schema = StructType(
            [
                # The name of the search parameter used in the interface.
                StructField("name", StringType(), True),
                # An absolute URI that is a formal reference to where this parameter was first
                # defined, so that a client can be confident of the meaning of the search
                # parameter (a reference to [[[SearchParameter.url]]]).
                StructField("definition", StringType(), True),
                # The type of value a search parameter refers to, and how the content is
                # interpreted.
                StructField("type", StringType(), True),
                # This allows documentation of any distinct behaviors about how the search
                # parameter is used.  For example, text matching algorithms.
                StructField("documentation", StringType(), True),
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
