"""
Example: Connecting to Microsoft Fabric Lakehouse SQL Endpoint via JDBC
"""

import pyodbc
from azure.identity import ClientSecretCredential
import struct

# --------- AUTHENTICATION ---------

DRIVER_CLASS = "com.microsoft.sqlserver.jdbc.SQLServerDriver"
CONN_STR = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=#SERVER#,1433;"
    "DATABASE=#DATABASE#;"
    "Authentication=ActiveDirectoryServicePrincipal;"
    "UID=#SERVICE_PRINCIPAL_CLIENT_ID#;"
    "PWD=#SERVICE_PRINCIPAL_CLIENT_SECRET#;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
)



# --------- CONNECT ---------
try:
    conn = pyodbc.connect(CONN_STR)
    cursor = conn.cursor()

    cursor.execute("SELECT TOP 10 * FROM aoc_valid.fac_autenticacio;")
    print(cursor.fetchone())

    cursor.close()
    conn.close()

except Exception as e:
    print("Connection failed:", e)
