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

```

## 📦 Consulta de dades del Lakehouse
```bash
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
```

---

## 📂 Exemple de valors
- **TENANT_ID:** 37a8a0b9-1874-4e5d-b1f5-11040c1c07fc
- **SERVER:** xgqkqn3udbou5mpvcecayhah7q-s4yfrirfuyaelmqiu46vvbbfqu.datawarehouse.fabric.microsoft.com
- **DATABASE:** lakehouse_gold
