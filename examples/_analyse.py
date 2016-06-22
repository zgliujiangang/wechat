# coding: utf-8

import re

class FieldBaseAnalyse(object):

    mode_funcs = dict()
    pattern = re.compile(r'^(?P<field>\w+?)__(?P<mode>\w+)$')

    def add(self, mode):
        def decorator(func):
            self.register(mode, func)
            return func
        return decorator

    def register(self, mode, func):
        self.mode_funcs[mode] = func
    
    def analyse(self, table, key, value):
        #@param param:name='Lucy';name__like='Lucy';name__contains='Lucy'
        match = pattern.match(key)
        if match:
            field, mode = match.groups()
            if mode in self.mode_funcs:
                return self.mode_funcs[mode](table, field, value)
            else:
                raise KeyError("mode funcs doesn't match!")
        else:
            field = param
            return "{table}.{field} = %s".format(table=table, field=field)


base_analyse = FieldBaseAnalyse()


@base_analyse.add("in")
def field_in(table, field, value):
    if not isinstance(value, list):
        value = [value]
    return "{table}.{field} in %s".format(table=table, field=field), value

@base_analyse.add("gt")
def field_gt(table, field, value):
    return "{table}.{field} > %s".format(table=table, field=field), value

@base_analyse.add("lt")
def field_lt(table, field, value):
    return "{table}.{field} < %s".format(table=table, field=field), value

@base_analyse.add("gte")
def field_gte(table, field, value):
    return "{table}.{field} >= %s".format(table=table, field=field), value

@base_analyse.add("lte")
def field_lte(table, field, value):
    return "{table}.{field} <= %s".format(table=table, field=field), value

@base_analyse.add("like")
def field_like(table, field, value):
    return "{table}.{field} LIKE %s".format(table=table, field=field), "%s%s%s" % ("%", value, "%")

@base_analyse.add("start_with"):
def field_like(table, field, value):
    return "{table}.{field} LIKE %s".format(table=table, field=field), "%s%s" % (value, "%")

@base_analyse.add("end_with"):
def field_like(table, field, value):
    return "{table}.{field} LIKE %s".format(table=table, field=field), "%s%s" % ("%", value)


class FieldAnalyse(FieldBaseAnalyse):

    def __init__(self, *args, **kwargs):
        super(FieldAnalyse, self).__init__(*args, **kwargs)
        self.mode_funcs = base_analyse.mode_funcs


analyse = FieldAnalyse()
