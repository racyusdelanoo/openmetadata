# Openmetadata
API Openmetadata 

# Virtual environment 
python3 -m venv env \
source env/bin/activate \
desactive 

# Flask 
export FLASK_APP=app.py\
export FLASK_ENV=development \
export FLASK_DEBUG=1 \
flask run 

# Curl commands   
* Database service \
curl http://localhost:5000/database_service -H 'content-type: application/json' \
curl http://localhost:5000/database_service -H 'content-type: application/json' -X POST -d '{"db_service_name":"database-service"}' \
curl http://localhost:5000/database_service/"database-service" -H 'content-type: application/json' \
curl http://localhost:5000/database_service/"database-service" -H 'content-type: application/json' -X DELETE 
  
* Database \
curl http://localhost:5000/database -H 'content-type: application/json' \
curl http://localhost:5000/database -H 'content-type: application/json' -X POST -d '{"db_service_name":"database-service", "db_name":"database"}' \
curl http://localhost:5000/database/"database-service.database" -H 'content-type: application/json' \
curl http://localhost:5000/database/"database-service.database" -H 'content-type: application/json' -X DELETE 

* Schema \
curl http://localhost:5000/schema -H 'content-type: application/json' <br> 
curl http://localhost:5000/schema -H 'content-type: application/json' -X POST -d '{"db_service_name":"database-service", "db_name":"database", "schema_name": "schema"}' \
curl http://localhost:5000/schema/"database-service.database.schema" -H 'content-type: application/json' \
curl http://localhost:5000/schema/"database-service.database.schema" -H 'content-type: application/json' -X DELETE 

* Table \
curl http://localhost:5000/table -H 'content-type: application/json' \
curl http://localhost:5000/table -H 'content-type: application/json' -X POST -d '{"db_service_name":"database-service", "db_name":"database", "schema_name": "schema", "table_name": "tableA", "table_columns": [{"name": "id", "type": "BIGINT", "constraints": "PRIMARY_KEY"}]}' \
curl http://localhost:5000/table/"database-service.database.schema.tableA" -H 'content-type: application/json' \
curl http://localhost:5000/table/"database-service.database.schema.tableA" -H 'content-type: application/json' -X DELETE

* Model service \
curl http://localhost:5000/model_service -H 'content-type: application/json' \
curl http://localhost:5000/model_service -H 'content-type: application/json' -X POST -d '{"ml_service_name":"CustomMLService"}' \
curl http://localhost:5000/model_service/"CustomMLService" -H 'content-type: application/json' \
curl http://localhost:5000/model_service/"CustomMLService" -H 'content-type: application/json' -X DELETE

* Model \
curl http://localhost:5000/model -H 'content-type: application/json' \
curl http://localhost:5000/model -H 'content-type: application/json' -X POST -d '{"ml_model": {"service_name": "CustomMLService", "name": "RevenuePredictions", "description": "This model computes how long it will take for an order to be picked up", "algorithm": "XGBoost", "target": "expected_time"}, "ml_feature": [{"name": "last_update_bucket", "type": "categorical", "algorithm": "Bucketing"}], "ml_feature_source": [{"name": "tableA", "type": "timestamp", "data_source_fqn": "database-service.database.schema.tableA"}], "ml_parameter": [{"name": "regularisation", "value": "0.5", "description": "Adding some room for error"}], "ml_store": {"storage": "s3://path-to-pickle", "image_repository": "https://docker.hub.com/image"}}' \
curl http://localhost:5000/model/"CustomMLService.RevenuePredictions" -H 'content-type: application/json' \
curl http://localhost:5000/model/"CustomMLService.RevenuePredictions" -H 'content-type: application/json' -X DELETE

* Pipeline service <br> 
curl http://localhost:5000/pipeline_service -H 'content-type: application/json' \
curl http://localhost:5000/pipeline_service -H 'content-type: application/json' -X POST -d '{"pipeline_service": {"name": "pipeline-service", "description": "Description of pipeline service"}}' \
curl http://localhost:5000/pipeline_service/"pipeline-service" -H 'content-type: application/json' \
curl http://localhost:5000/pipeline_service/"pipeline-service" -H 'content-type: application/json' -X DELETE 

* Pipeline <br>
curl http://localhost:5000/pipeline -H 'content-type: application/json' \
curl http://localhost:5000/pipeline -H 'content-type: application/json' -X POST -d '{"pipeline": {"service_name": "pipeline-service",  "name": "pipeline1", "description": "Description of the pipeline instance."}}' \
curl http://localhost:5000/pipeline/"pipeline-service.pipeline1" -H 'content-type: application/json' \
curl http://localhost:5000/pipeline/"pipeline-service.pipeline1" -H 'content-type: application/json' -X DELETE

* Tags group <br>
curl http://localhost:5000/tags_group -H 'content-type: application/json' \
curl http://localhost:5000/tags_group -H 'content-type: application/json' -X POST -d '{"tags_group": {"name": "Lemonade",  "description": "Tags of the Lemonade."}}' \
curl http://localhost:5000/tags_group/"Lemonade" -H 'content-type: application/json' \
curl http://localhost:5000/tags_group/"Lemonade" -H 'content-type: application/json' -X DELETE

