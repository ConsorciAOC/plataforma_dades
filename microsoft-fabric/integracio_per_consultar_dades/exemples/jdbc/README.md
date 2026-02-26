# 📘 Connectar-se a Microsoft Fabric Lakehouse SQL Endpoint mitjançant JDBC

Aquest article explica com connectar-se al **SQL Endpoint d’un Lakehouse de Microsoft Fabric** utilitzant **JDBC des de Python**. 
Tot i això, cal recordar que JDBC en Python depèn de *jaydebeapi* i *JPype1*, que poden no estar disponibles en alguns entorns. Aquest document replica l'exemple original i detalla els passos necessaris.

---
## 📂 Contingut
- Requisits
- Instal·lació
- Obtenció del token d’accés
- Connexió JDBC
- Execució de consultes
- Exemple de valors

---
## 🔧 Requisits
Abans de començar, necessites:
- Accés a Microsoft Fabric
- Python 3.9 o superior
- Driver JDBC de SQL Server (`mssql-jdbc-<versio>.jar`)
- Llibreries Python:
  - `jaydebeapi`
  - `JPype1`
  - `azure-identity`

---
## 📦 Instal·lació
Instal·la les dependències necessàries:
```bash
pip install jaydebeapi JPype1 azure-identity
```
> ⚠️ *Nota*: En alguns entorns pot fallar la instal·lació de JPype1.

---
## 🔑 Obtenció del token d’accés
```python
from azure.identity import InteractiveBrowserCredential
import struct

SCOPE = "https://database.windows.net/.default"
TENANT_ID = "<TENANT_ID>"

cred = InteractiveBrowserCredential(tenant_id=TENANT_ID)
token = cred.get_token(SCOPE)

# Convertim el token al format requerit per SQL
token_bytes = token.token.encode("utf-16-le")
packed_token = struct.pack(f"<I{len(token_bytes)}s", len(token_bytes), token_bytes)
```

---
## 🧩 Connexió JDBC
```python
import jaydebeapi

SERVER = "<SQL_ENDPOINT_URL>"  # Exemple: xxxx.datawarehouse.fabric.microsoft.com
DATABASE = "<LAKEHOUSE_NAME>"
DRIVER_CLASS = "com.microsoft.sqlserver.jdbc.SQLServerDriver"
JDBC_URL = f"jdbc:sqlserver://{SERVER}:1433;database={DATABASE};encrypt=true;trustServerCertificate=false;"
JAR_FILE = "mssql-jdbc-12.6.1.jre11.jar"

# Propietats JDBC
properties = {
    "accessToken": token.token
}

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
```

---
## 📂 Exemple de valors
- **TENANT_ID:** 37a8a0b9-1874-4e5d-b1f5-11040c1c07fc
- **SQL_ENDPOINT_URL:** xgqkqn3udbou5mpvcecayhah7q-hr43b7ttdlwutldvr36wzajgva.datawarehouse.fabric.microsoft.com
- **LAKEHOUSE_NAME:** lakehouse_gold

