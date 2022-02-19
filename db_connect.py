import logging

from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import generate_relationship
from sqlalchemy.orm import interfaces
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

class DBConnect:
    
    def __init__(self, username: str, password: str, host_url: str, port: str, service_name: str):
        """
        :param username: db user id
        :param password: db password
        :param host_url: db connection host URL
        :param port: database host connection port
        :param service_name: service name
        """
        
        self.base = automap_base()
        conn_str = f'oracle+cx_oracle://{username}:{password}@{host_url}:{port}/?service_name={service_name}'
        self.engine = create_engine(conn_str, max_identifier_length=128)
        # reflect the tables
        self.base.prepare(self.engine, reflect=True, generate_relationship=self.__gen_relationship)
        self.session_maker = sessionmaker(bind=self.engine)
    
    def get_session(self):
        """
        Returns a session from the sessionmaker factory
        :return:  sqlalchemy.orm.sessionmaker
        """
        return self.session_maker()
    
    def get_table_object(self, table: str):
        """
        Provided a table name in db, return the sql alchemy class instance corresponding to it
        :param table: str
        :return: sqlalchemy.ext.declarative.api.DeclarativeMeta
        """
        return self.base.classes[table]

    @staticmethod
    def __gen_relationship(base, direction, return_fn, attrname, local_cls, referred_cls, **kwargs):

        if direction is interfaces.ONETOMANY:
            kwargs['cascade'] = 'all, delete-orphan'
            kwargs['passive_deletes'] = True
        return generate_relationship(base, direction, return_fn, attrname,
                                     local_cls, referred_cls, **kwargs)
