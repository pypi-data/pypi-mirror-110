from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import DataType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class ConceptMap_DependsOnSchema:
    """
    A statement of relationships from one set of concepts to one or more other
    concepts - either code systems or data elements, or classes in class models.
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
        A statement of relationships from one set of concepts to one or more other
        concepts - either code systems or data elements, or classes in class models.


        property: A reference to an element that holds a coded value that corresponds to a code
            system property. The idea is that the information model carries an element
            somwhere that is labeled to correspond with a code system property.

        system: An absolute URI that identifies the code system of the dependency code (if the
            source/dependency is a value set that crosses code systems).

        code: Identity (code or path) or the element/item/ValueSet that the map depends on /
            refers to.

        display: The display for the code. The display is only provided to help editors when
            editing the concept map.

        """
        if (
            max_recursion_limit
            and nesting_list.count("ConceptMap_DependsOn") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["ConceptMap_DependsOn"]
        schema = StructType(
            [
                # A reference to an element that holds a coded value that corresponds to a code
                # system property. The idea is that the information model carries an element
                # somwhere that is labeled to correspond with a code system property.
                StructField("property", StringType(), True),
                # An absolute URI that identifies the code system of the dependency code (if the
                # source/dependency is a value set that crosses code systems).
                StructField("system", StringType(), True),
                # Identity (code or path) or the element/item/ValueSet that the map depends on /
                # refers to.
                StructField("code", StringType(), True),
                # The display for the code. The display is only provided to help editors when
                # editing the concept map.
                StructField("display", StringType(), True),
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
