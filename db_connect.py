"""
Normally sqlalchemy and alembic are used together in normal scenario, where data models are defined using sqlalchemy.
But another case is like data models are defined and migrated using some other technologies such as flywaydb. In this
context, if we wan't to reverse map databse tables into python model classes, we can use this utility module.
"""

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
        Establishes connection to data base
        
        :param username: db user id
        :param password: db password
        :param host_url: db connection host URL
        :param port: database host connection port
        :param service_name: service name
        """
        self.base = automap_base()
        conn_str = f'oracle+cx_oracle://{username}:{password}@{host_url}:{port}/?service_name={service_name}' # This is a sample connection string
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
        :param table: table name in the database
        :return: sqlalchemy.ext.declarative.api.DeclarativeMeta
        """
        return self.base.classes[table]

    @staticmethod
    def __gen_relationship(base, direction, return_fn, attrname, local_cls, referred_cls, **kwargs):
        """
        This method ensure that no ophan db entries are retained even after removing an entry that has foreign key relation with another table entry
        """
        if direction is interfaces.ONETOMANY:
            kwargs['cascade'] = 'all, delete-orphan'
            kwargs['passive_deletes'] = True
        return generate_relationship(base, direction, return_fn, attrname,
                                     local_cls, referred_cls, **kwargs)
    
    if __name__ == "__main__":
        # declare username, password, host_url, port, service_name
        db = DBConnect(username, password, host_url, port, service_name)
        # create a new session
        session = db.get_session()
        # connect to existing table, say there exists a table with name component
        component = db.get_table_object('component')
        # get row object
        component_obj = session.query(component).filter_by(component=self.component_name).filter_by(
                component_version=self.component_version).first()
        print(component_obj.name)
        session.close()
