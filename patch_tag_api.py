# -*- coding: utf-8 -*-}
import math
import logging

from flask import request, current_app, g as flask_globals
from flask_restful import Resource

from http import HTTPStatus
from marshmallow.exceptions import ValidationError

from openmetadata.openmetadata import serialize_json 
from openmetadata.openmetadata import connection
from openmetadata.openmetadata import create_patch_tag
from openmetadata.openmetadata import dump_tag
from openmetadata.openmetadata import list_entities
from openmetadata.openmetadata import get_entity_by_name
from openmetadata.openmetadata import get_entity_id
from openmetadata.openmetadata import delete_entity
from openmetadata.openmetadata import entity_type
from flask_babel import gettext

log = logging.getLogger(__name__)

class PatchTagListApi(Resource): 
    """ REST API for listing class Patch Tag"""

    def __init__(self):
        self.human_name = gettext('Patch Tag')
    
    def post(self):
        result = {'status': 'ERROR',
                  'message': gettext("Missing json in the request body")}
        return_code = HTTPStatus.BAD_REQUEST

        if request.json is not None:
          tags  = request.json['tags']
          ename = request.json['entity_name'] 
          etype = request.json['entity_type']  
          
          metadata = connection()
          data = get_entity_by_name(metadata, entity_type[etype], ename)
          
          if data[0] is not None: 
            for tag in tags: 
               create_patch_tag(metadata, tag['name'], etype, data[0]) 

            result = {'status': 'SUCESS',
                      'message': gettext("Json received with sucess")}
            return_code = HTTPStatus.CREATED
          else: 
            return_code = HTTPStatus.NOT_FOUND
            result = {
                       'status': 'ERROR',
                       'message': gettext(
                       'Entity not found (fqn=%(fqn)s)',
                        fqn=entity_name) 
                     }

        return result, return_code

class PatchTagDetailApi(Resource): 
    """ REST API for a single instance of class Patch Tag"""

    def __init__(self):
        self.human_name = gettext('Tag')

    def get(self, fqn):
        if log.isEnabledFor(logging.DEBUG):
           log.debug(gettext('Retrieving %s (fqn=%s)', self.human_name, fqn))
        
        metadata = connection()
        fqn = fqn.split('|') 
        etype  = fqn[0] 
        entity = fqn[1] 
        data = get_entity_by_name(metadata, entity_type[etype], entity) 
        return_code = HTTPStatus.OK
        if data[0] is not None: 
          result={
                  'status': 'OK',
                  'data': dump_tag(data) 
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

    #def delete(self, fqn):
    #    if log.isEnabledFor(logging.DEBUG):
    #       log.debug(gettext('Deleting %s (fqn=%s)', self.human_name, fqn))
    #    metadata = connection()
    #    fqn = fqn.split('|') 
    #    etype  = fqn[0] 
    #    entity = fqn[1] 
    #    data = get_entity_by_name(metadata, entity_type[etype], entity) 
    #    return_code = HTTPStatus.OK
    #    if data[0] is not None: 
    #      tag = ""
    #      #data[0].changeDescription.fieldsAdded[0].newValue = None
    #      #metadata.create_or_update(data=data)
    #      #import pdb; pdb.set_trace();
    #      create_patch_tag(metadata, tag, etype, data[0])
    #      result={
    #              'status': 'OK',
    #              'message': gettext(
    #              '%(name)s deleted with sucess!',
    #              name=self.human_name) 
    #             }
    #    else: 
    #        return_code = HTTPStatus.NOT_FOUND
    #        result = {
    #                   'status': 'ERROR',
    #                   'message': gettext(
    #                   '%(name)s not found (fqn=%(fqn)s)',
    #                   name=self.human_name, fqn=fqn) 
    #                 }
    #    return result, return_code 
