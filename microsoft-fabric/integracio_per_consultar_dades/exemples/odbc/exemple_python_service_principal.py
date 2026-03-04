import struct
import time
import pyodbc
from azure.identity import InteractiveBrowserCredential,ClientSecretCredential

# ---- CONFIG ----
TENANT_ID = "TENANT_ID"             # e.g., "contoso.onmicrosoft.com" or GUID
CLIENT_ID = "CLIENT_ID"             # Si tens un registre d’aplicació específic; altrament deixa-ho a None
CLIENT_SECRET = "CLIENT_SECRET"
SERVER = "SERVER,PORT"              # e.g., "xxxx-xxxx-xxxxx.sql.fabric.microsoft.com,1433"
DATABASE = "bronze_lh"              # e.g., "lakehouse_bronze"
# ----------------

# Fabric SQL endpoints use the SQL Database resource for tokens
SCOPE = "https://database.windows.net/.default"

# Create interactive credential (pops a browser on first use)
credential = ClientSecretCredential(
    tenant_id=TENANT_ID,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

def get_sql_access_token():
    """
    Acquire an AAD token for the SQL resource via interactive browser sign-in.
    Returns a bytes object suitable for ODBC's ActiveDirectoryAccessToken.
    """
    token = credential.get_token(SCOPE)
    access_token = token.token.encode("utf-16-le")  # ODBC requires UTF-16-LE
    # The driver expects the token as a struct-packed byte buffer
    return struct.pack(f"<I{len(access_token)}s", len(access_token), access_token)

def connect_with_access_token():
    """
    Build a pyodbc connection using ActiveDirectoryAccessToken.
    """
    # Basic ODBC connection string; note: Authentication is done via token, not here
    conn_str = (
        "Driver={ODBC Driver 18 for SQL Server};"
        f"Server={SERVER};"
        f"Database={DATABASE};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    SQL_COPT_SS_ACCESS_TOKEN = 1256  # ODBC token attribute
    token_bytes = get_sql_access_token()

    cnxn = pyodbc.connect(conn_str, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_bytes})
    return cnxn

if __name__ == "__main__":
    with connect_with_access_token() as cnxn:
        with cnxn.cursor() as cur:
            cur.execute("SELECT 1;")
            rows = cur.fetchall()
            for r in rows:
                print(r)