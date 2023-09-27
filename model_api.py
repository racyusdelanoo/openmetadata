# -*- coding: utf-8 -*-}
import math
import logging

from flask import request, current_app, g as flask_globals
from flask_restful import Resource

from http import HTTPStatus
from marshmallow.exceptions import ValidationError

from openmetadata.openmetadata import serialize_json 
from openmetadata.openmetadata import connection
from openmetadata.openmetadata import create_model
from openmetadata.openmetadata import list_entities
from openmetadata.openmetadata import get_entity_by_name
from openmetadata.openmetadata import get_entity_id
from openmetadata.openmetadata import delete_entity
from openmetadata.openmetadata import entity_type
from flask_babel import gettext

log = logging.getLogger(__name__)

class ModelListApi(Resource): 
    """ REST API for listing class Model"""

    def __init__(self):
        self.human_name = gettext('Model')

    def get(self):
        metadata = connection()
        data = list_entities(metadata, entity_type["MlModel"])
        
        if log.isEnabledFor(logging.DEBUG):
           log.debug(gettext('Listing %(name)s', name=self.human_name))

        return serialize_json(data) 

    def post(self):
        result = {'status': 'ERROR',
                  'message': gettext("Missing json in the request body")}
        return_code = HTTPStatus.BAD_REQUEST

        if request.json is not None:
          ml_service_name = request.json['ml_service_name']  
          ml_name = request.json['ml_name']
          ml_description = request.json['ml_description']
          ml_algorithm = request.json['ml_algorithm']
          ml_target = request.json['ml_target']
          ml_feature_name = request.json['ml_feature_name']
          ml_feature_datatype = request.json['ml_feature_datatype']
          ml_feature_algorithm = request.json['ml_feature_algorithm']
          ml_feature_source_name = request.json['ml_feature_source_name']
          ml_feature_source_datatype = request.json['ml_feature_source_datatype']
          ml_feature_data_source_fqn = request.json['ml_feature_data_source_fqn']
          ml_parameter_name = request.json['ml_parameter_name']
          ml_parameter_value = request.json['ml_parameter_value']
          ml_parameter_description = request.json['ml_parameter_description']
          ml_storage = request.json['ml_storage']
          ml_imagerepository = request.json['ml_imagerepository']
          
          model = {'name': ml_name,
                   'description': ml_description,
                   'algorithm': ml_algorithm,          
                   'target': ml_target,
                   'feature_name' : ml_feature_name, 
                   'feature_datatype':  ml_feature_datatype,
                   'feature_algorithm': ml_feature_algorithm,
                   'feature_source_name': ml_feature_source_name,
                   'feature_source_datatype': ml_feature_source_datatype,
                   'feature_data_source_fqn': ml_feature_data_source_fqn,
                   'parameter_name': ml_parameter_name,
                   'parameter_value': ml_parameter_value,
                   'parameter_description': ml_parameter_description,
                   'storage': ml_storage, 
                   'image_repository': ml_imagerepository
                  }

          metadata = connection()
          data = get_entity_by_name(metadata, entity_type["MlModelService"], ml_service_name)
          return_code = HTTPStatus.OK
          if data[0] is not None: 
            create_model(metadata, model, ml_service_name) 
            result = {'status': 'SUCESS',
                      'message': gettext("Json received with sucess")}
            return_code = HTTPStatus.CREATED
          else: 
            return_code = HTTPStatus.NOT_FOUND
            result = {
                       'status': 'ERROR',
                       'message': gettext(
                       'Model Service not found (fqn=%(fqn)s)',
                        fqn=ml_service_name) 
                     }

        return result, return_code

class ModelDetailApi(Resource): 
    """ REST API for a single instance of class Model"""

    def __init__(self):
        self.human_name = gettext('Model')

    def get(self, fqn):
        if log.isEnabledFor(logging.DEBUG):
           log.debug(gettext('Retrieving %s (fqn=%s)', self.human_name, fqn))

        metadata = connection()
        data = get_entity_by_name(metadata, entity_type["MlModel"], fqn)
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
        model = get_entity_by_name(metadata, entity_type["MlModel"], fqn) 
        return_code = HTTPStatus.OK
        if model[0] is not None: 
          delete_entity(metadata, entity_type["MlModel"], model[0].id)
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
