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
from metadata.generated.schema.type.entityReference import EntityReference

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

#Model Service 
from metadata.generated.schema.entity.services.mlmodelService import (
    MlModelService,
    MlModelConnection,
    MlModelServiceType
)
from metadata.generated.schema.api.services.createMlModelService import CreateMlModelServiceRequest
from metadata.generated.schema.entity.services.connections.mlmodel.customMlModelConnection import (
    CustomMlModelConnection, CustomMlModelType
)

#Model
from metadata.generated.schema.api.data.createMlModel import CreateMlModelRequest
from metadata.generated.schema.entity.data.mlmodel import (
    MlFeature, 
    MlHyperParameter, 
    FeatureSource, 
    MlStore, 
    MlModel
)

#Pipeline Service
from metadata.generated.schema.api.services.createPipelineService import (
    CreatePipelineServiceRequest,
)
from metadata.generated.schema.entity.services.connections.pipeline.customPipelineConnection import (
    CustomPipelineConnection, CustomPipelineType
)
from metadata.generated.schema.entity.services.pipelineService import (
    PipelineConnection,
    PipelineService,
    PipelineServiceType,
)

#Pipeline 
from metadata.generated.schema.api.data.createPipeline import CreatePipelineRequest
from metadata.generated.schema.entity.data.pipeline import (
    Pipeline,
    PipelineStatus,
    StatusType,
    Task,
    TaskStatus,
)

#Classification - Tags group
from metadata.generated.schema.entity.classification.classification import (
    Classification,
)
from metadata.generated.schema.api.classification.createClassification import (
    CreateClassificationRequest,
)

#Tag 
from metadata.generated.schema.entity.classification.tag import Tag
from metadata.generated.schema.api.classification.createTag import CreateTagRequest

#Tag Label 
from metadata.generated.schema.type.tagLabel import (
     LabelType, 
     State,
     TagLabel,
     TagSource,
)

#Lineage 
from metadata.generated.schema.api.lineage.addLineage import AddLineageRequest
from metadata.generated.schema.type.entityLineage import (
    EntitiesEdge,
    LineageDetails,
)

#Data Quality 
from metadata.generated.schema.api.tests.createTestCase import CreateTestCaseRequest
from metadata.generated.schema.api.tests.createTestDefinition import CreateTestDefinitionRequest
from metadata.generated.schema.api.tests.createTestSuite import CreateTestSuiteRequest
from metadata.generated.schema.tests.testCase  import TestCase
from metadata.generated.schema.tests.testCase  import TestCaseParameterValue
from metadata.generated.schema.tests.testSuite import TestSuite
from metadata.generated.schema.tests.testDefinition import (
    EntityType,
    TestCaseParameterDefinition,
    TestDefinition,
    TestPlatform,
)
from metadata.generated.schema.tests.basic import (
    TestCaseResult,
    TestCaseStatus,
    TestResultValue,
)

from datetime import datetime

jwt_token='eyJraWQiOiJHYjM4OWEtOWY3Ni1nZGpzLWE5MmotMDI0MmJrOTQzNTYiLCJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJvcGVuLW1ldGFkYXRhLm9yZyIsInN1YiI6ImluZ2VzdGlvbi1ib3QiLCJlbWFpbCI6ImluZ2VzdGlvbi1ib3RAb3Blbm1ldGFkYXRhLm9yZyIsImlzQm90Ijp0cnVlLCJ0b2tlblR5cGUiOiJCT1QiLCJpYXQiOjE2OTUyMDk2MjYsImV4cCI6bnVsbH0.RVJ6_EWarVhygSILmoGzk7rQ01uqBDOhTNJzAEGUqtyiB_VWJj7beIHI-SgBEQUj1RxSUcFOX2M-DszgHj2eX8a5ezgiT4yij6JVyU07QkCIAgQ5Q-S7tzvkt7GJIBNPXQJjpR9tkmCgFz4hpyanz2I723ZllmZxSrwwRabNUvHT6sLjLzwQillaJw0247iYIvwekmj3nzSL_p1L0mi4RvJkYXSIW_IjDYtCoc6zF5JxOVp9dNCSPYzQeViX6bSdHN3JgYFUQXEOvHSXi3NFl9_Iqyt9D9cAOzGIyqAkQD_7EaGH2TrOADH6Uiuoty8Lwi-GdeBPZnwdx0RcOXQbNQ'

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
                "MlModelService": MlModelService,  
                "MlModel": MlModel,
                "PipelineService": PipelineService,
                "Pipeline": Pipeline,
                "Classification": Classification,
                "Tag": Tag,
                "TagLabel": TagLabel,
                "TestCase": TestCase,
              }

test_entity_type = {
                     "Table": EntityType.TABLE, 
                     "Column": EntityType.COLUMN 
	           }

