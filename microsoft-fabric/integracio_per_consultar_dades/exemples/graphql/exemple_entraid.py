from azure.identity import InteractiveBrowserCredential
import requests
import json

# Obtener token
app = InteractiveBrowserCredential()
scp = 'https://analysis.windows.net/powerbi/api/user_impersonation'
result = app.get_token(scp)

if not result.token:
    print('Error:', "Could not get access token")

# Prepare headers
headers = {
    'Authorization': f'Bearer {result.token}',
    'Content-Type': 'application/json'
}

endpoint = 'https://<grapQLURL>.graphql.fabric.microsoft.com/v1/workspaces/<workspaceID>/graphqlapis/<graphAPIId>/graphql'
query = """
    { fac_activitats (first: 1000){items{ide_ens_original }  "
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
