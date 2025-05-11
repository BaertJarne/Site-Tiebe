[connector_python]
import os
user = os.getenv("db_user")
host = os.getenv("db_uri")
port = os.getenv("db_port")
password = os.getenv("db_password")
database = os.getenv("db_name")

[application_config]
driver = 'SQL Server'