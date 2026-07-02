import requests
import json
import msal
import asyncio
from azure.identity import InteractiveBrowserCredential
from azure.identity import AzureCliCredential
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

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
# CALL MCP
# -----------------------------
workspace_id = "YOUR_WORKSPACE_ID"
data_agent_id = "YOUR_DATA_AGENT_ID"
question = "<question>"

mcp_url = (
    f"https://api.fabric.microsoft.com/v1/mcp/workspaces/{workspace_id}"
    f"/dataagents/{data_agent_id}/agent"
)

credential = AzureCliCredential()

def get_auth_headers():
    return {"Authorization": f"Bearer {access_token}"}

async def query_data_agent(question):
    headers = get_auth_headers()

    async with streamablehttp_client(mcp_url, headers=headers) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # The data agent exposes a single tool. Discover it, then call it.
            tools = await session.list_tools()
            tool = tools.tools[0]
            question_arg = next(iter(tool.inputSchema["properties"]))

            result = await session.call_tool(tool.name, {question_arg: question})

            answers = [block.text for block in result.content if block.type == "text"]
            return "\n".join(answers)
        

answer = asyncio.run(query_data_agent(question))
print(answer)