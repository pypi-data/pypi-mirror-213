# eDGE 相关 Ngql语句\
from ngql_gen.generator import DictToSchema
from ngql_gen.model import edge_type


class EdgeType_Ngql:
    '''
    EdgeType 相关 Ngql语句
    '''
    # 创建EdgeType
    def Create(edge_type: edge_type,if_not_exists: bool = True):
        return f"CREATE EDGE{' IF NOT EXISTS' if if_not_exists else ''} { DictToSchema(edge_type.name, edge_type.properties) };"
    
    # 删除EdgeType
    def Drop(obj: object,if_exists: bool = True):
        return f"DROP EDGE{' IF EXISTS' if if_exists else ''} {obj.__name__};"
    
    # 显示所有EdgeType
    def ShowAll():
        return "SHOW EDGES;"
    
    # 显示指定EdgeType的信息
    def Describe(obj: object):
        return f"DESCRIBE EDGE {obj.__name__};"