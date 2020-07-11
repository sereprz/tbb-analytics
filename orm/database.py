from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Database:
    def __init__(self, config_dict):

        self.engine = create_engine(
            f'postgresql://{config_dict["user"]}:{config_dict["pwd"]}@{config_dict["host"]}:{config_dict["port"]}/{config_dict["db_name"]}')
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
    
    def commit_session(self):
        self.session.commit()
        
    def close_session(self):
        self.session.close()