# coding: utf-8

from ._analyse import analyse


class SqlFormat(object):
    """
    目前不能进行联表查询
    SELECT FOUND_ROWS();
    """

    __table__ = None

    def __init__(self, table):
        # 初始化表名及数据
        self.__table__ = table
        self._select = []
        self._join = []
        self._filters = []
        self._params = []
        self._page = []
        self._order = []
        self._count = False

    def clear(self):
        # 清除数据
        self._select = []
        self._join = []
        self._filters = []
        self._params = []
        self._page = []
        self._order = []
        self._count = False
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

    def filter(self, **kwargs):
        filters, params = self.analyse(**kwargs)
        self._filters.extend(filters)
        self._params.extend(params)
        return self

    def page(self, offset, limit):
        #获取分页数据
        self._page = [offset, limit]
        return self

    def order_by(self, *args):
        self._order = args
        return self

    def join(self, table, fields, condition, **kwargs):
        table = self.__class__(table).get(fields).filter(**kwargs)
        self._join.append((table, condition))
        return self

    def count(self):
        self._count = True
        return self

    def insert(self, **kwargs):
        #@param kwargs:name='Lucy',age=20,sex=0...
        #在数据库中插入一条数据
        columns, params = self.write(**kwargs)
        sql = "INSERT INTO {table} SET {columns}".format(table=self.__table__, columns=columns)
        return (sql, params)

    def update(self, values, filters):
        up_sql = "UPDATE %s SET %s"
        columns, params = self.write(**values)
        up_sql = up_sql % (self.__table__, columns)
        clause_sql = ""
        if filters:
            _filters, _params = self.analyse(**filters)
            clause_sql = "WHERE %s" % " AND ".join(filters)
            params.extend(_params)
        sql = "%s %s" % (up_sql, clause_sql)
        return (sql, params)

    def analyse(self, **kwargs):
        #@param kwargs:pk=1,name__like=Lucy
        #解析查询参数
        _analyse = [analyse.analyse(self.__table__, key, value) for key, value in kwargs.items()]
        filters = [item[0] for item in _analyse]
        params = [item[1] for item in _analyse]
        return filters, params

    def write(self, **kwargs):
        kwargs = kwargs.items()
        params = [item[1] for item in kwargs]
        columns = [item[0] for item in kwargs]
        columns = ["{column}=%s".foramt(column=column) for column in columns]
        columns = ", ".join(_columns)
        return columns, params

    @property
    def data(self):
        select_sql = "SELECT %s FROM %s" if not self._count else "SELECT SQL_CALC_FOUND_ROWS %s FROM %s"
        join_sql = ""
        clause_sql = ""
        limit_sql = ""
        order_sql = ""
        for table, condition in self._join:
            join_sql = "%s LEFT JOIN %s ON %s" % (join_sql, table.__table__, condition)
            self._select.extend(table._select)
            self._filters.extend(table._filters)
            self._params.extend(table._params)
        if self._filters:
            clause_sql = "WHERE %s" % " AND ".join(self._filters)
        if self._page:
            limit_sql = "LIMIT %s, %s" % self._page
        if self._order:
            order_sql = "ORDER BY %s" % ", ".join(self._order)
        select_sql = select_sql % (" ".join(self._select), self.__table__)
        sql = " ".join[select_sql, join_sql, clause_sql, limit_sql, order_sql]
        params = self._params
        return (sql, params)
    
    