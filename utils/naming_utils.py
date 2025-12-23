import re
import logging

"""
命名格式转换工具模块，用于在驼峰命名和下划线命名之间进行转换
"""

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def to_camel_case(snake_str):
    """
    将下划线命名转换为驼峰命名
    
    Args:
        snake_str: 下划线命名的字符串
        
    Returns:
        驼峰命名的字符串
    """
    try:
        if not snake_str:
            return snake_str
        components = snake_str.split('_')
        # 首字母小写，后续单词首字母大写
        return components[0] + ''.join(x.title() for x in components[1:])
    except Exception as e:
        logger.error("转换为驼峰命名失败: %s", e)
        raise

def to_snake_case(camel_str):
    """
    将驼峰命名转换为下划线命名
    
    Args:
        camel_str: 驼峰命名的字符串
        
    Returns:
        下划线命名的字符串
    """
    try:
        if not camel_str:
            return camel_str
        # 在大写字母前添加下划线，然后转换为小写
        snake_str = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_str)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', snake_str).lower()
    except Exception as e:
        logger.error("转换为下划线命名失败: %s", e)
        raise

def convert_dict_keys(data, convert_func):
    """
    递归转换字典的键名
    
    Args:
        data: 要转换的数据（字典或列表）
        convert_func: 转换函数（to_camel_case 或 to_snake_case）
        
    Returns:
        转换后的字典或列表
    """
    try:
        if isinstance(data, dict):
            new_dict = {}
            for key, value in data.items():
                new_key = convert_func(key)
                new_dict[new_key] = convert_dict_keys(value, convert_func)
            return new_dict
        elif isinstance(data, list):
            return [convert_dict_keys(item, convert_func) for item in data]
        else:
            return data
    except Exception as e:
        logger.error("转换字典键名失败: %s", e)
        raise

def snake_to_camel_dict(data):
    """
    将字典的所有键从下划线命名转换为驼峰命名
    
    Args:
        data: 要转换的字典
        
    Returns:
        转换后的字典
    """
    return convert_dict_keys(data, to_camel_case)

def camel_to_snake_dict(data):
    """
    将字典的所有键从驼峰命名转换为下划线命名
    
    Args:
        data: 要转换的字典
        
    Returns:
        转换后的字典
    """
    return convert_dict_keys(data, to_snake_case)
