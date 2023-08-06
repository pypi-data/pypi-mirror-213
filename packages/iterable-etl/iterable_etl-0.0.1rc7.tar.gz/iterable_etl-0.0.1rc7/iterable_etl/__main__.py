"""__main__"""
from dotenv import load_dotenv
from iterable_etl import iterable_etl

if __name__ == "__main__":
    load_dotenv()
    iterable_etl.main()
