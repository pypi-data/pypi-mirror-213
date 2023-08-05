import json
def get_max_properties_starting_with(id, prefix,LineageLogger):
    document=LineageLogger.query_graph("g.V().hasLabel('amlrun').has('id', '"+id+"')")
    jsondump = json.dumps(document)
    jsonload = json.loads(jsondump)
    for item in jsonload:
        properties = item.get('properties')
    if properties:
        matching_props = [prop[-1] for prop in properties.keys() if prop.startswith(prefix)]
        max_val = max(int(prop) for prop in matching_props) if matching_props else 0
    else:
        max_val = 0
    return str(max_val+1)

def read_from_adls_gen2(SOURCE_STORAGE_ACCOUNT_VALUE,\
                        AZURE_TENANT_ID,\
                        file_path,\
                        file_format,\
                        SOURCE_READ_SPN_VALUE,\
                        SOURCE_READ_SPNKEY_VALUE,\
                        RUN_ID,\
                        PIPELINE_STEP_NAME,\
                        LineageLogger):
    from pyspark.sql.session import SparkSession
    spark = SparkSession.builder.appName("Read from ADLS Gen2").getOrCreate()
    spark.conf.set("fs.azure.account.auth.type."+SOURCE_STORAGE_ACCOUNT_VALUE+".dfs.core.windows.net", "OAuth")
    spark.conf.set("fs.azure.account.oauth.provider.type."+SOURCE_STORAGE_ACCOUNT_VALUE+".dfs.core.windows.net",  "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
    spark.conf.set("fs.azure.account.oauth2.client.id."+SOURCE_STORAGE_ACCOUNT_VALUE+".dfs.core.windows.net", SOURCE_READ_SPN_VALUE)
    spark.conf.set("fs.azure.account.oauth2.client.secret."+SOURCE_STORAGE_ACCOUNT_VALUE+".dfs.core.windows.net", SOURCE_READ_SPNKEY_VALUE)
    spark.conf.set("fs.azure.account.oauth2.client.endpoint."+SOURCE_STORAGE_ACCOUNT_VALUE+".dfs.core.windows.net", "https://login.microsoftonline.com/"+AZURE_TENANT_ID+"/oauth2/token")

    df = spark.read.format(file_format).load(file_path)
    documentId = LineageLogger.query_graph("g.V().hasLabel('amlrun').has('RUN_ID', '"+RUN_ID+"').has('PIPELINE_STEP_NAME', '"+PIPELINE_STEP_NAME+"').values('id')")[0]
    sourcePostfix=get_max_properties_starting_with(documentId,"DataReadSourceColumns",LineageLogger)
    LineageLogger.update_vertex(documentId, {"DataReadSource_"+sourcePostfix: str(file_path),\
                                             "FileFormat_"+sourcePostfix:str(file_format),\
                                             "DataReadSourceColumns_"+sourcePostfix:"["+",".join(df.columns)+"]"})
    
    return df

def write_to_adls_gen2(SOURCE_STORAGE_ACCOUNT_VALUE,\
                       AZURE_TENANT_ID,\
                       file_path,\
                       file_format,\
                       repartition,\
                       partitionColumn,\
                       dynamicPartitionOverwriteMode,\
                       df,\
                       SOURCE_WRITE_SPN_VALUE,\
                       SOURCE_WRITE_SPNKEY_VALUE,\
                       RUN_ID,\
                       PIPELINE_STEP_NAME,\
                       LineageLogger):
    from pyspark.sql.session import SparkSession             
    spark = SparkSession.builder.appName("Read from ADLS Gen2").getOrCreate()
    spark.conf.set("fs.azure.account.auth.type."+SOURCE_STORAGE_ACCOUNT_VALUE+".dfs.core.windows.net", "OAuth")
    spark.conf.set("fs.azure.account.oauth.provider.type."+SOURCE_STORAGE_ACCOUNT_VALUE+".dfs.core.windows.net",  "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
    spark.conf.set("fs.azure.account.oauth2.client.id."+SOURCE_STORAGE_ACCOUNT_VALUE+".dfs.core.windows.net", SOURCE_WRITE_SPN_VALUE)
    spark.conf.set("fs.azure.account.oauth2.client.secret."+SOURCE_STORAGE_ACCOUNT_VALUE+".dfs.core.windows.net", SOURCE_WRITE_SPNKEY_VALUE)
    spark.conf.set("fs.azure.account.oauth2.client.endpoint."+SOURCE_STORAGE_ACCOUNT_VALUE+".dfs.core.windows.net", "https://login.microsoftonline.com/"+AZURE_TENANT_ID+"/oauth2/token")
    
    documentId = LineageLogger.query_graph("g.V().hasLabel('amlrun').has('RUN_ID', '"+RUN_ID+"').has('PIPELINE_STEP_NAME', '"+PIPELINE_STEP_NAME+"').values('id')")[0]
    targetPostfix=get_max_properties_starting_with(documentId,"DataWriteColumns",LineageLogger)
    LineageLogger.update_vertex(documentId, {"DataWriteTarget_"+targetPostfix: str(file_path),\
                                        "FileFormat_"+targetPostfix:file_format,\
                                        "DataWriteColumns_"+targetPostfix:"["+",".join(df.columns)+"]"})
    
    if dynamicPartitionOverwriteMode:
        spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
    
    if repartition is None:
        if partitionColumn:
            #partitionColumn accepted as list of columns
            df.write.format(file_format).partitionBy(partitionColumn).mode("overwrite").save(file_path)
        else: 
            df.write.format(file_format).mode('overwrite').save(file_path)
    else:
        if partitionColumn:
            df.repartition(repartition).write.format(file_format).partitionBy(partitionColumn).mode("overwrite").save(file_path)
        else:
            df.repartition(repartition).write.format(file_format).mode('overwrite').save(file_path)
    return

def read_from_kusto(kustoOptions,RUN_ID,PIPELINE_STEP_NAME,LineageLogger):
    from pyspark.sql.session import SparkSession
    pyKusto = SparkSession.builder.appName("kustoPySpark").getOrCreate()
    kustoDf  = pyKusto.read. \
                format("com.microsoft.kusto.spark.datasource"). \
                option("kustoCluster", kustoOptions["kustoCluster"]). \
                option("kustoDatabase", kustoOptions["kustoDatabase"]). \
                option("kustoQuery", kustoOptions["kustoTable"]). \
                option("kustoAadAppId", kustoOptions["kustoAADClientID"]). \
                option("kustoAadAppSecret", kustoOptions["kustoClientAADClientPassword"]). \
                option("kustoAadAuthorityID", kustoOptions["kustoAADAuthorityID"]). \
                load()
    
    documentId = LineageLogger.query_graph("g.V().hasLabel('amlrun').has('RUN_ID', '"+RUN_ID+"').has('PIPELINE_STEP_NAME', '"+PIPELINE_STEP_NAME+"').values('id')")[0]
    sourcePostfix=get_max_properties_starting_with(documentId,"DataReadSourceColumns",LineageLogger)
    LineageLogger.update_vertex(documentId, {"KustoDataReadCluster_"+sourcePostfix: str(kustoOptions["kustoCluster"]),\
                                        "KustoDataReadDatabase_"+sourcePostfix: str(kustoOptions["kustoDatabase"]),\
                                        "KustoDataReadQuery_"+sourcePostfix: str(kustoOptions["kustoTable"]),\
                                        "DataReadSourceColumns_"+sourcePostfix:"["+",".join(kustoDf.columns)+"]"})                
    return kustoDf

def read_from_azsql(SQL_SERVER_INSTANCE,access_token,Query,RUN_ID,PIPELINE_STEP_NAME,LineageLogger):
    from pyspark.sql.session import SparkSession
    pySql = SparkSession.builder.appName("AzSQLPySpark").getOrCreate()
    df = pySql.read \
        .format("com.microsoft.sqlserver.jdbc.spark") \
        .option("url", SQL_SERVER_INSTANCE) \
        .option("query", Query) \
        .option("accessToken", access_token) \
        .option("encrypt", "true") \
        .option("hostNameInCertificate", "*.database.windows.net") \
        .load()

    documentId = LineageLogger.query_graph("g.V().hasLabel('amlrun').has('RUN_ID', '"+RUN_ID+"').has('PIPELINE_STEP_NAME', '"+PIPELINE_STEP_NAME+"').values('id')")[0]
    sourcePostfix=get_max_properties_starting_with(documentId,"DataReadSourceColumns",LineageLogger)
    LineageLogger.update_vertex(documentId, {"SqlDataReadServer_"+sourcePostfix: str(SQL_SERVER_INSTANCE),\
                                        "SqlDataReadQuery_"+sourcePostfix: str(Query),\
                                        "DataReadSourceColumns_"+sourcePostfix:"["+",".join(df.columns)+"]"})  
    return df