# coding: utf-8

from ._analyse import analyse



class SqlBase(object):

    __table__ = None

    def __init__(self, *args, **kwargs):
        self.filters = list()
        self.filters_params = list()

    def table(self, table_name):
        #确定查询的表名
        self.__table__ = table_name
        return self

    def clear(self):
        self.filters = list()
        self.filters_params = list()
        return self

    def filter(self, **kwargs):
        filters, params = self.analyse(**kwargs)
        self.filters.extend(filters)
        self.filters_params.extend(params)
        return self

    def analyse(self, **kwargs):
        #@param kwargs:pk=1,name__like=Lucy
        #解析查询参数
        _analyse = [analyse.analyse(self.__table__, key, value) for key, value in kwargs.items()]
        filters = [item[0] for item in _analyse]
        params = [item[1] for item in _analyse]
        return filters, params

    def _break(self, **kwargs):
        #解析要插入的数据
        kwargs = kwargs.items()
        return [item[0] for item in kwargs], [item[1] for item in kwargs]

    def data(self):
        return None


class SqlSearch(SqlBase):
    """
    目前不能进行联表查询
    SELECT FOUND_ROWS();
    """

    def __init__(self, table):
        # 初始化表名及数据
        super(SqlSearch, self).__init__()
        self.__table__ = table
        self._select = list()
        self._join = list()
        self._page = list()
        self._order = list()
        self._count = False

    def clear(self):
        # 清除数据
        super(SqlSearch, self).clear()
        self._select = list()
        self._join = list()
        self._page = None
        self._order = list()
        self._count = False
        return self

    def get(self, fields):
        #@param fields:["name", "sex", "age"]
        #@param kwargs:pk=1,name__like=Lucy
        #@param count:True or False是否获取数据count
        #查找数据
        fields = ["%s.%s" % (self.__table__, field) for field in fields]
        self._select.extend(fields)
        return self

    def page(self, offset=0, limit=20):
        #获取分页数据
        self._page = (offset, limit)
        return self

    def order_by(self, *args):
        self._order = args
        return self

    def join(self, table, condition):
        table = self.__class__(table)
        self._join.append((table, condition))
        return self

    def join_get(self, fields):
        if len(self._join) == 0:
            raise ValueError('join table must set before get!')
        join = self._join[-1]
        join[0].get(fields)
        return self

    def join_filter(self, **kwargs):
        if len(self._join) == 0:
            raise ValueError('join table must set before get!')
        join = self._join[-1]
        join[0].filter(**kwargs)
        return self

    def count(self):
        self._count = True
        return self

    def data(self):
        select_sql = "SELECT %s FROM %s" if not self._count else "SELECT SQL_CALC_FOUND_ROWS %s FROM %s"
        join_sql = clause_sql = limit_sql = order_sql = str()
        _select = self._select + list()
        filters = self.filters + list()
        filters_params = self.filters_params + list()
        for table, condition in self._join:
            join_sql = "%s LEFT JOIN %s ON %s" % (join_sql, table.__table__, condition)
            _select.extend(table._select)
            filters.extend(table.filters)
            filters_params.extend(table.filters_params)
        if filters:
            clause_sql = "WHERE %s" % " AND ".join(filters)
        if self._page:
            limit_sql = "LIMIT %s, %s" % self._page
        if self._order:
            order_sql = "ORDER BY %s" % ", ".join(self._order)
        if not _select:
            raise ValueError('you should select at least one cloumn!')
        select_sql = select_sql % (", ".join(_select), self.__table__)
        sql = " ".join([select_sql, join_sql, clause_sql, limit_sql, order_sql])
        return (sql, filters_params)


class SqlInsert(SqlBase):

    def __init__(self, table):
        # 初始化表名及数据
        super(SqlInsert, self).__init__()
        self.__table__ = table
        self.columns = list()
        self.columns_params = list()

    def clear(self):
        super(SqlInsert, self).clear()
        self.columns = list()
        self.columns_params = list()
        return self

    def insert(self, **kwargs):
        #@param kwargs:name='Lucy',age=20,sex=0...
        #在数据库中插入一条数据
        self.columns, self.columns_params = self._break(**kwargs)
        return self

    def data(self):
        columns = ["{column}=%s".format(column=column) for column in self.columns]
        if not columns:
            raise ValueError("you should insert at least one column!")
        columns = ", ".join(columns)
        sql = "INSERT INTO {table} SET {columns}".format(table=self.__table__, columns=columns)
        params = self.columns_params
        return (sql, params)


class SqlUpdate(SqlBase):

    def __init__(self, table):
        # 初始化表名及数据
        super(SqlUpdate, self).__init__()
        self.__table__ = table
        self.columns = list()
        self.columns_params = list()

    def clear(self):
        super(SqlUpdate, self).clear()
        self.columns = list()
        self.columns_params = list()
        return self

    def update(self, **kwargs):
        self.columns, self.columns_params = self._break(**kwargs)
        return self

    def data(self):
        columns_sql = "UPDATE %s SET %s"
        columns = ["{column}=%s".format(column=column) for column in self.columns]
        if not columns:
            raise ValueError("you should update at least one column!")
        columns = ", ".join(columns)
        columns_sql = columns_sql % (self.__table__, columns)
        clause_sql = ""
        if self.filters:
            clause_sql = "WHERE %s" % " AND ".join(self.filters)
        sql = "%s %s" % (columns_sql, clause_sql)
        params = self.columns_params + self.filters_params
        return (sql, params)
    
    