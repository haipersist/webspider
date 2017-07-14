__author__ = 'haibo'
#encoding:utf8


def cookie2scrapy(cookies):
    """
    the function is used to covert the cookies that
     gotten from response using requests module to the style
     which can be used in scrapy.
     the style of original cookie:
      f=dwd;dsd=gdfg;g_d=1334

     In scrapy,the cookie must exist in dict format.
     Like this:
     {
     'f':'d',
     'w':'g'
    }
    :param cookies:
    :return:
    """
    cookie_list = cookies.split(';')
    cookie_list = map(lambda x:x.split('='),cookie_list)
    cookie_list = [{x[0]:x[1]} for x in cookie_list]
    scrapy_cookies = {}
    for item in cookie_list:
        scrapy_cookies.update(item)
    return scrapy_cookies



if __name__ == "__main__":
    cookies = """
    user_trace_token=20170327064902-b36275bfffde4c5ca209ca81349f8aaa; _ga=GA1.2.344451825.1490568536; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6
=1499929502; LGUID=20170327064902-68464139-1276-11e7-a304-525400f775ce; JSESSIONID=ABAAABAACDBAAIAB1AB69AE1192C8ACC3001B5E7E98558F
; X_HTTP_TOKEN=c39596d4e2fcb5042b60c89b648d0974; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1499929721
; LGSID=20170713150502-972ac068-6799-11e7-a82b-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND
=https%3A%2F%2Fpassport.lagou.com%2Flogin%2Flogin.html%3Fts%3D1499929500812%26serviceId%3Dlagou%26service
%3Dhttp%25253A%25252F%25252Fwww.lagou.com%25252Fjobs%26action%3Dlogin%26signature%3D29AAF895E0021662F49316D0B4D168A6
; LGRID=20170713150840-192d6e84-679a-11e7-b83e-525400f775ce; _gid=GA1.2.291952946.1499929504; _gat=1
; index_location_city=%E5%8C%97%E4%BA%AC; TG-TRACK-CODE=search_code; SEARCH_ID=94054433704c44139fd05
6f489f15c12
    """
    print cookie2scrapy(cookies).items()

