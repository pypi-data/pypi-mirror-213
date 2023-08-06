import socket

import os
import zipfile
import json
import loggerutility as logger


def get_machine_ip():
    """
    Retrieve the current machine IP address

    :return: IP address
    """
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))

    return s.getsockname()[0]


def decompress_file(file_path, destination_dir):
    """
    Decompress zip/tar file at file_path to destination_dir

    :param file_path: Zip file path
    :param destination_dir: The directory to extract file
    """
    if not os.path.isfile(file_path):
        raise Exception('No file exists at location [{}]'.format(file_path))

    with zipfile.ZipFile(file_path, 'r') as zip_file:
        zip_file.extractall(destination_dir)


def search_recursive(directory, file_names):
    """
    Search file in given directory which is matched file_names, and return the absolute path of file

    :param directory: Directory to search file
    :param file_names: File names to match

    :return: A tuple,
              first value is bool, success or failure
              second value is absolute path of file, if found else None
    """
    if not os.path.exists(directory):
        return False, None

    index_files = [file.lower() for file in file_names]

    for directory_path, directory_names, files in os.walk(directory):
        for file in files:
            if file.lower() in index_files:
                return True, os.path.join(directory_path, file)

    return False, None

def getErrorXml(descr, trace, message=""):
    errorXml = '''<Root>
                    <Header>
                        <editFlag>null</editFlag>
                    </Header>
                    <Errors>
                        <error type="E">
                            <message><![CDATA['''+message+''']]></message>
                            <description><![CDATA['''+descr+''']]></description>
                            <trace><![CDATA['''+trace+''']]></trace>
                            <type>E</type>
                        </error>
                    </Errors>
                </Root>'''

    return errorXml

def getTraineModelPath(modelType, modelName, modelScope, enterprise_key=""):
        modelPath=""
        logger.log("inside getTraineModelPath","0")
        logger.log(f"modelScope 78::{modelScope}", "0")
        modelScope =  "global" if modelScope=="G" or modelScope=="global" or modelScope=="g" else "enterprise"
        logger.log(f"modelScope 80::{modelScope}", "0")
        if modelScope=="global":
            logger.log("inside getTraineModelPath if","0")
            modelPath = "/proteus-sense/trained_model/" + modelType.lower() + "/" + modelScope.lower() +  "/"+ modelName.lower()
        else:
            logger.log("inside getTraineModelPath else ","0")
            modelPath = "/proteus-sense/trained_model/" +  modelType.lower()  + "/" + modelScope.lower() + "/" + enterprise_key.lower() +  "/"+ modelName.lower()
        if not os.path.exists(modelPath):
            os.makedirs(modelPath)
            logger.log(f"inside getTraineModelPath modelPath::{modelPath}","0")
        return modelPath

def createModelScope(modelScope, modelType, modelName, enterprise_key=""):
        path = "/proteus-sense/trained_model"
        fileName = "modelScope.json"
        filePath = path + "/" + fileName
        if os.path.exists(filePath):
            logger.log(f"File already exists.","0")
        else:
            if not os.path.exists(path):
                os.makedirs(path)   
            with open (filePath,"w") as file:
                fileData={}
                fileData=str(fileData).replace("'", '"')
                logger.log(f"after{str(fileData)}","0")
                file.write(fileData)
                file.close()
                if os.path.exists(filePath):
                    logger.log(f"File created","0")

        with open (filePath,"r") as file:
            FilejsonData = file.read()
            file.close()
            logger.log(f"FilejsonData::{FilejsonData},{type(FilejsonData)}","0")

            modelScopefileJson=json.loads(FilejsonData)
            logger.log(f"parsedJsonData::{modelScopefileJson},{type(modelScopefileJson)}","0")
        
        if modelScope == "global":
            if modelType in modelScopefileJson:
                if modelScope in modelScopefileJson[modelType]:
                    if modelName not in modelScopefileJson[modelType][modelScope]:
                        modelScopefileJson[modelType][modelScope].append(modelName)
                    else:
                        logger.log(f"ModelName exists","0")
                    logger.log(f"if::{modelScopefileJson}","0")

                else:
                    modelScopefileJson[modelType][modelScope] = [modelName]
            else:
                modelScopefileJson[modelType] = {modelScope :[modelName]}
        
        elif modelScope == "enterprise":
            if modelType in modelScopefileJson:
                if modelScope in modelScopefileJson[modelType]:
                    if enterprise_key not in modelScopefileJson[modelType][modelScope]:
                        modelScopefileJson[modelType][modelScope][enterprise_key]=[modelName]
                    else:    
                        if not modelName in modelScopefileJson[modelType][modelScope][enterprise_key]:
                            modelScopefileJson[modelType][modelScope][enterprise_key].append(modelName)
                        else:
                            logger.log(f"ModelName exists","0")
                else:
                    modelScopefileJson[modelType][modelScope] = {enterprise_key:[modelName]}
            else:
                modelScopefileJson[modelType] = {modelScope: {enterprise_key:[modelName]}}
        else:
            logger.log(f"Invalid modelScope received:: {modelScope}","0")
        
        logger.log(f"data: {modelScopefileJson}","0")

        with open (filePath,"w") as file:
            logger.log(f"modelScopefileJson in write mode;::: {modelScopefileJson}","0")    
            modelScopefileJson=str(modelScopefileJson).replace("'", '"')
            logger.log(f"after line 1198 :: {str(modelScopefileJson)}","0")
            file.write(modelScopefileJson)
            file.close()
            logger.log(f"File updated","0")
        
        return "File Updated successfully "
    


