import yaml

# 配置文件
config = None

# 默认配置
default_config = {
    'default_v1_name': 'v1',
    'default_v2_name': 'v2',
    'default_e_name': 'e',
}

# 读取配置文件(config.yaml)
with open('config.yaml', 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# 如果配置文件中没有配置default_v1_name, default_v2_name, default_e_name, 则使用默认配置
if 'default_v1_name' not in config:
    config['default_v1_name'] = default_config['default_v1_name']
if 'default_v2_name' not in config:
    config['default_v2_name'] = default_config['default_v2_name']
if 'default_e_name' not in config:
    config['default_e_name'] = default_config['default_e_name']
