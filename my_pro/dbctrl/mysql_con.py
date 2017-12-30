# coding: utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from contextlib import contextmanager


class OperateDatabase(object):
	link_str = "mysql://root:Callkin@123456@192.168.1.10:3306/fmea?charset=utf8mb4"
	engine = create_engine(link_str)
	session = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))

	@property
	def get_session(self):
		return self.session()

	@contextmanager
	def session_scope(self):
		session = self.get_session
		try:
			yield session
			session.commit()
		except:
			session.rollback()
			raise
		finally:
			session.close()


if __name__ == '__main__':
	pass
