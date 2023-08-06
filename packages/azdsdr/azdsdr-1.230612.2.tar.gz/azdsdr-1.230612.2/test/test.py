#%% load module
import sys
sys.path.append(r"D:\az_git_folder\azdsdr\src")

#%% 
from azdsdr.readers import DremioReader
username    = "anzhu@microsoft.com"
dr = DremioReader(username=username)


#%% run another test
query_sql   = """SELECT * FROM Azure.PPE."vw_customer_azure_monthlyusage " LIMIT 10"""
r           = dr.run_sql(query_sql)
display(r)

#%% 
sql = '''
select 
    * 
from 
    BizApps.PROD."vw_customer_powerapps_portalusage"
limit 10
'''
r = dr.run_sql(sql)
display(r)

#%% test Kusto Reader
from azdsdr.readers import KustoReader

cluster = "https://cgadataout.kusto.windows.net"
db      = "pii"
kr = KustoReader(cluster=cluster,db=db)

#%% test list all tables 
kr.list_tables(folder_name='prodev')

#%% 
kql = '''
cluster('Cgadataout').database('Starlight').FACT_ACR_Publish
| where 1==1
    and DIM_DateId < 20220901
    and DIM_DateId > 20210701
    and DIM_ACRAdjustmentTypeId == -686078934765504679
| summarize  
    ACR_sum = round(sum(ACR),0)
    by DIM_DateId
| order by DIM_DateId asc
'''
r = kr.run_kql(kql)
display(r)
r.plot()

#%% public sample 
from azdsdr.readers import KustoReader

cluster = "https://help.kusto.windows.net"
db      = "Samples"
kr = KustoReader(cluster=cluster,db=db)

#%% 
kql = "StormEvents | take 10"
r = kr.run_kql(kql)
display(r)

#%% test scope
# cosmos wiki: https://mscosmos.visualstudio.com/CosmosWiki/_wiki/wikis/Cosmos.wiki/3095/Pyscope-Code-Sample
import sys
sys.path.append(r"F:\az_git_folder\azdsdr\src")
from azdsdr.readers import CosmosReader

scope_exe_path      = r"D:\tools\ScopeSDK\Scope.exe"
scope_script        = "pa_daily_makers.script"
vc_path             = r"vc://cosmos11/AzureInsights.analytics"
account             = r"anzhu@microsoft.com"

cr                  = CosmosReader(scope_exe_path,account,vc_path)

#%% cosmos delete file test
file_path = "/users/anzhu/scope_query_temp.ss"
cr.delete_file_from_cosmos(file_path)

#%% run scope script
output_str = cr.run_scope(scope_script)
cr.check_job_status(output_str)

#%% download file from cosmos
source = "/users/anzhu/daily_makers.ss"
target = "./data/daily_makers.csv"

cr.download_file_as_csv(source,target)

#%% 
u_sql = '''
// Module references        
MODULE @"/shares/AzureAnalytics.Prod/Sdk/AzureAnalytics1.5.module" AS AzureAnalytics;   // Production location
   
#DECLARE cloudName                   string   = "public";
#DECLARE WorkloadEnvironment         string   = "Prod";

#DECLARE startDateTime string = "2022-09-07T00:00:00"; //DateTime.Parse("2020/09/25"); 
#DECLARE endDateTime string = "2022-09-13T00:00:00"; //DateTime.Parse("2020/09/26"); 

// Set the user details version. 
// This is the suffix added to the PowerApps.Telemetry.ActiveDailyUserDetailsV# (where # is the userDetailsVersion) 
// When the details version changes, just change it here!
#DECLARE userDetailsVersion string = "2";

#IF (@WorkloadEnvironment != "Prod")   
    #DECLARE prefixEntity string = @WorkloadEnvironment;
#ELSE
    #DECLARE prefixEntity string = "";
#ENDIF

#IF (@cloudName.ToLower() != "public")   // This is only for the current rest of world. When RoW migrates to Blueshift then the code will always be: prefixEntity = @prefixEntity+"."+ @cloudName;
    #IF (@prefixEntity != "")
    	#SET prefixEntity = @prefixEntity+"."+ @cloudName;
    #ELSE
    	#SET prefixEntity = @cloudName;
    #ENDIF
#ENDIF 

#IF (@prefixEntity != "")
        #DECLARE dailyActiveUserDetailsInputEntity string  = @prefixEntity+".PowerApps.Telemetry.ActiveDailyUserDetailsV" + @userDetailsVersion;   
#ELSE
        #DECLARE dailyActiveUserDetailsInputEntity string  = "PowerApps.Telemetry.ActiveDailyUserDetailsV" + @userDetailsVersion;
#ENDIF
        
AzureAnalytics.Initialize(entity = @dailyActiveUserDetailsInputEntity); 

curr_activeUser =    
    SELECT 
        TOP 10000
         activeUserDate     AS activeUserDate
        ,TenantID           AS TenantID
        ,TenantCountryCode  AS TenantCountryCode
        ,UserID             AS UserID
        ,UserIDType         AS UserIDType
        ,clientSessionId    AS clientSessionId
        ,eventPersona       AS eventPersona
        ,applicationType    AS applicationType
        ,userLicense        AS userLicense                
        ,applicationId      AS applicationId
        ,DeviceType         AS DeviceType
        ,deviceMake         AS deviceMake
        ,browserName        AS browserName
        ,OSType             AS OSType  
        ,JoinDate           AS JoinDate
        FROM 
        (AzureAnalytics.LoadStream
            (
                 startDateTime  = @startDateTime
                ,endDateTime    = @endDateTime
                ,entity         = @dailyActiveUserDetailsInputEntity
            )
        );

OUTPUT curr_activeUser
TO SSTREAM @output;
'''
r = cr.scope_query(scope_script=u_sql)
display(r)


