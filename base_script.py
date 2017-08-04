import time
import threading
import bs4
import lxml
import shutil
import os

from urllib import request as urlrequest



url = 'http://www.allitebooks.com/'
proxy_host = '94.177.180.226:80'

directory = os.path.dirname(__file__)

if not os.path.exists('Books'):
	os.makedirs('Books')

book_path    = os.path.join(directory,'Books')
packet_path  = os.path.join(directory,'Packet Path')
book_links = open('book_links.txt','a+')



def get_page_number():



    request = urlrequest.Request(url,data=None,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
    request.set_proxy(proxy_host,'http')

    response = urlrequest.urlopen(request)
    soup = bs4.BeautifulSoup(response,'lxml')

    page_number=soup.find('span' ,class_ = 'pages')
    return page_number.text.split()[2]

def get_book_links(f,page_number):



    for x in range(1,2+1):
        page_number = str(x)

        request = urlrequest.Request(url+'/page/'+page_number+'/',data=None,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
        request.set_proxy(proxy_host,'http')

        response = urlrequest.urlopen(request)
        soup  = bs4.BeautifulSoup(response,'lxml')

        for element in soup.find_all('article'):
            link = element.find('h2').find('a')
            f.write((link['href'])+'\n')
            print('caught')
        try:
            request.close()
        except:
            print("End soup")


def download_books(f):
    print('hit')
    for line in f:
        line = line.strip('\n')
        url = line

        request = urlrequest.Request(url,data=None, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
        request.set_proxy(proxy_host, 'http')


        response = urlrequest.urlopen(request)
        soup  = bs4.BeautifulSoup(response,'lxml')

        book_link = soup.find('span',class_= 'download-links')
        book_link = book_link.find('a')['href']

        book_name = book_link.split('/')[-1]


        request = urlrequest.Request(book_link, data=None, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
        request.set_proxy(proxy_host, 'http')

        complete_name = os.path.join(book_path,book_name)

        book_link = book_link.replace(' ','%20')



        try:
            response = urlrequest.urlopen(book_link)
            out_file = open(complete_name, 'wb')
            shutil.copyfileobj(response,out_file)
            print('hit')
        except:
            g = open('missing_books.txt', 'a+')
            g.write(book_name + '\n' + book_link + '\n')
            g.close()
            print('escaped')
            print(book_name)



    f.close()


page_number = int(get_page_number())
get_book_links(book_links,page_number)
book_links.close()
book_links = open('book_links.txt','r')
download_books(book_links)

'''
threads =[]

for x in range(1,63):

     pack = os.path.join(packet_path,'pack' + str(x) + '.txt')
     file = open(pack,'r')

     thread = threading.Thread(target=download_books,args=(file,))
     thread.start()
     threads.append(thread)


for thread in threads :
     thread.join()
'''

'''
threads =[]

for x in range(1,63):

     pack = os.path.join(packet_path,'pack' + str(x) + '.txt')
     file = open(pack,'r')

     thread = threading.Thread(target=download_books,args=(file,))
     thread.start()
     threads.append(thread)


for thread in threads :
     thread.join()
'''
