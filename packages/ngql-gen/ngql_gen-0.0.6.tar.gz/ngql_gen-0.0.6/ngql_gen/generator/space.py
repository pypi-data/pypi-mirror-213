# Space 相关 Ngql语句
class Space_Ngql:
    '''
    Space 相关 Ngql语句
    '''

    # 创建Space
    def Create(space_name:str, vid_type:str="FIXED_STRING(30)",if_not_exists: bool = True):
        return f"CREATE SPACE{' IF NOT EXISTS' if if_not_exists else ''} {space_name}(vid_type={vid_type});"
    
    # 删除Space
    def Drop(space_name:str,if_exists: bool = True):
        return f"DROP SPACE{' IF EXISTS' if if_exists else ''} {space_name};"
    
    # 显示所有Space
    def ShowAll():
        return "SHOW SPACES;"
    
    # 使用Space
    def Use(space_name:str):
        return f"USE {space_name};"
    
    # 显示指定图空间的信息
    def Describe(space_name:str):
        return f"DESCRIBE SPACE {space_name};"
    
    # 清空图空间中的点和边，但不会删除图空间本身以及其中的 Schema 信息
    def Clear(space_name:str,if_exists: bool = True):
        return f"CLEAR SPACE{' IF EXISTS' if if_exists else ''} {space_name};"
    
    # 克隆现有图空间的 Schema
    def Clone(space_name:str, new_space_name:str):
        return f"CREATE SPACE {new_space_name} as {space_name};"