#%% kusto ingest
import sys
sys.path.append(r"F:\az_git_folder\azdsdr\src")
import azdsdr.readers as dsdr
import importlib
importlib.reload(dsdr)
from azdsdr.readers import KustoReader

cluster         = "https://cgadataout.kusto.windows.net"
db              = "CGAWorkArea"
ingest_cluster  = r"https://ingest-cgadataout.kusto.windows.net"
kr              = KustoReader(cluster=cluster,db=db,ingest_cluster_str=ingest_cluster)

#%%
kql = '''
pa_makers_test | take 10
'''
r = kr.run_kql(kql)
display(r)

#%% ingest data 
import pandas as pd
target_table = 'pa_makers_test'
df = pd.read_csv("temp_query_data.csv")
kr.upload_to_kusto(target_table,df)

#%%
target_table = 'pa_makers_test'
kr.check_table_data(target_table)

#%% BLob test
import sys
sys.path.append(r"F:\az_git_folder\azdsdr\src")
from azdsdr.readers import AzureBlobReader

connect_str         = "DefaultEndpointsProtocol=https;AccountName=cedssparkstorage;AccountKey=AK054WvhVssGGpmGyLiZ8em5FhzQ6z6UmloFE6DM5dXQN2iJ30pP9x0jard+BCITJNVZU6JqTWO+EYCLw0zoxg==;EndpointSuffix=core.windows.net"
container           = "andrewzhu"
abr = AzureBlobReader(blob_conn_str=connect_str,container_name=container)

#%% blob upload test
import time
blob_file_path      = r'powerapps_data/pa_daily_temp.csv'
local_csv_path      = r'data/scope_query_temp.csv'
s = time.time()
abr.upload_file_chunks(blob_file_path=blob_file_path,local_file_path=local_csv_path)
print('done, use time',(time.time() -s))


#%% download test
blob_file_path = 'temp_query_data.csv'
local_file_path = 'test.csv'
abr.download_file(blob_file_path,local_file_path)


#%% upload test
#sas_token = abr.get_blob_sas_url()
# the working version:
# https://cedssparkstorage.blob.core.windows.net/andrewzhu/temp_query_data.csv?sv=2021-04-10&st=2022-10-05T04%3A29%3A18Z&se=2023-01-06T05%3A29%3A00Z&sr=b&sp=r&sig=sHWYA4IAyuRUGYS611aO0vXcijZD%2FY0WqwjzCPtzq0U%3D
# sas token: 
# se=2023-01-13T17%3A12%3A22Z&sp=r&sv=2021-08-06&ss=b&srt=o&sig=sWxAukkF7p%2B3DhfyNTkrfAQKSC5NxWsaMM8xbLD82L4%3D
url = r'''https://cedssparkstorage.blob.core.windows.net/andrewzhu/temp_query_data.csv?se=2023-01-13T17%3A12%3A22Z&sp=r&sv=2021-08-06&ss=b&srt=o&sig=sWxAukkF7p%2B3DhfyNTkrfAQKSC5NxWsaMM8xbLD82L4%3D'''

