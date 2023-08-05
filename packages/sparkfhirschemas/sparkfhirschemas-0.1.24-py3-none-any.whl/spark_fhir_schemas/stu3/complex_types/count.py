from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import DataType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class CountSchema:
    """
    A measured amount (or an amount that can potentially be measured). Note that
    measured amounts include amounts that are not precisely quantified, including
    amounts involving arbitrary units and floating currencies.
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
        A measured amount (or an amount that can potentially be measured). Note that
        measured amounts include amounts that are not precisely quantified, including
        amounts involving arbitrary units and floating currencies.


        """
        return StringType()
