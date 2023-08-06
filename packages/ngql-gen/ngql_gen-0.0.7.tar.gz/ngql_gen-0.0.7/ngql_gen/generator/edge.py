from ngql_gen.generator.utils import *


class Edge_Ngql():
    '''
    Edge 相关 Ngql语句
    '''

    # 在NebulaGraph实例的指定图空间中插入一条或多条边
    def Insert(obj: object, src: str, dst: str, if_not_exists: bool = True):
        return f"INSERT EDGE{' IF NOT EXISTS' if if_not_exists else ''} {ClassToSchemaWithOnlyKey(obj.__class__)} " \
            f"VALUES '{src}'->'{dst}':({GetProps(obj)});"

    # 删除边。一次可以删除一条或多条边
    def Delete(obj: object, src_vid: str, dst_vid: str):
        return f"DELETE EDGE {obj.__class__.__name__} '{src_vid}'->'{dst_vid}'@0;"