def serialize_json(data, mode=None): 
   """
   0 - Standard entities 
   1 - Tags group
   2 - Tags  
   """
   fields = [] 
   serviceType = None
   for index in range(len(data)):
      id          = str(data[index].id.__root__)
      name        = data[index].name.__root__
      if (mode == 2): 
        fqn = data[index].fullyQualifiedName
      else: 
        fqn = data[index].fullyQualifiedName.__root__
      description = str(data[index].description)
      if (mode == 0):
        serviceType = str(data[index].serviceType)   
      fields.append([id, name, fqn, serviceType, description])   
   
   result = [{'id': i, 'name': n, 'fullyQualifiedName': fqn, 'serviceType': st, 
                'description': d} 
                for i, n, fqn, st, d in fields]   

   return result

def dump_tag(data): 
   tags = data[0].changeDescription.fieldsAdded[0].newValue
   return json.loads(tags) 

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
               service=db_service
   )
   return metadata.create_or_update(data=database)

def create_schema(metadata, database, schema_name):
   schema = CreateDatabaseSchemaRequest(
             name=schema_name,
             database=database, 
   )
   return metadata.create_or_update(schema)

def create_table(metadata, table_name, table_columns, schema_name):
    mtable = CreateTableRequest(
              name=table_name, 
              databaseSchema=schema_name,  
              columns=[Column(name=column['name'], 
                              dataType=DataType(column['type']), 
                              constraint=column['constraints'] 
                             )
                             for column in table_columns
                      ], 
              )
    return metadata.create_or_update(data=mtable)

def create_model_service(metadata, ml_service_name): 
    ml_service = CreateMlModelServiceRequest(
	          name=ml_service_name,
                  serviceType=MlModelServiceType.CustomMlModel,
                  connection=MlModelConnection(
                      config=CustomMlModelConnection(
                          type=CustomMlModelType.CustomMlModel,
                          sourcePythonClass="my.class",
                      )
                   )
                )
    return metadata.create_or_update(data=ml_service)

def create_model(metadata, ml_model, ml_feature, ml_feature_source, ml_parameter, ml_store): 
   model = CreateMlModelRequest(
              name=ml_model["name"],
              description=ml_model["description"],
              algorithm=ml_model["algorithm"],
              target=ml_model["target"],
	      mlFeatures=[
	          MlFeature( 
	              name=feature['name'],
	              dataType=feature['type'],
	              featureAlgorithm=feature['algorithm'],
	              featureSources=[
	                FeatureSource(  
	                  name=feature_source['name'],
	                  dataType=feature_source['type'],
	                  dataSource=get_data_source_from_fqn(metadata, feature_source['data_source_fqn'])  
	                )
                        for feature_source in ml_feature_source 
	              ] 
	          )
                  for feature in ml_feature 
	      ],
	      mlHyperParameters=[
	          MlHyperParameter(
	              name=parameter['name'],
	              value=parameter['value'],
	              description=parameter['description'],
	          )
                  for parameter in ml_parameter 
	      ],
	      mlStore=MlStore(
	        storage=ml_store["storage"],
	        imageRepository=ml_store['image_repository']
              ), 
              service=ml_model['service_name']   
            ) 
   return metadata.create_or_update(data=model)

def create_pipeline_service(metadata, pip_service): 
   pipeline_service = CreatePipelineServiceRequest(
        name=pip_service["name"],
        description=pip_service["description"],
        serviceType=PipelineServiceType.CustomPipeline,
        connection=PipelineConnection(
            config=CustomPipelineConnection(  
                type=CustomPipelineType.CustomPipeline,  
                sourcePythonClass="", 
                connectionOptions=""  
            ),
        ),
    )

   return metadata.create_or_update(data=pipeline_service)  

def create_pipeline(metadata, pipeline): 
   mpipeline = CreatePipelineRequest(
            name=pipeline["name"],
            description=pipeline["description"], 
            service=pipeline['service_name'],
        )
   return metadata.create_or_update(data=mpipeline)

def create_tags_group(metadata, tags_group): 
   classification = CreateClassificationRequest(
                      description=tags_group["description"], name=tags_group["name"]
                    )
   return metadata.create_or_update(data=classification)

def create_tag(metadata, tag_group_name, tag_name, tag_description): 
   create_tag = CreateTagRequest(
                  name=tag_name,
                  description=tag_description,
                  classification=tag_group_name
                )
   return metadata.create_or_update(data=create_tag)

def create_patch_tag(metadata, tag, etype, entity): 
   TAG_LABEL = TagLabel(
                tagFQN=tag, 
                labelType=LabelType.Automated, 
                state=State.Suggested.value, 
                source=TagSource.Classification,
               )   
   join_entity_tag = metadata.patch_tag(
                       entity=entity_type[etype], 
                       source=entity,
                       tag_label=TAG_LABEL,
                     )
   return join_entity_tag

