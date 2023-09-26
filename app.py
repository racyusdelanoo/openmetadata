#!/usr/bin/env python
# -*- coding: utf-8 -*-

import eventlet.wsgi

from flask import Flask
from flask import request
from flask_babel import get_locale, Babel
from flask_cors import CORS
from flask_restful import Api

from openmetadata.database_service_api import DatabaseServiceListApi
from openmetadata.database_service_api import DatabaseServiceDetailApi
from openmetadata.database_api import DatabaseListApi
from openmetadata.database_api import DatabaseDetailApi
from openmetadata.schema_api import SchemaListApi
from openmetadata.schema_api import SchemaDetailApi
from openmetadata.table_api import TableListApi
from openmetadata.table_api import TableDetailApi

app = Flask(__name__)

babel = Babel(app)

CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)

mappings = {
    '/database_service': DatabaseServiceListApi, 
    '/database_service/<string:fqn>': DatabaseServiceDetailApi, 
    '/database': DatabaseListApi, 
    '/database/<string:fqn>': DatabaseDetailApi, 
    '/schema': SchemaListApi, 
    '/schema/<string:fqn>': SchemaDetailApi, 
    '/table': TableListApi, 
    '/table/<string:fqn>': TableDetailApi #, 
    #'/model_service': ModelServiceListApi, 
    #'/model': ModelListApi, 
    #'/pipeline_service': PipelineServiceListApi, 
    #'/pipeline': PipelineListApi, 
    #'/classification': ClassificationListApi, 
    #'/tag': TagListApi, 
    #'/lineage': LineageListApi, 
    #'/data_quality': DataQualityListApi, 
}

for path, view in list(mappings.items()):
   api.add_resource(view, path)

@babel.localeselector
def get_locale():
    return request.args.get('lang') or \
    request.accept_languages.best_match(['pt', 'en']) or 'pt'

if __name__ == '__main__':
   app.run(debug=True, port=5000)

