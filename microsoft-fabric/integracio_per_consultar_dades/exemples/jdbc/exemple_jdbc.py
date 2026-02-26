"""
Example: Connecting to Microsoft Fabric Lakehouse SQL Endpoint via JDBC
"""

import jaydebeapi
from azure.identity import InteractiveBrowserCredential
import struct

# --------- AUTHENTICATION ---------
SCOPE = "https://database.windows.net/.default"
TENANT_ID = "<TENANT_ID>"                       # e.g., "contoso.onmicrosoft.com" or GUID
SERVER = "<SERVER>"                             # e.g. xxxxxx-s12345.datawarehouse.fabric.microsoft.com
DATABASE = "<LAKEHOUSE_NAME>"                   # e.g. lakehouse_gold
DRIVER_CLASS = "com.microsoft.sqlserver.jdbc.SQLServerDriver"
JDBC_URL = f"jdbc:sqlserver://{SERVER}:1433;database={DATABASE};encrypt=true;trustServerCertificate=false;"
JAR_FILE = "mssql-jdbc-12.6.1.jre11.jar"        # Adjust version as needed

# Get token
cred = InteractiveBrowserCredential(tenant_id=TENANT_ID)
token = cred.get_token(SCOPE)

token_bytes = token.token.encode("utf-16-le")
packed_token = struct.pack(f"<I{len(token_bytes)}s", len(token_bytes), token_bytes)

# JDBC connection properties
properties = {
    "accessToken": token.token
}

# --------- CONNECT ---------
try:
    conn = jaydebeapi.connect(DRIVER_CLASS, JDBC_URL, properties, JAR_FILE)
    curs = conn.cursor()
    curs.execute("SELECT TOP 10 * FROM <schema>.<table>;")
    rows = curs.fetchall()
    for r in rows:
        print(r)
    curs.close()
    conn.close()
except Exception as e:
    print("Connection failed:", e)
