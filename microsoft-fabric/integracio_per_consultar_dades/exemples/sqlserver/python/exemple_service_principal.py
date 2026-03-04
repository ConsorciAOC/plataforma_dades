import mssql_python

# Connection parameters
SERVER = "SERVER"                       # e.g., "xxxx-xxxx-xxxxx.sql.fabric.microsoft.com"
DATABASE = "DATABASE"                   # e.g., "lakehouse_gold"
CLIENT_ID = "CLIENT_ID"                 # Si tens un registre d’aplicació específic
CLIENT_SECRET = "CLIENT_SECRET"         # Si tens un registre d’aplicació pdw

# Connection string
conn_str = f"""
Server={SERVER},1433;
Database={DATABASE};
Authentication=ActiveDirectoryServicePrincipal;
UID={CLIENT_ID};
PWD={CLIENT_SECRET};
Encrypt=yes;
TrustServerCertificate=no
"""

try:
    # Establish connection
    with mssql_python.connect(conn_str) as conn:
        with conn.cursor() as cursor:
            # Test query
            cursor.execute("SELECT DISTINCT(ide_ens) FROM [aoc_enotum].[fac_notificacions_activitat];")  # No data, just schema
            
            rows = cursor.fetchall()
            for row in rows:
                print(row)

    print("Connection successful.")

except Exception as e:
    print("Connection failed:")
    print(e)