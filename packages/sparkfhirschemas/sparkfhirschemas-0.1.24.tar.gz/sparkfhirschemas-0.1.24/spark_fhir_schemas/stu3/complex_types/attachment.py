from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import DataType
from pyspark.sql.types import IntegerType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class AttachmentSchema:
    """
    For referring to data content defined in other formats.
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
        For referring to data content defined in other formats.


        contentType: Identifies the type of the data in the attachment and allows a method to be
            chosen to interpret or render the data. Includes mime type parameters such as
            charset where appropriate.

        language: The human language of the content. The value can be any valid value according
            to BCP 47.

        data: The actual data of the attachment - a sequence of bytes. In XML, represented
            using base64.

        url: An alternative location where the data can be accessed.

        size: The number of bytes of data that make up this attachment (before base64
            encoding, if that is done).

        hash: The calculated hash of the data using SHA-1. Represented using base64.

        title: A label or set of text to display in place of the data.

        creation: The date that the attachment was first created.

        """
        if (
            max_recursion_limit
            and nesting_list.count("Attachment") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["Attachment"]
        schema = StructType(
            [
                # Identifies the type of the data in the attachment and allows a method to be
                # chosen to interpret or render the data. Includes mime type parameters such as
                # charset where appropriate.
                StructField("contentType", StringType(), True),
                # The human language of the content. The value can be any valid value according
                # to BCP 47.
                StructField("language", StringType(), True),
                # The actual data of the attachment - a sequence of bytes. In XML, represented
                # using base64.
                StructField("data", StringType(), True),
                # An alternative location where the data can be accessed.
                StructField("url", StringType(), True),
                # The number of bytes of data that make up this attachment (before base64
                # encoding, if that is done).
                StructField("size", IntegerType(), True),
                # The calculated hash of the data using SHA-1. Represented using base64.
                StructField("hash", StringType(), True),
                # A label or set of text to display in place of the data.
                StructField("title", StringType(), True),
                # The date that the attachment was first created.
                StructField("creation", StringType(), True),
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
