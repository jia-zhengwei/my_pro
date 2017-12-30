# coding: utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from contextlib import contextmanager


class OperateDatabase(object):
    db_str = 'mysql://root:Callkin@123456@192.168.1.10:3306/fmea?charset=utf8mb4'
    engine = create_engine(db_str, echo=False)
    SessionType = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))

    @property
    def GetSession(self):
        return self.SessionType()

    @contextmanager
    def session_scope(self):
        session = self.GetSession
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()


if __name__ == '__main__':
    # engine = create_engine(Conf().msqconf(), echo=True)
    # operat = OperateDatabase()
    # print(operat.engine)
    # # Session = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))()
    # conf = Conf()
    # print(conf.msqconf())
    pass



