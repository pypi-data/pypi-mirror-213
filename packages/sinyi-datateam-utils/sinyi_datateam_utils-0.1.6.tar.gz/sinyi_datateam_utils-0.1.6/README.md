# Introduction 
Sinyi Datateam common module (for databricks environment)

# Version
Latest releases - https://pypi.org/project/sinyi-datateam-utils/

# Getting Started
1.	Installation process - Module has already installed in databricks cluster


# Use Guideline

## sinyi-utils module
module tree structure:
```
.
├── __init__.py
├── db_connector.py
└── format_tool.py
```

### format_tool
``` python
from sinyi_utils.format_tool import AESCrypto, roc_era_to_ad, Road8
```
1. AESCrypto: google decrypt & encrypt
    - method : same as sinyi module

2. roc_era_to_ad : transfer Chinese date to AD
    Example:
    ```python
    roc_era_to_ad('0801122')

    # Out: '19911122'
    ```
3. Road8
    ```python
    address='Address need to be normalize'
    response = Road8.normalize(address)
    ```
    response will get entire json from api
    
### db_connector
```python
from sinyi_utils.db_connector import upload_blob_from_memory, DW001Connector, AzureADSConnector...
```
1. MssqlConnector : connector to all kinds of db

#### method : query(query,database)
```python
# DW001Connector
query=  """
            TRUNCATE TABLE [TMP].[dbo].[TMP_SYNAPSE_PIPELINE_LOG_test]  
       """
DW001Connector.query(query,database='TMP')

# AzureADSConnector/AzureTMPConnector
query=  """
            DELETE FROM [dbo].[SA_GENE_LIST] WHERE GENE_ID='M106_P13af_a' and MOBILE_NO = 999999;
       """
AzureTMPConnector.query(query)
# out: 1 rows affected
```
#### method : connector(database)
```python 
# DW001Connector
query = '''
SELECT TOP(10)[AGEN_CUST_ID]
      ,[OBJ_ID]
      ,[RECE_ID]
      ,[TRADE_CATE]
      ,[CUST_CATE]
      ,[DEAL_DATE]

  FROM [DIM].[dbo].[DIM_CUSTOMER_DEAL_STATUS_DATE]
  
'''
df = pd.read_sql(query,DW001Connector.connector(database='DIM'))
# AzureADSConnector/AzureTMPConnector
query = '''
SELECT TOP (10) [MOBILE_NO]
      ,[GENE_VALUE]
  FROM [dbo].[SA_GENE_RESULT_OUTPUT]
  
'''
df = pd.read_sql(query,AzureADSConnector.connector())

```


# Contribute
TODO: Explain how other users and developers can contribute to make your code better. 

