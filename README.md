# Openmetadata
API Openmetadata 

# Virtual environment 
python3 -m venv env \
source env/bin/activate \
desactive 

# Flask 
export FLASK_APP=app.py \ 
export FLASK_ENV=development \
export FLASK_DEBUG=1 \
flask run 

# Curl commands   
-> Database service \
curl http://localhost:5000/database_service -H 'content-type: application/json' \
curl http://localhost:5000/database_service -H 'content-type: application/json' -X POST -d '{"db_service_name":"database-service"}' \
curl http://localhost:5000/database_service/"database-service" -H 'content-type: application/json' \
curl http://localhost:5000/database_service/"database-service" -H 'content-type: application/json' -X DELETE 
  
-> Database \
curl http://localhost:5000/database -H 'content-type: application/json' \
curl http://localhost:5000/database -H 'content-type: application/json' -X POST -d '{"db_service_name":"database-service", "db_name":"database"}' \
curl http://localhost:5000/database/"database-service.database" -H 'content-type: application/json' \
curl http://localhost:5000/database/"database-service.database" -H 'content-type: application/json' -X DELETE 

-> Schema \
curl http://localhost:5000/schema -H 'content-type: application/json' \ 
curl http://localhost:5000/schema -H 'content-type: application/json' -X POST -d '{"db_service_name":"database-service", "db_name":"database", "schema_name": "schema"}' \
curl http://localhost:5000/schema/"database-service.database.schema" -H 'content-type: application/json' \
curl http://localhost:5000/schema/"database-service.database.schema" -H 'content-type: application/json' -X DELETE 

