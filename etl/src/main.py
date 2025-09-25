from src.db import ping, get_engine
from sqlalchemy import text


def main():
    ping()
    engine = get_engine()
    with engine.connect() as conn:
        version = conn.execute(text("SELECT VERSION()")).scalar_one()
    print(f"Connected to MySQL, server version: {version}")


if __name__ == "__main__":
    main()
