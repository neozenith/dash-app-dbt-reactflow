# Dash DBT App Prototype

Playing around getting a Dash app to interact with a dbt project fronted by a FastAPI endpoint.

```sh
# Create 2 fake dbt projects to demonstrate multi-project support.
git clone https://github.com/dbt-labs/jaffle_shop ./dbt/jaffle_shop
git clone https://github.com/dbt-labs/jaffle_shop ./dbt/jaffle_shop2

# Run in a terminal to start a postgresql db
invoke dev-db

# Run in a terminal to start dbt server which manages dbt project and commands.
invoke dev-dbt

# Run in a terminal to start Dash server
invoke dev
```