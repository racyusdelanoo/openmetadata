# openmetadata
API Openmetadata 

# Curl commands   
-> Database service \
curl http://localhost:5000/database\_service -H 'content-type: application/json' \
curl http://localhost:5000/database\_service -H 'content-type: application/json' -X POST -d '{"db\_service\_name":"database-service"}'\
curl http://localhost:5000/database\_service/"database-service" -H 'content-type: application/json' \
curl http://localhost:5000/database\_service/"database-service" -H 'content-type: application/json' -X DELETE \
  
-> Database 
  curl http://localhost:5000/database -H 'content-type: application/json'  
  curl http://localhost:5000/database -H 'content-type: application/json' -X POST -d '{"db_service_name":"database-service", "db_name":"database"}'
  curl http://localhost:5000/database/"database-service.database" -H 'content-type: application/json'
  curl http://localhost:5000/database/"database-service.database" -H 'content-type: application/json' -X DELETE

-> Schema 
  curl http://localhost:5000/schema -H 'content-type: application/json'  
  curl http://localhost:5000/schema -H 'content-type: application/json' -X POST -d '{"db_service_name":"database-service", "db_name":"database", "schema_name": "schema"}'
  curl http://localhost:5000/schema/"database-service.database.schema" -H 'content-type: application/json'
  curl http://localhost:5000/schema/"database-service.database.schema" -H 'content-type: application/json' -X DELETE

