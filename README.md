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
curl http://localhost:5000/table -H 'content-type: application/json' -X POST -d '{"db_service_name":"database-service", "db_name":"database", "schema_name": "schema",  "table_name":"tableA", "table_columns":["id"], "table_datatypes":["BIGINT"], "table_constraints":["PRIMARY_KEY"] }' \
curl http://localhost:5000/table/"database-service.database.schema.tableA" -H 'content-type: application/json' \
curl http://localhost:5000/table/"database-service.database.schema.tableA" -H 'content-type: application/json' -X DELETE

* Model service \
curl http://localhost:5000/model_service -H 'content-type: application/json' \
curl http://localhost:5000/model_service -H 'content-type: application/json' -X POST -d '{"ml_service_name":"CustomMLService"}' \
curl http://localhost:5000/model_service/"CustomMLService" -H 'content-type: application/json' \
curl http://localhost:5000/model_service/"CustomMLService" -H 'content-type: application/json' -X DELETE

* Model \
curl http://localhost:5000/model -H 'content-type: application/json' \
curl http://localhost:5000/model -H 'content-type: application/json' -X POST -d '{"ml_service_name":"CustomMLService", "ml_name":"RevenuePredictions",
"ml_description":"This model computes how long it will take for an order to be picked up", "ml_algorithm":"XGBoost", "ml_target": "expected_time", 
"ml_feature_name": ["last_update_bucket"], "ml_feature_datatype": ["categorical"], "ml_feature_algorithm": ["Bucketing"], 
"ml_feature_source_name": ["tableA"], "ml_feature_source_datatype": ["timestamp"], "ml_feature_data_source_fqn": ["database-service.database.schema.tableA"], "ml_parameter_name": ["regularisation"], "ml_parameter_value": [0.5], "ml_parameter_description": ["Adding some room for error"], "ml_storage": "s3://path-to-pickle", "ml_imagerepository": "https://docker.hub.com/image"}' \   
curl http://localhost:5000/model/"CustomMLService.RevenuePredictions" -H 'content-type: application/json' \
curl http://localhost:5000/model/"CustomMLService.RevenuePredictions" -H 'content-type: application/json' -X DELETE


