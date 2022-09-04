import os

def get_postgres_uri():
    host = "172.17.0.4"  # os.environ.get("DB_HOST", "localhost")
    port = 5432 if host == "127.0.0.1" else 5432
    password = os.environ.get("DB_PASSWORD", "postgres")
    db_name = "postgres"  # os.environ.get("DB_NAME", "postgres")
    user = "postgres"
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
