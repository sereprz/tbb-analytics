from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Database:
    def __init__(self, db_name, host, username, password, port):
        
        self.engine = create_engine(
            f'postgresql://{username}:{password}@{host}:{port}/{db_name}')
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
    
    def commit_session(self):
        self.session.commit()
        
    def close_session(self):
        self.session.close()