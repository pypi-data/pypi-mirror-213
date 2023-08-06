from ngql_gen.config import config


class Select_Ngql:
    '''
    Select 相关 Ngql语句
    '''
    def GetAllVertexs(typ: str = "", limit: int = 10):
        v1 = config['default_v1_name']
        pattern = f'({v1})' if typ == '' else f'({v1}: {typ})'
        output = v1
        return f'MATCH {pattern} RETURN {output} LIMIT {limit};'
    
    def GetAllEdges(limit: int = 10):
        e = config['default_e_name']
        pattern = f"()-[{e}]->()"
        output = e
        return f'MATCH {pattern} RETURN {output} LIMIT {limit};'
    
    def GetEdgesFromVertex(obj: object,prop_name: str,prop_value, limit: int = 10):
        v1 = config['default_v1_name']
        e = config['default_e_name']

        # 检查prop_value是否为字符串，如果是则加上引号
        if isinstance(prop_value, str):
            prop_value = f"'{prop_value}'"

        pattern = f'({v1}: {obj.__name__}{{{prop_name}:{prop_value}}})-[{e}]->()'
        output = e
        return f'MATCH {pattern} RETURN {output} LIMIT {limit};'
    
    def GetVertexByVid(vid: str):
        v1 = config['default_v1_name']
        return f"MATCH ({v1}) WHERE id({v1}) == '{vid}' RETURN {v1};"
    
    # 通过一个点获取所有与之相连的点
    def GetConnectedVertexs(obj:object, prop_name: str,prop_value: str):
        v1 = config['default_v1_name']
        v2 = config['default_v2_name']

        return f"MATCH ({v1}: {obj.__class__.__name__}{{{prop_name}: '{prop_value}'}})--({v2}) RETURN {v2};"
    
    # 通过一个点获取所有与之相连的点，限定边的类型
    def GetConnectedVertexsWidthEdgeType(v1_obj: object, prop_name: str,prop_value: str, edge_obj: object = None, v2_obj: object = None):
        v1 = config['default_v1_name']
        v2 = config['default_v2_name']

        if edge_obj is None and v2_obj is None:
            return f"MATCH ({v1}: {v1_obj.__name__}{{{prop_name}: '{prop_value}'}})--({v2}) RETURN {v2};"
        elif edge_obj is None:
            return f"MATCH ({v1}: {v1_obj.__name__}{{{prop_name}: '{prop_value}'}})--({v2}: {v2_obj.__name__}) RETURN {v2};"
        elif v2_obj is None:
            return f"MATCH ({v1}: {v1_obj.__name__}{{{prop_name}: '{prop_value}'}})-[e: {edge_obj.__name__}]-({v2}) RETURN {v2};"
        else:
            return f"MATCH ({v1}: {v1_obj.__name__}{{{prop_name}: '{prop_value}'}})-[e: {edge_obj.__name__}]-({v2}: {v2_obj.__name__}) RETURN {v2};"