
# Assume you are using Microsoft SQL Server.
# Modify this based on your database location

db_config = {
    'server': '<Your Server>',
    'database': '<Your database>'
}

connection_string = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={db_config['server']};"
    f"DATABASE={db_config['database']};"
    f"Trusted_Connection=yes;"
)
