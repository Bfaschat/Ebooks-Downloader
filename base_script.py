import time
import threading
import bs4
import lxml
import shutil
import os

from urllib import request as urlrequest


url = 'http://www.allitebooks.com/'
proxy_host = '178.22.117.153:53281'

directory = os.path.dirname(__file__)

if not os.path.exists('Books'):
	os.makedirs('Books')

if not os.path.exists('Book Packets'):
	os.makedirs('Book Packets')

book_path    = os.path.join(directory,'Books')
packet_path  = os.path.join(directory,'Book Packets')


def get_page_number():



	request = urlrequest.Request(url,data=None,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
	request.set_proxy(proxy_host,'http')

	response = urlrequest.urlopen(request)
	soup = bs4.BeautifulSoup(response,'lxml')

	page_number=soup.find('span' ,class_ = 'pages')
	return page_number.text.split()[2]




def get_book_links(page_number):
	packet_number = 1
	packet_file = os.path.join(packet_path,'Packet 1.txt')
	out_file = open(packet_file,'w+')
	
	for x in range(1,page_number+1):


			page_number = str(x)

			request = urlrequest.Request(url+'/page/'+page_number+'/',data=None,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
			request.set_proxy(proxy_host,'http')

			response = urlrequest.urlopen(request)
			soup  = bs4.BeautifulSoup(response,'lxml')

			for element in soup.find_all('article'):
				link = element.find('h2').find('a')
				out_file.write((link['href'])+'\n')
				print(link['href'])

			
			try:
				request.close()
			except:
				pass

			if(x%50 == 0):
				out_file.close()
				packet_number +=1
				packet_file = os.path.join(packet_path,'Packet ' + str(packet_number) +'.txt')
				out_file = open(packet_file,'w')



def copy_books(f,x):
	for line in f:
		original_line = line;
		line = line.strip('\n')
		url = line

		request = urlrequest.Request(url,data=None, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
		request.set_proxy(proxy_host, 'http')


		response = urlrequest.urlopen(request)
		soup  = bs4.BeautifulSoup(response,'lxml')
		book_link = soup.find('span',class_= 'download-links')
			
		if book_link is not None:
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
				print('Hit in thread ',x)
			except:
				g = open('missing_books.txt', 'a+')
				g.write(book_name + '\n' + book_link + '\n')
				g.close()
				print('Escaped')
				print(book_name)

		else:
			book_name = soup.find('h1',class_='entry-title')
			book_name = book_name.contents[0]
			
			book_name = book_name.lstrip()
			book_name = book_name.rstrip()

			g = open('missing_books.txt', 'a+')
			g.write(book_name +'\n' + original_line+'\n')
			g.close()
			print('Escaped')
			print(book_name)

	f.close()



def download_books():
	threads =[]

	length = len(os.listdir(packet_path))

	for x in range(1,length+1):
		 pack = os.path.join(packet_path,'Packet ' + str(x) + '.txt')
		 file = open(pack,'r')

		 thread = threading.Thread(target=copy_books,args=(file,x))
		 thread.start()
		 threads.append(thread)


	for thread in threads :
		 thread.join()
	threads =[]

	for x in range(1,length+1):

		 pack = os.path.join(packet_path,'Packet ' + str(x) + '.txt')
		 file = open(pack,'r')

		 thread = threading.Thread(target=download_books,args=(file,))
		 thread.start()
		 threads.append(thread)


	for thread in threads :
		 thread.join()

<<<<<<< HEAD
#page_number = int(get_page_number())
=======

page_number = int(get_page_number())
>>>>>>> 194463ef2cfd00052f6c6f152920e00c4eb222d9

get_book_links(page_number)

download_books()
