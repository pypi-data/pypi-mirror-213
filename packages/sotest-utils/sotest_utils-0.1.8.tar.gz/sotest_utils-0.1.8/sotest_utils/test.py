import json
from inspect import isfunction


def sotest_test_case(test_name="", group="", author="", level="", cmdb_name="", cid="", case_desc=""):
    """
    sotest test case扫描标识
    :param test_name: 用例名称
    :param group: 用例分组，用于soTest页面展示分组
    :param author: 作者，用于标记
    :param level: 用例级别：L1: 冒烟测试用例，L2: 重要功能用例，L3: 一般功能用例，L4: 生僻功能用例
    :param cmdb_name: 系统名称
    :param cid: 用例uuid唯一标识，在项目中需要保证其唯一性，用于用例更新时匹配的id，未配置时使用：package + class + method name,
                在线生成地址：https://www.guidgenerator.com/
    :param case_desc 用例描述
    :return:
    """
    name = test_name
    if isfunction(test_name):
        name = test_name.__name__
    import allure
    return allure.label("sotest_test_case",
                        json.dumps(dict(test_name=name, group=group, author=author, level=level, cmdb_name=cmdb_name,
                                        cid=cid, case_desc=case_desc)))
