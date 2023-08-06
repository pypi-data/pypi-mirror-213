import random
import string
from typing import Sequence, Union, List, Dict, Tuple, Callable
from p360_export.exceptions.query_builder import NoAttributesSelectedException


class QueryBuilder:
    def __init__(self, config):
        self.__params = config["params"]
        self.__segments = config["segments"]

    def __get_table_id(self):
        return "".join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=32))

    def __build_select_part(self, table_id: str) -> str:
        features = self.__params["export_columns"]
        attributes = list(self.__params["mapping"].values())

        columns = ", ".join(list(dict.fromkeys(features + attributes)))

        if not columns:
            raise NoAttributesSelectedException("Cannot export an empty subset of attributes.")

        return f"SELECT {columns} FROM {table_id}"

    def __get_build_term_method(self, option: str) -> Callable:
        if option == "BETWEEN":
            return self.__build_term__between
        if option == "EQUALS":
            return self.__build_term__equals
        if option == "NOT_EQUALS":
            return self.__build_term_not_equals
        if option == "LESS_THAN":
            return self.__build_term__less_than
        if option == "GREATER_THAN":
            return self.__build_term__greater_than

        raise NotImplementedError(f"{option} option not implemented yet.")

    def __build_term(self, term_config: dict) -> str:
        option = term_config.get("op")
        column_name = term_config.get("id")
        value = term_config.get("value")

        build_term_method = self.__get_build_term_method(option)

        return build_term_method(column_name, value)

    def __build_term__between(self, column_name: str, value: Sequence[float]) -> str:
        return " ".join([column_name, "BETWEEN", str(value[0]), "AND", str(value[1])])

    def __build_term_not_equals(self, column_name: str, value: Union[bool, float, List[str]]) -> str:
        if isinstance(value, bool):
            value = int(value)

        if isinstance(value, list):
            values = ",".join([f"'{value}'" for value in value])

            return f"{column_name} NOT IN ({values})"

        return " ".join([column_name, "!=", str(value)])

    def __build_term__equals(self, column_name: str, value: Union[bool, float, List[str]]) -> str:
        if isinstance(value, bool):
            value = int(value)

        if isinstance(value, list):
            values = ",".join([f"'{value}'" for value in value])

            return f"{column_name} IN ({values})"

        return " ".join([column_name, "=", str(value)])

    def __build_term__less_than(self, column_name: str, value: float) -> str:
        if isinstance(value, bool):
            value = int(value)

        return " ".join([column_name, "<", str(value)])

    def __build_term__greater_than(self, column_name: str, value: float) -> str:
        if isinstance(value, bool):
            value = int(value)

        return " ".join([column_name, ">", str(value)])

    def __assemble_terms(self, terms: Sequence[str], logical_operator: str) -> str:
        if logical_operator not in ["AND", "OR"]:
            raise ValueError("Only AND and OR logical_operator supported.")

        subquery = f"\n{logical_operator}\n".join(terms)

        if logical_operator == "AND":
            subquery = "(\n" + subquery + "\n)"

        return subquery

    def __exporting_all_users(self, segment_definition: List[Dict]) -> bool:
        if not segment_definition or not segment_definition[0]:
            return True

        return False

    def __build_condition(self) -> str:
        if self.__exporting_all_users(self.__segments):
            return ""

        list_of_product_terms = self.__build_list_of_product_terms(self.__segments[0].get("definition_segment"))

        query_condition = self.__assemble_terms(terms=list_of_product_terms, logical_operator="OR")

        return query_condition

    def __build_list_of_product_terms(self, definition_of_product_terms: Dict) -> Sequence[str]:
        list_of_product_terms = []

        for product_term_definition in definition_of_product_terms:
            list_of_clauses = self.__build_list_of_clauses(product_term_definition)
            product_term = self.__assemble_terms(terms=list_of_clauses, logical_operator="AND")
            list_of_product_terms.append(product_term)

        return list_of_product_terms

    def __build_list_of_clauses(self, product_term_definition: dict) -> List[str]:
        list_of_clauses = []

        for clause_definition in product_term_definition.get("attributes"):
            clause = self.__build_term(clause_definition)
            list_of_clauses.append(clause)

        return list_of_clauses

    def build(self) -> Tuple[str, str]:
        table_id = self.__get_table_id()

        condition = self.__build_condition()
        select_part = self.__build_select_part(table_id=table_id)

        if condition:
            query = select_part + " WHERE\n" + condition + ";"
        else:
            query = select_part + ";"

        return query, table_id
