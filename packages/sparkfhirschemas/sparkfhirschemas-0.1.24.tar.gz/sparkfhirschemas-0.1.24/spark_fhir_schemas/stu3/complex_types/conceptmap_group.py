from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import ArrayType
from pyspark.sql.types import DataType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class ConceptMap_GroupSchema:
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


        source: An absolute URI that identifies the Code System (if the source is a value set
            that crosses more than one code system).

        sourceVersion: The specific version of the code system, as determined by the code system
            authority.

        target: An absolute URI that identifies the code system of the target code (if the
            target is a value set that cross code systems).

        targetVersion: The specific version of the code system, as determined by the code system
            authority.

        element: Mappings for an individual concept in the source to one or more concepts in
            the target.

        unmapped: What to do when there is no match in the mappings in the group.

        """
        from spark_fhir_schemas.stu3.complex_types.conceptmap_element import (
            ConceptMap_ElementSchema,
        )
        from spark_fhir_schemas.stu3.complex_types.conceptmap_unmapped import (
            ConceptMap_UnmappedSchema,
        )

        if (
            max_recursion_limit
            and nesting_list.count("ConceptMap_Group") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["ConceptMap_Group"]
        schema = StructType(
            [
                # An absolute URI that identifies the Code System (if the source is a value set
                # that crosses more than one code system).
                StructField("source", StringType(), True),
                # The specific version of the code system, as determined by the code system
                # authority.
                StructField("sourceVersion", StringType(), True),
                # An absolute URI that identifies the code system of the target code (if the
                # target is a value set that cross code systems).
                StructField("target", StringType(), True),
                # The specific version of the code system, as determined by the code system
                # authority.
                StructField("targetVersion", StringType(), True),
                # Mappings for an individual concept in the source to one or more concepts in
                # the target.
                StructField(
                    "element",
                    ArrayType(
                        ConceptMap_ElementSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension,
                        )
                    ),
                    True,
                ),
                # What to do when there is no match in the mappings in the group.
                StructField(
                    "unmapped",
                    ConceptMap_UnmappedSchema.get_schema(
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
