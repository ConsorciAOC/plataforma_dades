
# Connectar Databricks Unity Catalog a OneLake mitjançant Catalog Federation

Aquest article explica com connectar **Databricks Unity Catalog** amb **Microsoft OneLake** utilitzant la característica oficial de **OneLake Catalog Federation**. Aquesta integració permet consultar dades emmagatzemades en Lakehouses o Warehouses de Microsoft Fabric directament des d’Azure Databricks **sense copiar les dades**, mantenint OneLake com a font de veritat.

---
## Contingut
- Requisits previs
- Pas 1: Habilitar OneLake Read Federation
- Pas 2: Crear la connexió des d’Unity Catalog
- Pas 3: Crear el catàleg extern (Foreign Catalog)
- Pas 4: Consultar taules de OneLake des de Databricks
- Limitacions (Beta)
- Referències
---
## Requisits previs
- Workspace habilitat per a Unity Catalog
- Databricks Runtime 18.0+ en mode Standard
- SQL Warehouse Pro 2025.35+
- Permisos UC: CREATE CONNECTION, STORAGE CREDENTIAL, CATALOG, FOREIGN CATALOG
- Permisos Azure per Managed Identity o Service Principal
---
## Pas 1: Habilitar OneLake Read Federation
1. Admin Console → Previews
2. Activar OneLake Read Federation
3. Reiniciar cluster o SQL Warehouse
---
## Pas 2: Crear la connexió
```sql
CREATE CONNECTION onelake_connection
TYPE onelake
OPTIONS (
 authentication='servicePrincipal',
 clientId='APP_ID',
 clientSecret='APP_SECRET',
 tenantId='TENANT_ID',
 oneLakePath='https://onelake.dfs.fabric.microsoft.com/{workspaceName}/{itemName}'
);
```
---
## Pas 3: Crear el catàleg extern
```sql
CREATE FOREIGN CATALOG onelake_fabric_catalog
USING CONNECTION onelake_connection;
```
---
## Pas 4: Consultar dades
```sql
SELECT * FROM onelake_fabric_catalog.schema.table LIMIT 100;
```
```python
df = spark.table("onelake_fabric_catalog.schema.table")
df.display()
```
---
## Limitacions
- Només lectura
- No compatible amb SQL Warehouse Serverless
- Només Lakehouse i Warehouse
- Cal reinici després d’habilitar preview
---
## Referències
https://learn.microsoft.com/es-es/azure/databricks/query-federation/onelake
