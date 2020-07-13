from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func

class Database:
    def __init__(self, config_dict):

        self.engine = create_engine(
            f'postgresql://{config_dict["user"]}:{config_dict["pwd"]}@{config_dict["host"]}:{config_dict["port"]}/{config_dict["db_name"]}')
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
    
    def get_latest(self, analytics_table, dispatch_table):
        '''
            Returns the most recent rows in dispatch_table that haven't yet been added to analytics_table
        '''
        latest = self.session.query(func.max(analytics_table.updated_at)).first()[0]
        
        if latest:
            rows = self.session.query(dispatch_table).filter(dispatch_table.updated_at > latest).all()
        else:
            rows = self.session.query(dispatch_table).all()
        
        return rows
        
    def commit_session(self):
        self.session.commit()
        
    def close_session(self):
        self.session.close()
