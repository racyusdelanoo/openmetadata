# -*- coding: utf-8 -*-}
import math
import logging

from flask import request, current_app, g as flask_globals
from flask_restful import Resource

from http import HTTPStatus
from marshmallow.exceptions import ValidationError

from openmetadata.openmetadata import serialize_json 
from openmetadata.openmetadata import connection
from openmetadata.openmetadata import create_lineage
from openmetadata.openmetadata import list_entities
from openmetadata.openmetadata import get_entity_by_name
from openmetadata.openmetadata import get_entity_id
from openmetadata.openmetadata import get_lineage_by_name 
from openmetadata.openmetadata import entity_type
from openmetadata.openmetadata import delete_lineage_edge
from flask_babel import gettext

log = logging.getLogger(__name__)

class LineageListApi(Resource): 
    """ REST API for listing class Lineage """

    def __init__(self):
        self.human_name = gettext('Lineage')
    
    def post(self):
        result = {'status': 'ERROR',
                  'message': gettext("Missing json in the request body")}
        return_code = HTTPStatus.BAD_REQUEST

        if request.json is not None:
          from_entity      = request.json['fromEntity'] 
          from_entity_type = request.json['fromEntityType'] 
          to_entity        = request.json['toEntity'] 
          to_entity_type   = request.json['toEntityType'] 
          description = request.json['description'] 
          
          metadata = connection()

          from_entity_data = get_entity_by_name(metadata, entity_type[from_entity_type], from_entity)   
          to_entity_data   = get_entity_by_name(metadata, entity_type[to_entity_type], to_entity)   

          if (from_entity_data[0] is not None) and (to_entity_data[0] is not None): 
            create_lineage(metadata, from_entity_data[0], to_entity_data[0], from_entity_type, to_entity_type, description) 
            result = {'status': 'SUCESS',
                      'message': gettext("Json received with sucess")}
            return_code = HTTPStatus.CREATED
          else: 
            return_code = HTTPStatus.NOT_FOUND
            result = {
                       'status': 'ERROR',
                       'message': gettext(
                       'Entities not found (fqn=%(fqn)s)',
                        fqn=entity_name) 
                     }

        return result, return_code

class LineageDetailApi(Resource): 
    """ REST API for a single instance of class Lineage"""

    def __init__(self):
        self.human_name = gettext('Lineage')

    def get(self, fqn):
        if log.isEnabledFor(logging.DEBUG):
           log.debug(gettext('Retrieving %s (fqn=%s)', self.human_name, fqn))
        
        metadata = connection()
        fqn = fqn.split('|') 
        etype  = fqn[0] 
        entity = fqn[1] 
        data = get_lineage_by_name(metadata, entity_type[etype], entity) 

        return_code = HTTPStatus.OK
        
        if data is not None: 
          result={
                  'status': 'OK',
                  'data': data 
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
        fqn = fqn.split('|') 
        from_entity_type = fqn[0] 
        from_entity      = fqn[1] 
        to_entity_type   = fqn[2] 
        to_entity        = fqn[3]  
        lineage = get_lineage_by_name(metadata, entity_type[from_entity_type], from_entity) 
        from_entity_data = get_entity_by_name(metadata, entity_type[from_entity_type], from_entity)
        to_entity_data = get_entity_by_name(metadata, entity_type[to_entity_type], to_entity)
        return_code = HTTPStatus.OK
        if lineage is not None: 
          lineage_edge = {"from_entity_id": from_entity_data[0].id, 
                          "from_entity_type": from_entity_type, 
                          "to_entity_id": to_entity_data[0].id,
                          "to_entity_type": to_entity_type
                         }
          delete_lineage_edge(metadata, lineage_edge)
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
