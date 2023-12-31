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
from openmetadata.model_service_api import ModelServiceListApi
from openmetadata.model_service_api import ModelServiceDetailApi
from openmetadata.model_api import ModelListApi
from openmetadata.model_api import ModelDetailApi
from openmetadata.pipeline_service_api import PipelineServiceListApi
from openmetadata.pipeline_service_api import PipelineServiceDetailApi
from openmetadata.pipeline_api import PipelineListApi
from openmetadata.pipeline_api import PipelineDetailApi
from openmetadata.tags_group_api import TagsGroupListApi
from openmetadata.tags_group_api import TagsGroupDetailApi
from openmetadata.tag_api import TagListApi
from openmetadata.tag_api import TagDetailApi
from openmetadata.patch_tag_api import PatchTagListApi
from openmetadata.patch_tag_api import PatchTagDetailApi
from openmetadata.patch_column_tag_api import PatchColumnTagListApi
from openmetadata.patch_column_tag_api import PatchColumnTagDetailApi
from openmetadata.lineage_api import LineageListApi
from openmetadata.lineage_api import LineageDetailApi
from openmetadata.data_quality_api import DataQualityListApi
from openmetadata.data_quality_api import DataQualityDetailApi

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
    '/table/<string:fqn>': TableDetailApi, 
    '/model_service': ModelServiceListApi, 
    '/model_service/<string:fqn>': ModelServiceDetailApi, 
    '/model': ModelListApi,  
    '/model/<string:fqn>': ModelDetailApi, 
    '/pipeline_service': PipelineServiceListApi, 
    '/pipeline_service/<string:fqn>': PipelineServiceDetailApi, 
    '/pipeline': PipelineListApi, 
    '/pipeline/<string:fqn>': PipelineDetailApi, 
    '/tags_group': TagsGroupListApi, 
    '/tags_group/<string:fqn>': TagsGroupDetailApi, 
    '/tag': TagListApi, 
    '/tag/<string:fqn>': TagDetailApi, 
    '/patch_tag': PatchTagListApi, 
    '/patch_tag/<string:fqn>': PatchTagDetailApi, 
    '/patch_column_tag': PatchColumnTagListApi, 
    '/patch_column_tag/<string:fqn>': PatchColumnTagDetailApi, 
    '/lineage': LineageListApi, 
    '/lineage/<string:fqn>': LineageDetailApi, 
    '/data_quality': DataQualityListApi, 
    '/data_quality/<string:fqn>': DataQualityDetailApi, 
}

for path, view in list(mappings.items()):
   api.add_resource(view, path)

@babel.localeselector
def get_locale():
    return request.args.get('lang') or \
    request.accept_languages.best_match(['pt', 'en']) or 'pt'

if __name__ == '__main__':
   app.run(debug=True, port=5000)

