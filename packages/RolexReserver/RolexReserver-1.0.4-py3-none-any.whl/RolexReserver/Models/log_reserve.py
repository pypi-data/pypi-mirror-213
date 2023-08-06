import LibHanger.Models.modelFields as fld
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.sql.elements import Null

# Baseクラス生成
Base = declarative_base()

class log_reserve(Base):

	"""
	log_reserveテーブルクラス
	
	Parameters
    ----------
    Base : 
        Baseクラス
	"""
    
	# テーブル名
	__tablename__ = 'log_reserve'
	
	# スキーマ
	__table_args__ = {'schema': 'rolexre'}
	
	# 列定義
	logtime = fld.DateTimeFields(primary_key=True,default=Null)
	status = fld.NumericFields(1,0,default=0)
	html = fld.CharFields(8000,default='')
	updinfo = fld.CharFields(40,default='')

