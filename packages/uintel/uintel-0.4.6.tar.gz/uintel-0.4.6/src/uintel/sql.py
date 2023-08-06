"""Connect to SQL databases.

Connect (or create) databases on postgreSQL servers, as well as upload DataFrames to databases quickly and efficiently.
"""

__all__ = ["connect", "upload"]

import io, sqlalchemy, sqlalchemy_utils, psycopg2, pandas, warnings
from .install import _get_config, _save_config

def connect(database_name: str, host: str, sslmode: str ="require") -> dict:
    """Connect to a database.

    Connect to a given database (e.g. 'chap'), using the stored credentials for SQL for the host (e.g. encivmu-tml62). If the database does not exist, then a new database is created with this database_name. 

    Args:
        database_name: The name of the database to connect to, or create if it does not exist.
        host: The name or address of the SQL table host.
        sslmode: The method for SSL authentication. Acceptable values are: "disable", "allow", "prefer", "require". Please note that "verify-ca" and "verify-full" are acceptable values, but have not been implemented in this function and will fallback to the "require" method. 
    
    Returns:
        A dictionary containing a sqlalchemy Engine ('engine') and a psycopg2 connection ('con').
    """

    config = _get_config()
    try:
        credentials = config["sql"][host]
    except KeyError:
        warnings.warn(f"Unfortunately, {host} is not in your saved SQL databases.")
        credentials = {
            "port": int(input(f"What port is the SQL database on {host}? (e.g. 5002) ")),
            "username": input("What is the username to connect to SQL? (e.g. postgres) "),
            "password": input("What is the password to connect to SQL? ")
        }
        # Save this new connection to the UI configuration file
        config["sql"][host] = credentials
        _save_config(config)

    # Check the SSL method
    if sslmode not in ["disable", "allow", "prefer", "require", "verify-ca", "verify-full"]:
        warnings.warn(f"The SSL mode of {sslmode} is unacceptable. The 'prefer' SSL mode will be used to connect with the database.")
        sslmode = "prefer"
    if sslmode in ["verify-ca", "verify-full"]:
        warnings.warn(f"The SSL mode of {sslmode} has not been set up in the uintel package, as certificates were notoriously tricky to share and implement with psycopg2. The 'require' SSL mode will be used instead.")
        sslmode = "require"
    connect_args = {"sslmode": sslmode}

    # Create the engine to the database
    engine = sqlalchemy.create_engine(f"postgresql+psycopg2://{credentials['username']}:{credentials['password']}@{host}/{database_name}?port={credentials['port']}", connect_args=connect_args)

    # Create the database if it doesn't exist
    if not _database_exists(database_name, engine, connect_args):
        _create_database(database_name, engine, connect_args)

    # Make a connection to the database
    connection = psycopg2.connect(f"host={host} dbname={database_name} user={credentials['username']} password='{credentials['password']}' port={str(credentials['port'])}", **connect_args)

    return {"engine": engine, "con": connection}
    

def _database_exists(database_name: str, engine, connect_args: dict):
    """Check if a postgis database exists.

    Checks if a databse already exists in postgreSQL. 

    Args:
        database_name: The name of the database.
        engine: A SQLAlchemy engine.
        connect_args: A dictionary of connection arguments passed to sqlalchemy.create_engine function. These usually pertain to SSL connections.

    Returns:
        A boolean which is True if the given database_name exists.
    """

    url = sqlalchemy_utils.functions.database._set_url_database(engine.url, "postgres")
    engine = sqlalchemy.create_engine(url, connect_args=connect_args)
    existing_tables = pandas.read_sql(f"SELECT datname FROM pg_database WHERE datname = '{database_name}' AND datistemplate = 'false' AND datallowconn = 'true'", engine)
    engine.dispose()
    return len(existing_tables) > 0
        

def _create_database(database_name: str, engine, connect_args: dict):
    """Create a new postgis database.

    Create a new database in postgres and enable the postgis extension.

    Args:
        database_name: The name of the database to connect to, or create if it does not exist.
        engine: A SQLAlchemy engine.
        connect_args: A dictionary of connection arguments passed to sqlalchemy.create_engine function. These usually pertain to SSL connections.

    Returns:
        None.
    """

    # Connect to the postgres table (poentially using SSL) and create the new table
    url = sqlalchemy_utils.functions.database._set_url_database(engine.url, "postgres")
    engine = sqlalchemy.create_engine(url, isolation_level='AUTOCOMMIT', connect_args=connect_args)
    with engine.begin() as conn:
        _ = conn.execute(sqlalchemy.text(f"""CREATE DATABASE "{database_name}" ENCODING 'utf8' TEMPLATE template1"""))
    engine.dispose()
    
    # Connect to the new database (potentially using SSL) and enable the postgis extension
    url = sqlalchemy_utils.functions.database._set_url_database(engine.url, database_name)
    engine = sqlalchemy.create_engine(url, isolation_level='AUTOCOMMIT', connect_args=connect_args)
    with engine.begin() as conn:
        _ = conn.execute(sqlalchemy.text("CREATE EXTENSION postgis"))
    engine.dispose()


def upload(df: pandas.DataFrame, table_name: str, db: dict, if_exists: str = "replace") -> None:
    """Upload a DataFrame.

    Upload a Pandas Dataframe to a SQL table called table_name. 

    Args:
        df: The pandas.DataFrame to upload.
        table_name: The name of the table to upload the dataframe to.
        db: A dictionary of the SQL database engine and connection.
        if_exists: The action to undertake if the table_name exists. E.g. "replace" or "append".

    Returns:
        None.
    """

    # Truncates the table and sends the column names to sql
    df.head(0).to_sql(table_name, db['engine'], if_exists=if_exists, index=False) 
    
    # Open connection to sql
    conn = db['engine'].raw_connection()
    cur = conn.cursor()
    
    # Send dataframe to stringio
    output = io.StringIO()
    df.to_csv(output, sep='\t', header=False, index=False)
    
    # Send stringio to sql
    output.seek(0)
    cur.copy_from(output, table_name, null="") # null values become ''
    conn.commit()
