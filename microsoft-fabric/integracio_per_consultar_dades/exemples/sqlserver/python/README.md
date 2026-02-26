# 📘 Consultar dades des de Python utilitzant SQL Driver

Aquest repositori explica com connectar-se al **punt de connexió SQL de Microsoft Fabric** i consultar dades d’un **Lakehouse** utilitzant **Python**.
Inclou exemples d’autenticació, execució de consultes i gestió de resultats.

---

## 📂 Contingut
- Requisits
- Obtenir URL Fabric Lakehouse SQL Endpoint
- Instal·lació
- Autenticació amb Azure AD
- Executar consultes amb la Fabric Graph API

---

## 🔧 Requisits
- Un compte amb accés a Microsoft Fabric
- Python 3.9 o superior
- Instal·lar les llibreries necessàries (vegeu ./requirements.txt)

---

## 🔧 Obtenir URL Fabric Lakehouse
1. Obre l’àrea de treball de Microsoft Fabric ([Fabric App](https://app.fabric.microsoft.com/)).
2. Obre el Lakehouse, ves a Configuració → Punt de Connexió d’Anàlisi SQL.
3. Copia la URL i el nom del Lakehouse.

---

## 📦 Instal·lació
```bash
pip install -r requirements.txt
```

## 📦 Obtenció del Token d’accés
```bash
import struct
import time
import pyodbc
from azure.identity import InteractiveBrowserCredential

TENANT_ID = "TENANT_ID"
CLIENT_ID = None
SERVER = "SQL_ENDPOINT_URL"
DATABASE = "NOM_LAKEHOUSE"

SCOPE = "https://database.windows.net/.default"

credential = InteractiveBrowserCredential(tenant_id=TENANT_ID, client_id=CLIENT_ID) if CLIENT_ID else InteractiveBrowserCredential(tenant_id=TENANT_ID)

def get_sql_access_token():
    token = credential.get_token(SCOPE)
    access_token = token.token.encode("utf-16-le")
    return struct.pack(f"<I{len(access_token)}s", len(access_token), access_token)
```

## 📦 Consulta de dades del Lakehouse
```bash
def connect_with_access_token():
    conn_str = (
        "Driver={ODBC Driver 18 for SQL Server};"
        f"Server={SERVER};"
        f"Database={DATABASE};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )
    SQL_COPT_SS_ACCESS_TOKEN = 1256
    token_bytes = get_sql_access_token()
    return pyodbc.connect(conn_str, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_bytes})

with connect_with_access_token() as cnxn:
    with cnxn.cursor() as cur:
        cur.execute("SELECT TOP 10 * FROM [lakehouse_gold].[aoc_via_oberta].[fac_activitat];")
        for r in cur.fetchall():
            print(r)
```

---

## 📂 Exemple de valors
- **TENANT_ID:** 37a8a0b9-1874-4e5d-b1f5-11040c1c07fc
- **SERVER:** xgqkqn3udbou5mpvcecayhah7q-s4yfrirfuyaelmqiu46vvbbfqu.datawarehouse.fabric.microsoft.com
- **DATABASE:** lakehouse_gold
