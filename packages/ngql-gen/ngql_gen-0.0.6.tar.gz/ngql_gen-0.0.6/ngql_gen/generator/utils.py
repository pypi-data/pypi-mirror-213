# Python类型到Ngsl类型的映射
import datetime


TypeToNgsl = {
    'str': 'String',
    'int': 'Int64',
    'float': 'Float',
    'bool': 'Bool',
    'datetime': 'DateTime',
    'date': 'Date',
    'time': 'Time',
    'timestamp': 'Timestamp',
    'set': 'Set',
    'map': 'Map',
}


# 从类中获取属性的类型名
def typeNameFromClass(obj, key) -> str:
    return obj.__annotations__[key].__name__


# 从类中获取属性的键值对
def ClassToSchema(obj):
    # 获取obj的所有属性名和类型
    props = ""
    for key in obj.__fields__.keys():
        # 如果属性类型在TypeToNgsl中
        if typeNameFromClass(obj, key) in TypeToNgsl:
            props += f'{key} {TypeToNgsl[typeNameFromClass(obj, key)]}, '

    return f'{obj.__name__}({props[:-2]})'

# 从类中获取属性的键值对，只包含主键
def ClassToSchemaWithOnlyKey(obj):
    # 获取obj的所有属性名和类型
    props = ""
    # print(obj.__annotations__)
    for key in obj.__annotations__.keys():
        # print(key)
        # 如果属性类型在TypeToNgsl中
        if typeNameFromClass(obj, key) in TypeToNgsl:
            props += f'{key}, '

    return f'{obj.__name__}({props[:-2]})'

# 实例转换为属性的键值对
def InstanceToField(obj: object):
    # 获取obj的所有属性名和属性值
    props = ""
    for key in obj.__annotations__.keys():
        props += f'{obj.__dict__[key]}, '

    return f'{obj.__class__.__name__}({props[:-2]})'

# 检查有无None值，如果有且属性类型为str，则替换为空字符串，如果属性为数字类型，则替换为0
def CheckNone(obj: object):
    for key in obj.__annotations__.keys():
        if obj.__dict__[key] is None:
            if typeNameFromClass(obj, key) == 'str':
                obj.__dict__[key] = ""
            elif typeNameFromClass(obj, key) == 'int':
                obj.__dict__[key] = 0
            elif typeNameFromClass(obj, key) == 'float':
                obj.__dict__[key] = 0.0
            elif typeNameFromClass(obj, key) == 'bool':
                obj.__dict__[key] = False
            elif typeNameFromClass(obj, key) == 'datetime':
                obj.__dict__[key] = datetime.datetime.now()
            elif typeNameFromClass(obj, key) == 'date':
                obj.__dict__[key] = datetime.date.today()
            elif typeNameFromClass(obj, key) == 'time':
                obj.__dict__[key] = datetime.datetime.now().time()
            elif typeNameFromClass(obj, key) == 'timestamp':
                obj.__dict__[key] = datetime.datetime.now().timestamp()
            elif typeNameFromClass(obj, key) == 'set':
                obj.__dict__[key] = set()
            elif typeNameFromClass(obj, key) == 'map':
                obj.__dict__[key] = dict()
            else:
                obj.__dict__[key] = None
    return obj

 # 获取obj的所有属性值
def GetProps(obj: object) -> str:
    props = ""

    # 检查有无None值
    obj = CheckNone(obj)

    for key in obj.__annotations__.keys():
        if isinstance(obj.__dict__[key], str):
            props += f"'{obj.__dict__[key]}', "
        elif isinstance(obj.__dict__[key], datetime.datetime):
            props += f"datetime('{obj.__dict__[key]}'), "
        else:
            props += f'{obj.__dict__[key]}, '
    props = props[:-2]
    return props

# 字典转换为属性的键值对
def DictToSchema(name: str, props: dict):
    props_str = ""
    for key in props.keys():
        props_str += f"{key} {props[key]}, "
    props_str = props_str[:-2]
    return f"{name}({props_str})"