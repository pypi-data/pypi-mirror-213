import requests


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
}


def ip2geo(ip):
    url = f'http://whois.pconline.com.cn/ipJson.jsp?json=true&ip={ip}'
    try:
        data = requests.get(url).json()
    except:
        data = {}
    return data
    

def get(url, **props):
    """发起get请求
    返回reso对象 属性值包括status_code text cookie
    network.get('http://baidu.com')
    network.get(http://httpbin.org/get?name=germey&age=22)     //200
    network.get('http://httpbin.org/get',params = {'name':'germey','age':22})    //299
    """    
    props = {'headers': HEADERS, **props}
    return requests.get(url=url, **props)
 

def post(url, data,**props):
    """发起post请求
    post('http://httpbin.org/post',data={'name':'germey','age':23})   //<Response [200]>
    """
    props = {'headers': HEADERS, **props}
    return requests.post(url=url, data=data,**props)



