import unittest
from simple_sql_query_builder import SimpleSQLQueryBuilder


class TestSimpleSQLQueryBuilder(unittest.TestCase):
    def test_select_all(self):
        query_builder = SimpleSQLQueryBuilder()
        query_builder.select("*").from_table("users")
        query, params = query_builder.build()
        self.assertEqual(query, "SELECT * FROM users;")
        self.assertEqual(params, [])

    def test_select_columns(self):
        query_builder = SimpleSQLQueryBuilder()
        query_builder.select(["id", "name", "email"]).from_table("users")
        query, params = query_builder.build()
        self.assertEqual(query, "SELECT id, name, email FROM users;")
        self.assertEqual(params, [])

    def test_insert_into(self):
        query_builder = SimpleSQLQueryBuilder()
        values = {"name": "John", "email": "john@example.com"}
        query_builder.insert_into("users").values(values)
        query, params = query_builder.build()
        self.assertEqual(
            query, "INSERT INTO users(name, email) VALUES (%s, %s);")
        self.assertEqual(params, ["John", "john@example.com"])

    def test_update(self):
        query_builder = SimpleSQLQueryBuilder()
        values = {"name": "John", "email": "john@example.com"}
        query_builder.update("users").set(values).where(
            {"id": {"operator": "=", "value": 1}})
        query, params = query_builder.build()
        self.assertEqual(
            query, "UPDATE users SET name = %s, email = %s WHERE id = %s;")
        self.assertEqual(params, ["John", "john@example.com", 1])

    def test_delete_from(self):
        query_builder = SimpleSQLQueryBuilder()
        query_builder.delete_from("users").where(
            {"id": {"operator": "=", "value": 1}})
        query, params = query_builder.build()
        self.assertEqual(query, "DELETE FROM users WHERE id = %s;")
        self.assertEqual(params, [1])

    def test_where_operator(self):
        query_builder = SimpleSQLQueryBuilder()
        query_builder.select(
            "*").from_table("users").where({"age": {"operator": ">=", "value": 18}})
        query, params = query_builder.build()
        self.assertEqual(query, "SELECT * FROM users WHERE age >= %s;")
        self.assertEqual(params, [18])

    def test_where_single_condition(self):
        query_builder = SimpleSQLQueryBuilder()
        query_builder.select(
            '*').from_table('users').where({'name': {'operator': '=', 'value': 'John'}})
        query_string = query_builder.build_query_string()
        expected_query = "SELECT * FROM users WHERE name = 'John';"
        self.assertEqual(query_string, expected_query)

    def test_where_multiple_conditions(self):
        query_builder = SimpleSQLQueryBuilder()
        conditions = {
            'name': {'operator': '=', 'value': 'John'},
            'age': {'operator': '>', 'value': 30},
            'city': {'operator': 'LIKE', 'value': 'New%'}
        }
        query_builder.select('*').from_table('users').where(conditions)
        query_string = query_builder.build_query_string()
        expected_query = "SELECT * FROM users WHERE name = 'John' AND age > 30 AND city LIKE 'New%';"
        self.assertEqual(query_string, expected_query)

    def test_where_invalid_operator(self):
        query_builder = SimpleSQLQueryBuilder()
        conditions = {'name': {'operator': '$', 'value': 'John'}}
        with self.assertRaises(ValueError):
            query_builder.select('*').from_table('users').where(conditions)

    def test_select_with_like(self):
        query_builder = SimpleSQLQueryBuilder()
        query_builder.select(
            "*").from_table("users").where({"name": {"operator": "LIKE", "value": "John%"}})
        query, params = query_builder.build()
        self.assertEqual(query, "SELECT * FROM users WHERE name LIKE %s;")
        self.assertEqual(params, ["John%"])

    def test_group_by(self):
        query_builder = SimpleSQLQueryBuilder()
        query_builder.select(["name", "COUNT(*)"]
                             ).from_table("users").group_by(["name", "age"])
        query, params = query_builder.build()
        self.assertEqual(
            query, "SELECT name, COUNT(*) FROM users GROUP BY name, age;")
        self.assertEqual(params, [])

    def test_order_by(self):
        query_builder = SimpleSQLQueryBuilder()
        query_builder.select(
            "*").from_table("users").order_by("name", ("age", False))
        query, params = query_builder.build()
        self.assertEqual(
            query, "SELECT * FROM users ORDER BY name ASC, age DESC;")
        self.assertEqual(params, [])

    def test_limit(self):
        query_builder = SimpleSQLQueryBuilder()
        query_builder.select("*").from_table("users").limit(10)
        query, params = query_builder.build()
        self.assertEqual(query, "SELECT * FROM users LIMIT 10;")
        self.assertEqual(params, [])

    def test_offset(self):
        query_builder = SimpleSQLQueryBuilder()
        query_builder.select("*").from_table("users").offset(5)
        query, params = query_builder.build()
        self.assertEqual(query, "SELECT * FROM users OFFSET 5;")
        self.assertEqual(params, [])

    def test_sanitize_input(self):
        sanitized_value = SimpleSQLQueryBuilder.sanitize_input(
            "John'; DROP TABLE users;")
        self.assertEqual(sanitized_value, "John DROP TABLE users")

    def test_build_query_string(self):
        builder = SimpleSQLQueryBuilder()
        query = builder.select("*").from_table("users").where(
            {"name": {"operator": "=", "value": "John"}}).build_query_string()
        self.assertEqual(query, "SELECT * FROM users WHERE name = 'John';")

        builder = SimpleSQLQueryBuilder()
        query = builder.insert_into("users").values(
            {"name": "John", "age": 25}).build_query_string()
        self.assertEqual(
            query, "INSERT INTO users(name, age) VALUES ('John', 25);")

        builder = SimpleSQLQueryBuilder()
        query = builder.update("users").set({"age": 30}).where(
            {"name": {"operator": "=", "value": "John"}}).build_query_string()
        self.assertEqual(
            query, "UPDATE users SET age = 30 WHERE name = 'John';")

        builder = SimpleSQLQueryBuilder()
        query = builder.delete_from("users").where(
            {"name": {"operator": "=", "value": "John"}}).build_query_string()
        self.assertEqual(query, "DELETE FROM users WHERE name = 'John';")

        builder = SimpleSQLQueryBuilder()
        query = builder.select("name").from_table("users").group_by(
            "name").order_by("name").limit(10).offset(5).build_query_string()
        self.assertEqual(
            query, "SELECT name FROM users GROUP BY name ORDER BY name ASC LIMIT 10 OFFSET 5;")


if __name__ == "__main__":
    unittest.main()
