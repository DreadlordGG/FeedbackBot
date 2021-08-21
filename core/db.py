import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from core.logging import getLogger
from functools import wraps
logger = getLogger(__name__)
class pgsql:
    def __init__(self, database):
        self.database = database

    def with_connection(f):
        @wraps(f)
        def with_connection_(self, *args, **kwargs):
            DB_CONNECTION_STRING = "dbname=%s host=%s user=%s password=%s" % (self.database, '127.0.0.1',  os.getenv('DATABASE_USER'), os.getenv('DATABASE_PASSWORD'))
            try:
                cnn = psycopg2.connect(DB_CONNECTION_STRING)
                cnn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);
                Cursor = cnn.cursor()
            except Exception as e:
                logger.error("Database connection failed %s", e)
                raise
            try:
                rv = f(Cursor, *args, **kwargs)
            except Exception as e:
                cnn.rollback()
                logger.error("Query to %s failed %s",cnn, e)
                raise
            finally:
                cnn.close()
            return rv
        return with_connection_
        
    @with_connection
    def query(Cursor, query):
        Cursor.execute(query)
        result = Cursor.fetchone()
        return query

    @with_connection
    def init(self, Cursor):
        try:
            Cursor.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(self.database))
            )
            logger.info(f'[{self.database}] has been created')
            return
        except psycopg2.errors.DuplicateDatabase as e:
            logger.warning(f'[{self.database}] already exists. Moving on...')
            return
        except Exception as e:
            logger.error(f'[{self.database}] creation failed. {e}.')
            raise
"""         else:
            try:
                print("i reach here")
                Cursor.execute("CREATE TABLE vendors (vendor_id SERIAL PRIMARY KEY,vendor_name VARCHAR(255) NOT NULL)")
                logger.info(f'Tables structure for [{self.database}] has been created')
                return
            except psycopg2.errors.DuplicateTable as e:
                logger.warning(f'Table structure for [{self.database}] already exists. Moving on...')
                return
            except Exception as e:
                logger.error(f'[{self.database}] creation failed. {e}.') """




