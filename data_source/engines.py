from data_source.exception import DataBaseConnectError
import sqlalchemy as sa


def get_engine(data_source):
    try:
        if data_source['engine'] == 'doris':
            # 'mysql+pymysql://admin:xxxxxxxxxxxxxxxx@xxx.xxx.xxx.xxx:xxxx/dbcenter'
            return sa.create_engine('mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}'
                                    .format(user=data_source['user'],
                                            passwd=data_source['passwd'],
                                            host=data_source['host'],
                                            port=data_source['port'],
                                            db=data_source['db']))
        elif data_source['engine'] == 'vertica':
            return sa.create_engine('vertica+vertica_python://{user}:{passwd}@{host}:{port}/{db}'
                                    .format(user=data_source['user'],
                                            passwd=data_source['passwd'],
                                            host=data_source['host'],
                                            port=data_source['port'],
                                            db=data_source['db']))
    except Exception as e:
        raise DataBaseConnectError('executing function "%s.engine" caught %s'%(__name__, e))
