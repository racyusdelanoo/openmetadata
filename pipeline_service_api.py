# -*- coding: utf-8 -*-}
import math
import logging

from flask import request, current_app, g as flask_globals
from flask_restful import Resource

from http import HTTPStatus
from marshmallow.exceptions import ValidationError

from openmetadata.openmetadata import serialize_json 
from openmetadata.openmetadata import connection
from openmetadata.openmetadata import create_pipeline_service
from openmetadata.openmetadata import list_entities
from openmetadata.openmetadata import get_entity_by_name
from openmetadata.openmetadata import get_entity_id
from openmetadata.openmetadata import delete_entity
from openmetadata.openmetadata import entity_type
from flask_babel import gettext

log = logging.getLogger(__name__)

class PipelineServiceListApi(Resource): 
    """ REST API for listing class Pipeline Service """

    def __init__(self):
        self.human_name = gettext('Pipeline Service')

    def get(self):
        metadata = connection()
        data = list_entities(metadata, entity_type["PipelineService"])
        if log.isEnabledFor(logging.DEBUG):
           log.debug(gettext('Listing %(name)s', name=self.human_name))

        return serialize_json(data) 

    def post(self):
        result = {'status': 'ERROR',
                   'message': gettext("Missing json in the request body")}
        return_code = HTTPStatus.BAD_REQUEST

        if request.json is not None:
          pipeline_service = request.json['pipeline_service']  
          metadata = connection()
          create_pipeline_service(metadata, pipeline_service) 
          
          result = {'status': 'SUCESS',
                    'message': gettext("Json received with sucess")}
          return_code = HTTPStatus.CREATED

        return result, return_code

class PipelineServiceDetailApi(Resource): 
    """ REST API for a single instance of class Pipeline Service """

    def __init__(self):
        self.human_name = gettext('Pipeline Service')

    def get(self, fqn):
        if log.isEnabledFor(logging.DEBUG):
           log.debug(gettext('Retrieving %s (fqn=%s)', self.human_name, fqn))

        metadata = connection()
        data = get_entity_by_name(metadata, entity_type["PipelineService"], fqn)
        return_code = HTTPStatus.OK
        if data[0] is not None: 
          result={
                  'status': 'OK',
                  'data': serialize_json(data) 
                 }
        else: 
            return_code = HTTPStatus.NOT_FOUND
            result = {
                       'status': 'ERROR',
                       'message': gettext(
                       '%(name)s not found (fqn=%(fqn)s)',
                       name=self.human_name, fqn=fqn) 
                     }
        return result, return_code 

    def delete(self, fqn):
        if log.isEnabledFor(logging.DEBUG):
           log.debug(gettext('Deleting %s (fqn=%s)', self.human_name, fqn))

        metadata = connection()
        pipeline_service = get_entity_by_name(metadata, entity_type["PipelineService"], fqn) 
        return_code = HTTPStatus.OK
        if pipeline_service[0] is not None: 
          delete_entity(metadata, entity_type["PipelineService"], pipeline_service[0].id)
          result={
                  'status': 'OK',
                  'message': gettext(
                  '%(name)s deleted with sucess!',
                  name=self.human_name) 
                 }
        else: 
            return_code = HTTPStatus.NOT_FOUND
            result = {
                       'status': 'ERROR',
                       'message': gettext(
                       '%(name)s not found (fqn=%(fqn)s)',
                       name=self.human_name, fqn=fqn) 
                     }
        return result, return_code 
