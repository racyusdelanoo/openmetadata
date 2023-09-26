# -*- coding: utf-8 -*-}

import json 

#Connection 
from metadata.generated.schema.entity.services.connections.metadata.openMetadataConnection import (
    OpenMetadataConnection,
)

from metadata.generated.schema.security.client.openMetadataJWTClientConfig import (
        OpenMetadataJWTClientConfig,
)

#Openmetadata API
from metadata.ingestion.ometa.ometa_api import OpenMetadata

#Database Service
from metadata.generated.schema.api.services.createDatabaseService import (
    CreateDatabaseServiceRequest,
)

from metadata.generated.schema.entity.services.connections.database.customDatabaseConnection import (
    CustomDatabaseConnection,
)

from metadata.generated.schema.entity.services.databaseService import (
    DatabaseConnection,
    DatabaseService,
    DatabaseServiceType,
)

#Database 
from metadata.generated.schema.entity.data.database import Database
from metadata.generated.schema.api.data.createDatabase import CreateDatabaseRequest

#Schema 
from metadata.generated.schema.entity.data.databaseSchema import DatabaseSchema
from metadata.generated.schema.api.data.createDatabaseSchema import (
   CreateDatabaseSchemaRequest,
)

#Table 
from metadata.generated.schema.entity.data.table import Column, DataType, Table
from metadata.generated.schema.api.data.createTable import CreateTableRequest

jwt_token='eyJraWQiOiJHYjM4OWEtOWY3Ni1nZGpzLWE5MmotMDI0MmJrOTQzNTYiLCJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJvcGVuLW1ldGFkYXRhLm9yZyIsInN1YiI6ImluZ2VzdGlvbi1ib3QiLCJlbWFpbCI6ImluZ2VzdGlvbi1ib3RAb3Blbm1ldGFkYXRhLm9yZyIsImlzQm90Ijp0cnVlLCJ0b2tlblR5cGUiOiJCT1QiLCJpYXQiOjE2OTU2NTcwNDksImV4cCI6bnVsbH0.OSYzmvRHspjebmdOTWUNFZ-fmsDhBxHUDy_kRKf8J9OdJKk8Rsh2skwubVHHNFJZJweKNQSkpF6Wmm36w9R__XdEU1RtG9ocVQfpEUgboItNeN5lDDj1mRthMU8JEvUU5tsEYSCvMDsYpqWlzfB-F636MhWdUe8slmYlXLq4SF3UVvmfcdJh4PPIEMcmlp7SsX8pjScbKiU9RMQG0op4Eu91le22gUaSkyau2eYxFl8EnCmNV5wXhbMx5Emxv8oR2FXKq9VZEwYyQaMMWsk79Peu7UHzl_x3rq3YPw1ECWL0TXvg_QFMfpi_Z-3Lej_vEztXC38eTHTxFfZJewxjeQ'

server_config = OpenMetadataConnection(
    hostPort="http://localhost:8585/api",
    authProvider="openmetadata",
    securityConfig=OpenMetadataJWTClientConfig(
        jwtToken=jwt_token
    ),
)

database_connection_config = {
    "username": "root",
    "password": "lemon",
    "hostPort": "http://10.5.5.41:3308", 
}

entity_type = {
                "DatabaseService": DatabaseService,  
                "Database": Database, 
                "DatabaseSchema": DatabaseSchema,
                "Table": Table,
              }

def serialize_json(data): 
   fields = [] 
   
   for index in range(len(data)):
      id          = str(data[index].id.__root__)
      name        = data[index].name.__root__
      fqn         = data[index].fullyQualifiedName.__root__
      serviceType = str(data[index].serviceType)
      description = str(data[index].description)
      tags        = [data[index].tags]
      fields.append([id, name, fqn, serviceType, description, tags])   
   result = [{'id': i, 'name': n, 'fullyQualifiedName': fqn, 'serviceType': st, 
            'description': d, 'tags': t} 
            for i, n, fqn, st, d, t in fields]   
   return result

def connection(): 
   metadata = OpenMetadata(server_config)
   return metadata

def create_database_service(metadata, db_service_name): 
   db_service = CreateDatabaseServiceRequest(
       name=db_service_name,
       serviceType=DatabaseServiceType.CustomDatabase,  
       connection=DatabaseConnection(    
           config=CustomDatabaseConnection(
           type="CustomDatabase",       
           sourcePythonClass="MysqlConnection",               
           connectionOptions=database_connection_config,    
       )
     ),
   ) 
   return metadata.create_or_update(data=db_service)

def create_database(metadata, db_service, db_name): 
   database = CreateDatabaseRequest(
               name=db_name,
               service=db_service,
   )
   return metadata.create_or_update(data=database)

def create_schema(metadata, database, schema_name):
   schema = CreateDatabaseSchemaRequest(
             name=schema_name,
             database=database, 
   )
   return metadata.create_or_update(schema)

def create_table(metadata, table, schema_name):
    mtable = CreateTableRequest(
              name=table['name'], 
              databaseSchema=schema_name,  
              columns=[Column(name=col, 
                              dataType=DataType(dtype), 
                              constraint=const 
                             )
                             for (col, dtype, const) in zip(table['columns'], table['datatypes'], table['constraints']) 
                      ], 
              )
    return metadata.create_or_update(data=mtable)

def list_entities(metadata, entity_type): 
   return metadata.list_entities(entity=entity_type).entities

def get_entity_by_name(metadata, entity_type, fqn):
   return [metadata.get_by_name(entity=entity_type, fqn=fqn)]

def get_entity_id(metadata, entity_type, fqn):
   return metadata.get_by_name(entity=entity_type, fqn=fqn).id.__root__

def delete_entity(metadata, entity_type, id):
   metadata.delete(entity=entity_type, 
                          entity_id=id, 
                          recursive=True, 
                          hard_delete=True
                  )
