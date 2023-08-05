from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import DataType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class AuditEvent_NetworkSchema:
    """
    A record of an event made for purposes of maintaining a security log. Typical
    uses include detection of intrusion attempts and monitoring for inappropriate
    usage.
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
        A record of an event made for purposes of maintaining a security log. Typical
        uses include detection of intrusion attempts and monitoring for inappropriate
        usage.


        address: An identifier for the network access point of the user device for the audit
            event.

        type: An identifier for the type of network access point that originated the audit
            event.

        """
        if (
            max_recursion_limit
            and nesting_list.count("AuditEvent_Network") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["AuditEvent_Network"]
        schema = StructType(
            [
                # An identifier for the network access point of the user device for the audit
                # event.
                StructField("address", StringType(), True),
                # An identifier for the type of network access point that originated the audit
                # event.
                StructField("type", StringType(), True),
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
