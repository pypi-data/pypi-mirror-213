# Tag 相关 Ngql语句
from ngql_gen.generator.utils import DictToSchema
from ngql_gen.model.tag import Tag


class Tag_Ngql:
    '''
    Tag 相关 Ngql语句
    '''
    # 创建Tag
    def Create(tag: Tag, if_not_exists: bool = True):
        return f"CREATE TAG{' IF NOT EXISTS' if if_not_exists else ''} { DictToSchema(tag.name, tag.properties) };"

    # 删除当前工作空间内所有点上的指定 Tag
    def Drop(tag_name: str, if_exists: bool = True):
        return f"DROP TAG{' IF EXISTS' if if_exists else ''} {tag_name};"

    # 删除指定点上的指定 Tag
    def DeleteFromTag(tag_name: str, vid: str):
        return f"DELETE {tag_name} FROM {vid};"

    # 显示所有Tag
    def ShowAll():
        return "SHOW TAGS;"

    # 显示指定Tag的信息
    def Describe(tag_name: str):
        return f"DESCRIBE TAG {tag_name};"
