
# 📘 Consultar dades des de Python utilitzant Microsoft Fabric Graph API

Aquest article explica com connectar-se a la **Graph API de Microsoft Fabric** i consultar dades d’un **Lakehouse**, **Warehouse** o **KQL Database** utilitzant **Python**.
Inclou exemples d’autenticació, execució de consultes i gestió de resultats.

---
## 📂 Contingut
- Requisits
- Obtenir la URL de la Fabric GraphQL API
- Instal·lació
- Autenticació amb Azure AD
- Executar consultes amb la Fabric Graph API

---
## 🔧 Requisits
Abans de començar, necessites:
- Un compte o Service Principal amb accés a Microsoft Fabric
- Python 3.9 o superior
- URL GraphQL de connexió

---
## 📦 Instal·lació
Instal·la les dependències necessàries:
```bash
pip install -r requirements.txt
```

## 📦 Obtenció del token d’accés
```python
import requests
import msal
import pandas as pd

TENANT_ID = "TENANT_ID"
CLIENT_ID = "CLIENT_ID"
CLIENT_SECRET = "CLIENT_SECRET"
GRAPHQL_ENDPOINT = "GRAPHQL_ENDPOINT"

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://api.fabric.microsoft.com/.default"]

app = msal.ConfidentialClientApplication(
    CLIENT_ID,
    authority=AUTHORITY,
    client_credential=CLIENT_SECRET
)

token = app.acquire_token_for_client(scopes=SCOPE)

if "access_token" not in token:
    raise Exception("Error obtenint el token: ", token)

access_token = token["access_token"]
```

## 📦 Consulta de dades del Lakehouse
```python
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

endpoint = GRAPHQL_ENDPOINT
query = """
{ fac_activitats (first: 1000){ items { ide_ens_original } } }
"""

variables = {}

try:
    response = requests.post(endpoint, json={'query': query, 'variables': variables}, headers=headers)
    response.raise_for_status()
    data = response.json()
    print(json.dumps(data, indent=4))
except Exception as error:
    print(f"La consulta ha fallat amb l’error: {error}")
```

---
## 📂 Exemple de valors
- **TENANT_ID:** 37a8a0b9-1874-4e5d-b1f5-11040c1c07fc
- **GRAPHQL_ENDPOINT:** https://040f10b0c0084e4692276db70e217de0.z04.graphql.fabric.microsoft.com/v1/workspaces/040f10b0-c008-4e46-9227-6db70e217de0/graphqlapis/d7bd49fe-0521-4182-ba2a-5e2b7c664c43/graphql
