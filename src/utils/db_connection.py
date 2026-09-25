from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

def get_engine():
    url = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    return create_engine(url)

def test_connection():
    try:
        engine = get_engine()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT VERSION();"))
            print("connected😃")
            print("MySQL version:",result.fetchone()[0])
    except Exception as e:
        print("Connection Failed☹️",e)
        
if __name__ == "__main__":
    test_connection()
    
                        