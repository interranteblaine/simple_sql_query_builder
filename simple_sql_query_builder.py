import re


class SimpleSQLQueryBuilder:
    def __init__(self):
        self.query = ""
        self.params = []

    def select(self, columns):
        self.query += "SELECT "
        if columns == "*":
            self.query += "*"
        else:
            if isinstance(columns, (list, tuple)):
                columns = [str(col) for col in columns]
            else:
                columns = [str(columns)]

            self.query += ", ".join(columns)
        return self

    def from_table(self, table):
        self.query += f" FROM {table}"
        return self

    def insert_into(self, table):
        self.query += f"INSERT INTO {table}"
        return self

    def values(self, values):
        columns = ", ".join(values.keys())
        placeholders = ", ".join(["%s"] * len(values))
        self.query += f"({columns}) VALUES ({placeholders})"
        self.params.extend(list(values.values()))
        return self

    def update(self, table):
        self.query += f"UPDATE {table}"
        return self

    def set(self, values):
        set_values = ", ".join([f"{column} = %s" for column in values.keys()])
        self.query += f" SET {set_values}"
        self.params.extend(list(values.values()))
        return self

    def delete_from(self, table):
        self.query += f"DELETE FROM {table}"
        return self

    def where(self, conditions, operator="AND"):
        self.query += " WHERE "
        conditions_with_params = []
        for column, condition in conditions.items():
            condition_operator = condition["operator"].upper()
            condition_value = condition["value"]
            if condition_operator == "LIKE":
                conditions_with_params.append(f"{column} LIKE %s")
                self.params.append(condition_value)
            elif condition_operator == "IN":
                if not isinstance(condition_value, (list, tuple)):
                    raise ValueError(
                        "Value for IN operator must be a list or tuple")
                placeholders = ", ".join(["%s"] * len(condition_value))
                conditions_with_params.append(f"{column} IN ({placeholders})")
                self.params.extend(condition_value)
            elif condition_operator in ["=", "<", ">", "<=", ">=", "!="]:
                conditions_with_params.append(
                    f"{column} {condition_operator} %s")
                self.params.append(condition_value)
            else:
                raise ValueError(f"Invalid operator: {condition_operator}")

        self.query += f" {operator} ".join(conditions_with_params)
        return self

    def group_by(self, columns):
        if isinstance(columns, (list, tuple)):
            group_by_clause = ", ".join(columns)
        else:
            group_by_clause = columns
        self.query += f" GROUP BY {group_by_clause}"
        return self

    def order_by(self, *args):
        if not args:
            return self

        order_by_clause = []
        for arg in args:
            if isinstance(arg, tuple):
                column, ascending = arg
            else:
                column, ascending = arg, True

            if not isinstance(column, str):
                raise ValueError("Column names must be strings")

            order_by_clause.append(
                f"{column} {'ASC' if ascending else 'DESC'}")

        self.query += f" ORDER BY {', '.join(order_by_clause)}"
        return self

    def limit(self, limit):
        self.query += f" LIMIT {limit}"
        return self

    def offset(self, offset):
        self.query += f" OFFSET {offset}"
        return self

    def build(self):
        return self.query + ';', self.params

    def build_query_string(self):
        query_string = self.query
        if self.params:
            for param in self.params:
                if isinstance(param, str):
                    param = f"'{param}'"
                query_string = query_string.replace("%s", str(param), 1)
        return query_string + ';'

    @staticmethod
    def sanitize_input(value):
        # Remove any SQL special characters that can be used for injection
        sanitized_value = re.sub(r"[;\\'\"]", '', value)
        return sanitized_value
