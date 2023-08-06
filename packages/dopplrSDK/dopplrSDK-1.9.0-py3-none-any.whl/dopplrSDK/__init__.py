import pandas as pd
import psycopg2
import sys
import boto3
import json
import os



def putFileTomywrkspace(filePath,file_type,loginName):
    try:
        query="select DOR.\"OrgName\",Du.\"UserKey\",DOR.\"ContainerName\",DOR.\"AwsAccessKey\",DOR.\"AwsSecretKey\" FROM doppler.\"DopplerUser\" Du join doppler.\"DopplerOrg\" DOR on DOR.\"OrgId\"=Du.\"OrgId\" where Du.\"LoginName\"="+"'"+loginName+"'"+""
        #print(query)
        cnxn = psycopg2.connect(host='adb63cdf19ef14e14b3e7ffd2c4bd4e3-1623479541.ap-south-1.elb.amazonaws.com',database='Dopplr',user='postgres',password='SystechIndia@123',port='5432')

        cur=cnxn.cursor()
        cur.execute(query)
        results = cur.fetchone()
        

        ContainerName=results[2]
        AwsAccessKey=results[3]
        AwsSecretKey=results[4]
        UserKey=results[1]
        OrgName=results[0]
        
        s3 = boto3.client('s3', aws_access_key_id=AwsAccessKey, aws_secret_access_key=AwsSecretKey)

        cur=cnxn.cursor()
        file_name = os.path.basename(filePath)
        insert_query = "INSERT INTO doppler.\"DopplerLake\"(\"UserKey\", \"TableName\",\"ResourceType\",\"DopplerConnectionDetailsKey\",\"Projectid\",\"Status\") VALUES ("+str(UserKey)+",'"+file_name+"','"+file_type+"',null,'','Uploaded')"

        cur.execute(insert_query)


        cnxn.commit()
        
        cur1=cnxn.cursor()
        insert_query1 = "SELECT max(\"SourceKey\") as \"SourceKey\" FROM doppler.\"DopplerLake\" where \"UserKey\"="+str(UserKey)+" and \"TableName\"='"+file_name+"'"
        
        cur1.execute(insert_query1)
        results = cur1.fetchone()
        SourceKey=results[0]
        SourceKey=str(SourceKey)


        ConnectionString = str(OrgName)+"/"+str(loginName).upper()+"/"+(str(SourceKey).lstrip()+'/SOURCE/'+file_name)

        update_query = "UPDATE doppler.\"DopplerLake\" set \"ConnectionString\"='"+str(OrgName)+"/"+str(loginName).upper()+'/'+(str(SourceKey).lstrip()+'/SOURCE/'+file_name+".csv',\"Source\"= 'MLStudio' ,\"CreatedTs\"=CURRENT_TIMESTAMP where \"SourceKey\"="+str(SourceKey))
        cur2=cnxn.cursor()
        #print("update_query ",update_query)
        cur2.execute(update_query)
        cnxn.commit()

        s3.upload_file(filePath, ContainerName, ConnectionString)

         # Generate a pre-signed URL
        
        s3.put_object_acl(ACL='public-read',
                          Bucket=ContainerName,
                          Key=ConnectionString)
        #url = f"https://{ContainerName}.s3.ap-south-1.amazonaws.com/{ConnectionString}"
        url = f"s3://{ContainerName}/{ConnectionString}"
        print("uri : ",url)
        cnxn.close()
        #print("done")
    except Exception as error:
        if 'NoneType' in str(error):
            dopplrsource= 'File does not exists'
            print("Error : ", dopplrsource)
            sys.exit()
        else:
            print("Error : ",error)


def getWorkspaceFile(fileName,destination,loginName):
    #type = 1 then get file (Actual file) 
    #type = 2 then get file* (file pattern)


    #destination = "/data"
    folder_prefix = 'Systech/'+loginName.upper()+'/'
    query="select DOR.\"OrgName\",Du.\"UserKey\",DOR.\"ContainerName\",DOR.\"AwsAccessKey\",DOR.\"AwsSecretKey\" FROM doppler.\"DopplerUser\" Du join doppler.\"DopplerOrg\" DOR on DOR.\"OrgId\"=Du.\"OrgId\" where Du.\"LoginName\"="+"'"+loginName+"'"+""

    cnxn = psycopg2.connect(host='adb63cdf19ef14e14b3e7ffd2c4bd4e3-1623479541.ap-south-1.elb.amazonaws.com',database='Dopplr',user='postgres',password='SystechIndia@123',port='5432')

    cur=cnxn.cursor()
    cur.execute(query)
    results = cur.fetchone()
        

    ContainerName=results[2]
    AwsAccessKey=results[3]
    AwsSecretKey=results[4]
    UserKey=results[1]
    OrgName=results[0]
        
    s3 = boto3.client('s3', aws_access_key_id=AwsAccessKey, aws_secret_access_key=AwsSecretKey)

    # Check if the file exists
    if os.path.exists(destination):
        print('folder exists')
    else:
        os.mkdir(destination)

    response = s3.list_objects_v2(Bucket=ContainerName, Prefix=folder_prefix)
    # Iterate through the objects
    destination=destination+'/'+fileName
    for obj in response['Contents']:
        key = obj['Key']
        #print(key,fileName)
            
        is_same = is_file_name_same(key, fileName)

        if(is_same):                
            s3.download_file(ContainerName, key, destination)

def is_file_name_same(file_path, expected_file_name):
        file_name = os.path.basename(file_path)
        return file_name == expected_file_name


#putFileTomywrkspace("C:\\Users\\JakeerAhamedShaik\\Downloads\\Forecasting.csv",'csv',"Anand")

#getWorkspaceFile("Transaction","C:\\Users\\AnandThirurangaruban\\Documents\\dopplrSDK","Anand")

