# File: ArangoDB Datafield based Metadata
# Author: alexsanchezvega
# Company: d20
# Version: 1.0

from pyArango.connection import *
from pyArango.collection import *
from pyArango.graph import *
from .BasicElement import BasicElement
from .GraphClassFactory import ClassFactory
import json
import os
from .Error import *

def md_dbname():
    return f'{os.environ.get("DBPREFIX", "")}metadata'

class Metadata():

    def __init__(self, conf={}):
        graphname = ''
        collections = ['DataFields', 'Parameters', 'Labels', 'Log', 'Countries', 'LocationHistoryCatalogue', 'Zipcodes']
        edgeDefinitions={}
        db_name = md_dbname()
        factory = ClassFactory(graphname, db_name, collections = collections, edgeDefinitions=edgeDefinitions, conf=conf)

        print(factory, " - OK")
        version_parameter = Metadata.Parameter()
        try:
            version_parameter.load('ORM_VERSION')
        except ObjectNotFoundException:
            dfs = Metadata.DataField()
            dfs.install()
            dfs = Metadata.Countries()
            dfs.install()
            dfs = Metadata.Parameter()
            dfs.install()


    class DataField(BasicElement):                    
        # Rethink
        @classmethod
        def get_col_dict(cls):
            if os.environ.get('COL_DICT', None) != None:
                col_dict = json.loads(os.environ.get('COL_DICT'))
            else:
                print("No configuration given, cannot start.")
                raise Exception
            return col_dict

        @classmethod
        def coll_to_class(cls, coll):
            col_dict = cls.get_col_dict()
            return col_dict.get(coll, coll)

        @classmethod
        def class_to_coll(cls, cl):
            col_dict = cls.get_col_dict()
            res = cl
            for e in col_dict.items():
                if e[1] == cl:
                    res = str(e[0])
                    break
            return res
                
        def make(self):
            self.attributes = ['_key', 'obj_type', 'active', 'deleted']
            self.active = True
            self.deleted = False


        def build(self):
            for key in self.attributes:
                setattr(self, key, None)
            if self.obj_type == None: 
                self.obj_type = self.__class__.__name__.lower()

            qf = self.build_filter_string_from_list([{'obj_type' : self.get('obj_type')}])
            
            if qf != '':
                qf = 'FILTER '+qf
            query = 'for m in '+ self.get_collection_name() + ' ' + qf + ' return '
            self.found = self.db.AQLQuery(query, rawResults=True, batchSize=1000)
            if len(self.found) <= 0:
                return
            self.attributes = [f.get('name') for f in self.found]
            self.scopes = {}
            for f in self.found:
                if not f.get('scope') in self.get('scopes'):
                    self.scopes[f.get('scope')] = []
                self.scopes[f.get('scope')].append(f.get('name'))
            for key in self.attributes:
                setattr(self, key, None)


        def install(self):
            self.wipeByFilter([{'obj_type':self.get('obj_type')}])
            from .Defaults_json import datafields
            for df in datafields:
                to_insert = {}
                to_insert['date_created']= datetime.utcnow()
                to_insert['date_updated'] = datetime.utcnow()
                to_insert['deleted'] = False
                to_insert.update(df)
                ins_obj = self.collection.createDocument(to_insert)
                ins_obj.save()
            from __version__ import version
            version_parameter = Metadata.Parameter()
            try:
                version_parameter.load('ORM_VERSION')
                version_parameter.value = version
                version_parameter.update()
            except ObjectNotFoundException:
                version_parameter.value = version
                version_parameter.create()

        def __init__(self, data=None, obj_type=None):
            self.obj_type = obj_type
            super().__init__(db_name = md_dbname(), data=data)
            self.collection = 'DataFields'
            
        @property
        def obj_type(self):
            return self._obj_type

        @obj_type.setter
        def obj_type(self, value):
            self._obj_type = value
            

    class Parameter(BasicElement):
        def make(self):
            self.attributes = ['_key', 'name', 'desc', 'code', 'value', 'created', 'updated', 'active', 'deleted']
            for key in self.attributes:
                setattr(self, key, None)


        def install(self):
            self.get_all()
            for res in self.found:
                res.wipe()
            from .Defaults_json import parameters
            for df in parameters:
                to_insert = {}
                to_insert['date_created']= datetime.utcnow()
                to_insert['date_updated'] = datetime.utcnow()
                to_insert['deleted'] = False
                to_insert.update(df)
                ins_obj = self.collection.createDocument(to_insert)
                ins_obj.save()

        def __init__(self, data=None):
            super().__init__(db_name = md_dbname(), data=data)
            self.collection = 'Parameters'

    class Label(BasicElement):
        def make(self):
            self.attributes = ['_key', 'name', 'lang', 'code', 'value', 'created', 'updated', 'active', 'deleted']
            for key in self.attributes:
                setattr(self, key, None)

        def __init__(self, data=None):
            super().__init__(db_name = md_dbname(), data=data)
            self.collection = 'Labels'


    class LogEntry(BasicElement):

        def make(self):
            self.attributes = ['_key', 'action', 'user', 'api_user', 'datetime', 'token', 'api_token', 'source', 'user_agent', 'user_location', 'user_ip', 'host_ip']
            for key in self.attributes:
                setattr(self, key, None)

        def __init__(self, data=None):
            super().__init__(db_name = md_dbname(), data=data)
            self.collection = 'Log'


    class LocationLog(BasicElement):

        def make(self):
            self.attributes = ['_key', 'type', 'location', 'date']
            for key in self.attributes:
                setattr(self, key, None)

        def __init__(self, data=None):
            super().__init__(db_name = md_dbname(), data=data)
            self.collection = 'LocationHistoryCatalogue'


    class Countries(BasicElement):
        def make(self):
            self.attributes = ['_key', 'name', 'translations', 'alpha3Code']
            for key in self.attributes:
                setattr(self, key, None)


        def install(self):
            self.get_all()
            for res in self.found:
                res.wipe()
            from .Defaults_json import countries
            for df in countries:
                to_insert = {}
                to_insert['date_created']= datetime.utcnow()
                to_insert['date_updated'] = datetime.utcnow()
                to_insert['deleted'] = False
                to_insert.update(df)
                ins_obj = self.collection.createDocument(to_insert)
                ins_obj.save()

        def __init__(self, data=None):
            self.collection = 'Countries'
            super().__init__(db_name = md_dbname(), data=data)


    class cp_col(BasicElement):

        def make(self):
            self.attributes = ['_key', 'IdEnt', 'Entidad', 'Ciudad', 'Municipio', 'Colonia', 'CP']
            for key in self.attributes:
                setattr(self, key, None)

        def get_by_cp(self, cp):
            self.CP = cp
            self.get_all()

        def __init__(self, data=None):
            super().__init__(db_name = md_dbname(), data=data)
            self.collection = 'Zipcodes'
