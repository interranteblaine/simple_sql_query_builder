## SimpleSQLQueryBuilder

The `SimpleSQLQueryBuilder` class provides methods to construct SQL queries dynamically.

### Methods

- `select(columns)`:

  - Constructs the SELECT statement with the specified columns.
  - Accepts a single column name as a string or a list/tuple of column names.
  - Returns the instance of the class.

- `from_table(table)`:

  - Adds the FROM clause to specify the table to query from.
  - Accepts the table name as a string.
  - Returns the instance of the class.

- `insert_into(table)`:

  - Constructs the INSERT INTO statement to specify the table to insert into.
  - Accepts the table name as a string.
  - Returns the instance of the class.

- `values(values)`:

  - Adds the column-value pairs to the INSERT INTO statement.
  - Accepts a dictionary where keys represent column names and values represent column values.
  - Returns the instance of the class.

- `update(table)`:

  - Constructs the UPDATE statement to specify the table to update.
  - Accepts the table name as a string.
  - Returns the instance of the class.

- `set(values)`:

  - Adds the column-value pairs to the SET clause of the UPDATE statement.
  - Accepts a dictionary where keys represent column names and values represent column values.
  - Returns the instance of the class.

- `delete_from(table)`:

  - Constructs the DELETE FROM statement to specify the table to delete from.
  - Accepts the table name as a string.
  - Returns the instance of the class.

- `where(conditions, operator="AND")`:

  - Adds the WHERE clause to specify the conditions for filtering rows.
  - Accepts a dictionary where keys represent column names, and values represent conditions in the form of a dictionary with "operator" and "value" keys.
  - The operator can be one of "=", "<", ">", "<=", ">=", "!=", or "LIKE".
  - The operator "LIKE" is used for pattern matching.
  - Returns the instance of the class.

- `group_by(columns)`:

  - Adds the GROUP BY clause to group the results by the specified columns.
  - Accepts a single column name as a string or a list/tuple of column names.
  - Returns the instance of the class.

- `order_by(columns, ascending=True)`:

  - Adds the ORDER BY clause to specify the order of the results.
  - Accepts a single column name as a string or a list/tuple of column names.
  - By default, the order is ascending, but you can set `ascending=False` to sort in descending order.
  - Returns the instance of the class.

- `limit(limit)`:

  - Adds the LIMIT clause to limit the number of rows returned.
  - Accepts the limit value as an integer.
  - Returns the instance of the class.

- `offset(offset)`:

  - Adds the OFFSET clause to specify the number of rows to skip.
  - Accepts the offset value as an integer.
  - Returns the instance of the class.

- `build()`:

  - Returns a tuple containing the constructed query string and the query parameters.

- `build_query_string()`:

  - Returns the query string with placeholders replaced by the actual query parameters.

- `sanitize_input(value)` (static method):

  - Sanitizes a given value by removing SQL special characters that can be used for injection.
  - Accepts the value as a string.
  - Returns the sanitized value.

You can use these methods in combination to construct your desired SQL queries.

### Basic Examples

1. Select all columns from a table:

```
query_builder = SimpleSQLQueryBuilder()
query = query_builder.select("*").from_table("users").build_query_string()
print(query)
# Output: SELECT * FROM users;
```

2. Select specific columns from a table with a WHERE condition:

```
query_builder = SimpleSQLQueryBuilder()
query = query_builder.select(["name", "email"]).from_table("users").where({"age": {"operator": ">", "value": 18}}).build_query_string()
print(query)
# Output: SELECT name, email FROM users WHERE age > 18;
```

3. Insert a row into a table:

```
query_builder = SimpleSQLQueryBuilder()
values = {"name": "John Doe", "email": "john.doe@example.com", "age": 25}
query = query_builder.insert_into("users").values(values).build_query_string()
print(query)
# Output: INSERT INTO users (name, email, age) VALUES ('John Doe', 'john.doe@example.com', 25);
```

4. Update rows in a table with a WHERE condition:

```
query_builder = SimpleSQLQueryBuilder()
values = {"name": "Jane Doe", "age": 30}
query = query_builder.update("users").set(values).where({"id": {"operator": "=", "value": 1}}).build_query_string()
print(query)
# Output: UPDATE users SET name = 'Jane Doe', age = 30 WHERE id = 1;
```

5. Delete rows from a table with a WHERE condition:

```
query_builder = SimpleSQLQueryBuilder()
query = query_builder.delete_from("users").where({"age": {"operator": "<", "value": 18}}).build_query_string()
print(query)
# Output: DELETE FROM users WHERE age < 18;
```

6. Filtering with pagination parameters:

```
page_number = 3
page_size = 25
offset = (page_number - 1) * page_size

query_builder = SimpleSQLQueryBuilder()
query = query_builder.select("*").from_table("products").where(
    {
        "category": {"operator": "=", "value": "Electronics"},
        "price": {"operator": "<=", "value": 1000},
        "brand": {"operator": "IN", "value": ["Apple", "Samsung", "Sony"]},
    }
).order_by(("price", False),
           "name",
           ("rating", True)).limit(page_size).offset(offset).build_query_string()

print(query)

# Output: SELECT * FROM products WHERE category = 'Electronics' AND price <= 1000 AND brand IN ('Apple', 'Samsung', 'Sony') ORDER BY price DESC, name ASC, rating ASC LIMIT 25 OFFSET 50;
```

7. Sanitize user input

```
query_builder = SimpleSQLQueryBuilder()

user_input = "John'; DROP TABLE users; --"

# Sanitize the user input before using it in the query
sanitized_input = SimpleSQLQueryBuilder.sanitize_input(user_input)

query_builder.select("*").from_table("users").where({"name": {"operator": "=", "value": sanitized_input}})

query = query_builder.build_query_string()

print(query)
# Output: SELECT * FROM users WHERE name = 'John DROP TABLE users --';
```

Note: Sanitizing input is just one aspect of preventing SQL injection. It's important to also consider other security measures like parameterized queries and input validation to ensure robust security.

8. Parameterize query

```
query_builder = SimpleSQLQueryBuilder()

user_input = "John'; DROP TABLE users; --"

# Sanitize the user input before using it in the query
sanitized_input = SimpleSQLQueryBuilder.sanitize_input(user_input)

query_builder.select(
    "*").from_table("users").where({"name": {"operator": "=", "value": sanitized_input}})

query, params = query_builder.build()

print(query)
# Output: SELECT * FROM users WHERE name = %s;
print(params)
# Output: ['John DROP TABLE users --']
```
