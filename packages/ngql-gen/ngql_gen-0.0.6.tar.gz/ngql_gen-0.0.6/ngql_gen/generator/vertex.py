
from ngql_gen.generator.utils import *


class Vertex_Ngql():
    # 在NebulaGraph实例的指定图空间中插入一个或多个点
    def Insert(obj: object, vid: str, if_not_exists: bool = True):
        return f"INSERT VERTEX{' IF NOT EXISTS' if if_not_exists else ''} {ClassToSchemaWithOnlyKey(obj.__class__)} " \
            f"VALUES '{vid}':({GetProps(obj)});"

    # 删除点，以及点关联的出边和入边
    def Delete(vid: str):
        return f"DELETE VERTEX '{vid}';"
