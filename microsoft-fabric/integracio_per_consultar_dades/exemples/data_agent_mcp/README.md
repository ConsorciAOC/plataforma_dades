# 📘 Consulta de Data Agents de Microsoft Fabric mitjançant MCP i Python

Aquest document explica com consultar un **Data Agent de Microsoft Fabric** utilitzant **Python** i el protocol **MCP (Model Context Protocol)**.

---

## 📂 Contingut

- Requisits
- Instal·lació de dependències
- Exemple 1: autenticació amb Azure CLI
- Exemple 2: autenticació amb Service Principal
- Configuració dels paràmetres
- Execució dels exemples
- Estructura del projecte

---

## 🔧 Requisits

Abans de començar, assegura't de disposar de:

- Accés a Microsoft Fabric
- Un Workspace de Fabric
- Un Data Agent publicat
- Python 3.10 o superior
- Permisos per accedir al Data Agent

Per a l'autenticació:

### Opció 1: Azure CLI

- Azure CLI instal·lat
- Sessió iniciada amb:

```bash
az login
```

### Opció 2: Service Principal

- Tenant ID
- Client ID
- Client Secret
- Permisos sobre Microsoft Fabric

---

## 📦 Instal·lació de dependències

Instal·la les llibreries definides a `requirements.txt`:

```bash
pip install -r requirements.txt
```

Exemples de dependències utilitzades:

```text
azure-identity
mcp
msal
requests
```

---

## 🔐 Exemple 1: Autenticació amb Azure CLI

Fitxer:

```text
exemple_mcp_entraid.py
```

Aquest exemple utilitza les credencials de l'usuari autenticat amb Azure CLI per obtenir un token d'accés i consultar el Data Agent.

### Funcionament

1. Obté un token mitjançant `AzureCliCredential`.
2. Construeix la URL MCP del Data Agent.
3. Descobreix automàticament l'eina exposada pel Data Agent.
4. Envia una pregunta al Data Agent.
5. Mostra la resposta per consola.

### Paràmetres principals

```python
workspace_id = "YOUR_WORKSPACE_ID"
data_agent_id = "YOUR_DATA_AGENT_ID"
question = "La teva pregunta"
```

---

## 🔑 Exemple 2: Autenticació amb Service Principal

Fitxer:

```text
exemple_mcp_service_principal.py
```

Aquest exemple utilitza MSAL per obtenir un token mitjançant un Service Principal i executar consultes al Data Agent sense necessitat d'un usuari interactiu.

### Funcionament

1. Obté un token OAuth utilitzant MSAL.
2. Utilitza el flux d'autenticació Client Credentials.
3. Construeix la connexió amb l'endpoint MCP de Fabric.
4. Descobreix automàticament l'eina exposada pel Data Agent.
5. Executa la pregunta i retorna la resposta.

### Paràmetres principals

```python
TENANT_ID = "YOUR_TENANT_ID"
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"

workspace_id = "YOUR_WORKSPACE_ID"
data_agent_id = "YOUR_DATA_AGENT_ID"
question = "La teva pregunta"
```

### Exemple de valors

```python
TENANT_ID = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
CLIENT_ID = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
CLIENT_SECRET = "xxxxxxxxxxxxxxxxxxxxxxxxxxxx"

workspace_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
data_agent_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

question = "Quina és l'edat mitjana de la bretxa digital?"
```

---

## ⚙️ Configuració dels paràmetres

### Workspace ID

Identificador únic del Workspace de Microsoft Fabric.

---