def create_patch_column_tag(metadata, tag, table, column): 
   TAG_LABEL = TagLabel(
                tagFQN=tag, 
                labelType=LabelType.Automated, 
                state=State.Suggested.value, 
                source=TagSource.Classification,
               )   
   join_column_tag = metadata.patch_column_tag(
                       table=table, 
                       tag_label=TAG_LABEL,
                       column_fqn=table.fullyQualifiedName.__root__ +"."+column
                     )
   return join_column_tag

def create_lineage(metadata, fromEntity, toEntity, fromEntityType, toEntityType, description):
   lineage = AddLineageRequest(
                 edge=EntitiesEdge(fromEntity=EntityReference(id=fromEntity.id, type=fromEntityType.lower()),
                 toEntity=EntityReference(id=toEntity.id, type=toEntityType.lower()),
                 lineageDetails=LineageDetails(description=description),
               ),
            ) 
   return metadata.add_lineage(data=lineage) 

def create_test(metadata, test): 
  
   test_definition = metadata.create_or_update(
        CreateTestDefinitionRequest(
     	   name=test['name'],
     	   description=test['description'],
     	   entityType=test_entity_type[test['entity_type']],
     	   testPlatforms=[TestPlatform.GreatExpectations],
     	   parameterDefinition=[
     			         TestCaseParameterDefinition(
     					                     name=parameter['name'], 
     							     value=parameter['value']
     							    ) 
     			         for parameter in test['parameters']
     			       ],
        )
   )
   
   test_suite = metadata.create_or_update_executable_test_suite(
         CreateTestSuiteRequest(
            name=test['entity_name'] + "." + test['name'],
            description=test['description'],
            executableEntityReference=test['entity_name'],
         )
   ) 

   test_case = metadata.create_or_update(
        CreateTestCaseRequest(
            name=test['name'],
            description=test['description'],
            entityLink="<#E::table::" + test['entity_name'] + ">",
            testSuite=test_suite.fullyQualifiedName,
            testDefinition=test_definition.fullyQualifiedName,
            parameterValues=[
                             TestCaseParameterValue(
                                                     name=parameter['name'], 
                                                     value=parameter['value']
                                                   )
                             for parameter in test['parameters']
                            ],
        )
   )
  
   test_case_status = TestCaseStatus.Failed
   result_description = "Test case failed!"

   if test['test_result'].upper() == 'SUCESS': 
     test_case_status = TestCaseStatus.Success
     result_description = "Test case success!"
     
   test_case_results = metadata.add_test_case_results(
      test_results=TestCaseResult(
          timestamp=int(datetime.utcnow().timestamp()),
          testCaseStatus=test_case_status,
          result=result_description,
          sampleData=None,
          testResultValue=[
                            TestResultValue(
                                             name=parameter['name'], 
                                             value=parameter['value']
                                           )
                            for parameter in test['parameters']
                          ],
      ),
      test_case_fqn=test_case.fullyQualifiedName.__root__,
   )

def list_entities(metadata, entity_type): 
   return metadata.list_entities(entity=entity_type).entities

def get_entity_by_name(metadata, entity_type, fqn, fields = None):
   return [metadata.get_by_name(entity=entity_type, fqn=fqn, fields=fields)]

def get_entity_id(metadata, entity_type, fqn):
   return metadata.get_by_name(entity=entity_type, fqn=fqn).id.__root__

def get_lineage_by_name(metadata, entity_type, fqn): 
   return metadata.get_lineage_by_name( 
		entity=entity_type,
		fqn=fqn,
		# Tune this to control how far in the lineage graph to go
		up_depth=1,
                down_depth=1
          )  

def get_data_source_from_fqn(metadata, fqn):
    if fqn:
        table: Table = metadata.get_by_name(entity=Table, fqn=fqn)
        if table:
            return EntityReference(
                id=table.id.__root__,
                type="table",
                name=table.name.__root__,
                fullyQualifiedName=table.fullyQualifiedName.__root__,
            )

    return None

def delete_entity(metadata, entity_type, id):
   metadata.delete(entity=entity_type, 
                          entity_id=id, 
                          recursive=True, 
                          hard_delete=True
                  )

def delete_lineage_edge(metadata, lineage_edge): 
    edge=EntitiesEdge(fromEntity=EntityReference(id=lineage_edge['from_entity_id'], type=lineage_edge['from_entity_type'].lower()),
    toEntity=EntityReference(id=lineage_edge['to_entity_id'], type=lineage_edge['to_entity_type'].lower()))
    metadata.delete_lineage_edge(edge)
