
"""
Author:Haibo Wang
Date:2017-03-01
E-mail:hbnnlong@163.com
"""


from webspider.spider.jobspider.items import CompanyItem





def dict_decorator(method):
    """
    the decorator is used to convert scrapyd item into dict structure
    the scrapyed item contains two instances:JobItem and CompanyItem.
    they are defined in items.py

    :param method:it is the method of one class instance
    :return:

    """
    def to_dict(decorated_instance, item,spider):
        result = {}
        for key in item:
            result[key] = item[key]
            if isinstance(item[key], CompanyItem):
                company = {}
                for ele in result[key]:
                    company[ele] = result[key][ele]
                result[key] = company
        method(decorated_instance,result,spider)

    return to_dict