#%% test get blob sas url
blob_file_path = 'temp_query_data.csv'
url = abr.get_blob_sas_url(blob_file_path)
print(url)

#%% upload file test 
blob_file_path = 'upload_test.csv'
local_file_path = 'temp_query_data_2.csv'
abr.upload_file(blob_file_path=blob_file_path,local_file_path=local_file_path)
print('done')

#%% delete blob file test
blob_file_path = 'upload_test.csv'
abr.delete_blob_file(blob_file_path)
print('done')

#%% test kusto table exist
table_name = 'pa_makers_test2'
r = kr.is_table_exist(table_name)
print(r)

#%% test kusto delete
table_name = 'pa_makers_test'
output_str = kr.drop_table(table_name)
print(output_str)


#%% test create table from csv
kusto_table_name = 'pa_makers_test'
csv_file_path = 'temp_query_data.csv'
folder = 'anzhu/test'
r = kr.create_table_from_csv(kusto_table_name,csv_file_path,kusto_folder=folder)
print(r)


#%% raw string to string
raw_str = r'''
//Script GUID:55667bda-5bde-471d-81a4-31a1246ae184\r\n//Used for tracking history\r\n//Script GUID:1ded5fb3-edf9-4aa0-a468-6aef1eec71c6\r\n/************************************************************************************************\r\nPurpose:\r\nMonthly metrics aggregated by TenantID. Provides:\r\n    Standalone_MAU              Canvas_User_MAU\r\n    Canvas_MAU                  Canvas_Maker_MAU\r\n    ModelDrivenApps_MAU         Model_User_MAU\r\n    TeamsDrivenApps_MAU         Model_Maker_MAU\r\n    Standalone_User_MAU         Teams_User_MAU           \r\n    Standalone_Maker_MAU        Canvas_Production_Maker_MAU\r\n    All_User_MAU                Model_Production_Maker_MAU\r\n    All_Maker_MAU               Total_Production_Maker_MAU \r\n\r\nScript flow summary:\r\n1.    Get usage data for last 28 days from vw_IdentifyStandaloneActiveUsersByPeriod    \r\n2.    Calculate AppMAU and apply IsProductionFlag\r\n3.    Join all that to Filters for Test Tenants and internal tenants\r\n4.    Calculate the final aggregations\r\n\r\nOutput Streams:\r\nBAG.PowerCAT.PowerAppsUsage.Detailed.AggregatedByTenantByDate\r\n\r\nName of job in Lens Explorer:\r\n    PowerApps_Detailed_AggregatedByTennant\r\nDevOps Ticket\r\nhttps://msazure.visualstudio.com/One/_queries/edit/13795949/?triage=true\r\n\r\nAuthor          Date        Change\r\nv-mikeinman     3/19/2022   Creation\r\nV-guptavinay    06/14/2022  Modified\r\n\r\n*********************************************************/\r\n\r\nMODULE @\"/shares/AzureAnalytics.Prod/Sdk/AzureAnalytics1.5.module\" AS AzureAnalytics;\r\nMODULE \"/shares/asimov.prod.data/AsimovApi/v3/Asimov.Batch.module\";\r\nMODULE @\"/shares/AzureAnalytics.Partner.AAPT/BAPICommon/PowerApps/PowerApps.Telemetry.StandaloneUsersViewsV1.module\" AS StandaloneUsersViews;\r\nREFERENCE @\"/local/AAPTIgnition/Binaries/Azure.IgnitionData.dll\";\r\nUSING Azure.IgnitionData;\r\n\r\n\r\n#DECLARE WorkloadEnvironment string = \"Prod\";\r\n#DECLARE cloudName string = \"public\"; \r\n#DECLARE serviceOid string = \"e509ba3a-dd18-4324-99dc-71651f4f238e\";\r\n\r\n#DECLARE StartDate DateTime = DateTime.Parse(@@startDateTime@@);\r\n#DECLARE StartDateStr string = @StartDate.ToString(\"yyyy-MM-dd\");\r\n\r\n#DECLARE StartDate28Days DateTime = DateTime.Parse(@StartDateStr).AddDays( - 27);\r\n#DECLARE StartDate28DaysStr string = @StartDate28Days.ToString(\"yyyy-MM-dd\");\r\n\r\n#DECLARE EndDate28Days DateTime = DateTime.Parse(@StartDateStr).AddDays(1);\r\n#DECLARE EndDateStr string = @EndDate28Days.ToString(\"yyyy-MM-dd\");\r\n\r\n//Pull metadata: TPID to AAD Tenant ID mapping AND list of internal AND test tenants.\r\nInternalTenants =\r\n    AzureAnalytics.LoadSnapshot\r\n    (\r\n        entity = \"BAPI.ODIN.ODINTInternalExternalTenants\"\r\n    );\r\n\r\nmapTenantTPID =\r\n    AzureAnalytics.LoadSnapshot\r\n    (\r\n        entity = \"AllTenants.mapTenantTPID_AllTPIDs\"\r\n    );\r\n\r\n// We keep TPIds with IsWinner = 1\r\nmapTenantTPID =\r\n    SELECT DISTINCT TenantId AS TenantId,\r\n                    TPId\r\n    FROM mapTenantTPID\r\n    WHERE IsWinner == 1;\r\n\r\nTenants =\r\n    SELECT  DISTINCT TenantId AS TenantId,\r\n            IsTestTenant,\r\n            IsInternal\r\n    FROM InternalTenants;\r\n\r\n//Pull data from combined Cosmos view\r\nUsage =\r\n    SELECT DISTINCT activeUserDate AS Date,\r\n           UserID AS UserID,\r\n           UserIDType AS UserIDType,\r\n           IsGuid(TenantID) ?Guid.Parse(TenantID) : Guid.Empty AS  TenantID,\r\n           eventPersona AS Persona,\r\n           applicationId AS applicationId,\r\n           clientSessionId AS clientSessionId,\r\n           applicationType AS Platform\r\n    FROM\r\n    (\r\n        StandaloneUsersViews.vw_IdentifyStandaloneActiveUsersByPeriod\r\n        (\r\n            startDateTime = @StartDate28DaysStr,\r\n            endDateTime = @EndDateStr,\r\n            WorkloadEnvironment = @WorkloadEnvironment,\r\n            cloud = @cloudName\r\n        )\r\n    );\r\n\r\n\r\n//calculate App MAU  Production flag = App MAU >=5 or Session Count >=50\r\nappMAU =\r\n    SELECT TenantID,\r\n           applicationId,\r\n           COUNT(DISTINCT UserID) AS app_MAU,\r\n           COUNT( * ) AS session_count,\r\n           COUNT(DISTINCT UserID) >= 5 || COUNT( * ) >= 50? \"TRUE\" : \"FALSE\" AS IsProductionFlag\r\n    FROM Usage\r\n    GROUP BY TenantID,\r\n             applicationId;\r\n\r\n// Loading necessary columns, joining usage data with metadata.\r\n//2. Get App MAU and App Session Count\r\n//aggreage userid left join to primary table based on tenantID and ResourceId(applicationType)\r\nUsageData =\r\n    SELECT DISTINCT @StartDate AS ActivityDate,\r\n                    U.TenantID,\r\n                    U.Persona AS Persona,\r\n                    U.Platform AS Platform,\r\n                    M.TPId,\r\n                    A.IsProductionFlag,\r\n                    (T.IsTestTenant == true? \"Yes\" : \"No\") AS IsTestTenant,\r\n                    (T.IsInternal == true? \"Yes\" : \"No\") AS IsInternal,\r\n                    U.UserID\r\n    FROM Usage AS U\r\n         LEFT OUTER JOIN Tenants AS T ON U.TenantID == T.TenantId\r\n         LEFT OUTER JOIN mapTenantTPID AS M ON T.TenantId == M.TenantId\r\n         LEFT OUTER JOIN appMAU AS A ON T.TenantId == A.TenantID AND U.applicationId == A.applicationId;\r\n\r\nAggregatedByTenant =\r\n    SELECT ActivityDate                                                                                                                      AS ActivityDate,\r\n           TenantID                                                                                                                          AS TenantId,\r\n           28                                                                                                                                AS InternalProductId,\r\n           COUNT(DISTINCT UserID)                                                                                                            AS Standalone_MAU,\r\n           COUNT(DISTINCT (CASE WHEN Platform == \"CANVAS\" THEN UserID ELSE NULL END))                                                        AS Canvas_MAU,\r\n           COUNT(DISTINCT (CASE WHEN Platform == \"MODEL\"  THEN UserID ELSE NULL END))                                                        AS ModelDrivenApps_MAU,\r\n           COUNT(DISTINCT (CASE WHEN Platform == \"TEAMS\"  THEN UserID ELSE NULL END))                                                        AS TeamsDrivenApps_MAU,\r\n           COUNT(DISTINCT (CASE WHEN Persona  == \"USER\"   THEN UserID ELSE NULL END))                                                        AS Standalone_User_MAU,\r\n           COUNT(DISTINCT (CASE WHEN Persona  == \"MAKER\"  THEN UserID ELSE NULL END))                                                        AS Standalone_Maker_MAU,\r\n           COUNT(DISTINCT (CASE WHEN Persona == \"POTENTIAL USER\" OR Persona == \"USER\"  THEN UserID ELSE NULL END))                           AS All_User_MAU,\r\n           COUNT(DISTINCT (CASE WHEN Persona == \"POTENTIAL MAKER\" OR Persona == \"MAKER\"  THEN UserID ELSE NULL END))                         AS All_Maker_MAU,\r\n           COUNT(DISTINCT (CASE WHEN Platform == \"CANVAS\" AND Persona == \"USER\"  THEN UserID ELSE NULL END))                                 AS Canvas_User_MAU,\r\n           COUNT(DISTINCT (CASE WHEN Platform == \"CANVAS\" AND Persona == \"MAKER\" THEN UserID ELSE NULL END))                                 AS Canvas_Maker_MAU,\r\n           COUNT(DISTINCT (CASE WHEN Platform == \"MODEL\"  AND Persona == \"USER\"  THEN UserID ELSE NULL END))                                 AS Model_User_MAU,\r\n           COUNT(DISTINCT (CASE WHEN Platform == \"MODEL\"  AND Persona == \"MAKER\" THEN UserID ELSE NULL END))                                 AS Model_Maker_MAU,\r\n           COUNT(DISTINCT (CASE WHEN Platform == \"TEAMS\"  AND Persona == \"USER\"  THEN UserID ELSE NULL END))                                 AS Teams_User_MAU,\r\n           COUNT(DISTINCT (CASE WHEN Platform == \"TEAMS\"  AND Persona == \"MAKER\" THEN UserID ELSE NULL END))                                 AS Teams_Maker_MAU,           \r\n           COUNT(DISTINCT (CASE WHEN Platform == \"CANVAS\"  AND Persona == \"MAKER\" AND IsProductionFlag == \"TRUE\" THEN UserID ELSE NULL END)) AS Canvas_Production_Maker_MAU,\r\n           COUNT(DISTINCT (CASE WHEN Platform == \"MODEL\"  AND Persona == \"MAKER\"  AND IsProductionFlag == \"TRUE\" THEN UserID ELSE NULL END)) AS Model_Production_Maker_MAU,\r\n           COUNT(DISTINCT (CASE WHEN Persona == \"MAKER\" AND IsProductionFlag == \"TRUE\" THEN UserID ELSE NULL END))                           AS Total_Production_Maker_MAU\r\n    FROM UsageData\r\n    WHERE  IsTestTenant == \"No\";\r\n\r\nAzureAnalytics.PublishStream\r\n(\r\n    entity = \"BAG.PowerCAT.PowerAppsUsage.Detailed.AggregatedByTenant\",\r\n    startDateTime = @StartDate.ToString(\"yyyy-MM-dd\"),\r\n    periodInMinutes = \"1440\",\r\n    input = AggregatedByTenant,\r\n    expiryInDays = \"1095\",\r\n    publishToPrivateVC = true,\r\n    privateVCOutputPathInShares = \"AzureInsights/PowerCAT/Usage/\" ,  \r\n    serviceOid = @serviceOid,\r\n    InGDPRScope = false,\r\n    clusteredBy=\"TenantId\"\r\n);\r\n\r\n\r\n#CS\r\n             \r\n    public static bool IsGuid(string value)\r\n    {\r\n        Guid x;\r\n        return Guid.TryParse(value, out x);\r\n    }\r\n\r\n#ENDCS
'''

import codecs

new_str = codecs.decode(raw_str,'unicode_escape')
print(new_str)


#%% read file test
#file_path = r'C:\Users\xhink\.azdsdr_conf.json'
file_path = r'C:\\Users\\xhink\\.azdsdr_conf.json'
with open(file_path,'w') as f:
    print('going to write something')
#print(content)


#%% test writing data
from azdsdr.readers import update_config

key = 'test_key'
value = 'test_value'
update_config(key=key,value=value)

