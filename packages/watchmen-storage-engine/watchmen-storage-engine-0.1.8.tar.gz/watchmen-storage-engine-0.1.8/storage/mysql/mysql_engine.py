import json

from sqlalchemy import create_engine

from storage.config.config import settings
from storage.utils.date_utils import DateTimeEncoder


def dumps(o):
    return json.dumps(o, cls=DateTimeEncoder)


connection_url = 'mysql+mysqldb://%s:%s@%s:%s/%s' % (settings.MYSQL_USER,
                                                     settings.MYSQL_PASSWORD,
                                                     settings.MYSQL_HOST,
                                                     settings.MYSQL_PORT,
                                                     settings.MYSQL_DATABASE)

engine = create_engine(connection_url,
                       echo=True,
                       future=True,
                       pool_recycle=3600,
                       json_serializer=dumps)
