import sys
sys.path.append('../src')
from znetwork import get
from znetwork.dom import DOM

rsp = get('http://www.19lou.com/forum-262-1.html')
html = rsp.text
print(html)
page_DOM = DOM(html)
for item in page_DOM.find_all('.list-data-item div.title a'):
    title = item.find('a>span').text 
    url = item.get('href')
    print(title,url)