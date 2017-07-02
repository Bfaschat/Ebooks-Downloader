import time
import threading
import bs4
import lxml
import shutil
import os

from urllib import request as urlrequest

g = open('missing_books.txt','a+')


proxy_host = '212.237.50.24:3128'

directory = os.path.dirname(__file__)

book_path   = os.path.join(directory,'Books')
packet_path = os.path.join(directory,'Packet Path')


def get_book_links(f):

     url = 'http://www.allitebooks.com/page/'

     for x in range(1,718 ):
          page_number = str(x)

          request = urlrequest.Request(url+page_number+'/',data=None,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
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

        with urlrequest.urlopen(book_link)  as response, open(complete_name,'wb') as out_file:
            shutil.copyfileobj(response,out_file)
            print(book_name)

    f.close()


threads =[]

for x in range(1,3):

     pack = os.path.join(packet_path,'pack' + str(x) + '.txt')
     file = open(pack,'r')

     thread = threading.Thread(target=download_books,args=(file,))
     thread.start()
     threads.append(thread)


for thread in threads :
     thread.join()
