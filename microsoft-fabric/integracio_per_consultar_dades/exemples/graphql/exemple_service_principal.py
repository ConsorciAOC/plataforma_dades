from azure.identity import InteractiveBrowserCredential
import requests
import json

# -----------------------------
# OBTENER TOKEN
# -----------------------------
TENANT_ID = "YOUR_TENANT_ID"
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://api.fabric.microsoft.com/.default"]

app = msal.ConfidentialClientApplication(
    CLIENT_ID,
    authority=AUTHORITY,
    client_credential=CLIENT_SECRET
)

token = app.acquire_token_for_client(scopes=SCOPE)

if "access_token" not in token:
    raise Exception("Error obteniendo token: ", token)

access_token = token["access_token"]


# -----------------------------
# OBTENER RESULTADOS GRAPHQL
# -----------------------------
headers = {
    'Authorization': f'Bearer {result.token}',
    'Content-Type': 'application/json'
}

endpoint = 'https://<grapQLURL>.graphql.fabric.microsoft.com/v1/workspaces/<workspaceID>/graphqlapis/<graphAPIId>/graphql'
query = """
    {
    "query":"{ fac_activitats (first: 100000){items{ide_ens_original } } } "
    }
"""

variables = {

  }
  

# Issue GraphQL request
try:
    response = requests.post(endpoint, json={'query': query, 'variables': variables}, headers=headers)
    response.raise_for_status()
    data = response.json()
    print(json.dumps(data, indent=4))
except Exception as error:
    print(f"Query failed with error: {error}")
