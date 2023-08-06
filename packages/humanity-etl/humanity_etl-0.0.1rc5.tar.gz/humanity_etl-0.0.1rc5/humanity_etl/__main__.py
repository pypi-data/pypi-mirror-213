"""__main__"""
from dotenv import load_dotenv
from humanity_etl import humanity_etl

if __name__ == "__main__":
    load_dotenv()
    humanity_etl.main()
