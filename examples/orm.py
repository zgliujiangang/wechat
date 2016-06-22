# coding: utf-8

from ._analyse import analyse


class SqlUtil(object):
    """
    目前不能进行联表查询
    """

    __table__ = None
    sql = None
    params = list()
    #count_sql = "SELECT FOUND_ROWS()"

    def __init__(self, table):
        # 初始化表名及数据
        self.sql = None
        self.params = []
        self.__table__ = table

        self._filter = None
        self._select = []
        self._page = None
        self._order = []

    def clear(self):
        # 清除数据
        self.sql = None
        self.params = []
        return self

    def table(self, table_name):
        #确定查询的表名
        self.__table__ = table_name
        return self

    def get(self, fields):
        #@param fields:["name", "sex", "age"]
        #@param kwargs:pk=1,name__like=Lucy
        #@param count:True or False是否获取数据count
        #查找数据
        fields = ["%s.%s" % (self.__table__, field) for field in fields]
        self._select = self._select.extend(fields)
        return self

    def page(self, offset, limit):
        #获取分页数据
        self.sql = "{sql} LIMIT %s, %s".format(self.sql)
        self.params.extend([offset, limit])
        return self

    def order_by(self, *args):
        self.sql = "%s ORDER BY %s" % (self.sql, ", ".join(args))
        return self

    def insert(self, **kwargs):
        #@param kwargs:name='Lucy',age=20,sex=0...
        #在数据库中插入一条数据
        params = kwargs.items()
        columns = [item[0] for item in params]
        values = [item[1] for item in params]
        _columns = ["{column}=%s".foramt(column=column) for column in columns]
        _columns = ", ".join(_columns)
        sql = "INSERT INTO {table} SET {columns}".format(table=self.__table__, columns=_columns)
        self.sql, self.params = sql, values
        return self

    def filter(self, **kwargs):
        conditions, params = self.__class__.analyse(**kwargs)
        return (conditions, params)

    def join(self):
        pass

    @classmethod
    def analyse(cls, **kwargs):
        #@param kwargs:pk=1,name__like=Lucy
        #解析查询参数
        _analyse = [analyse.analyse(cls.__table__, key, value) for key, value in kwargs.items()]
        conditions = [item[0] for item in _analyse]
        params = [item[1] for item in _analyse]
        return conditions, params

    @property
    def data(self):
        pass
    
    