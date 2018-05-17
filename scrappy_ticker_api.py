import urllib
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time

quote_page ='http://www.bloomberg.com/quote/SPX:IND'        # decleared url
page = urllib.request.urlopen(quote_page)
soup = BeautifulSoup(page, 'html.parser')                   # parse html using BeautifulSoup, store in soup.

name_box = soup.find('h1', attrs={'class':'name'})          # class name is unique, can query <div class='name'>
                                                            # remove <div> of the name and get its value
name = name_box.text.strip()                                # strip() used to remove starting and trailing, i.e. spaces.
                                                            #
print(name)

price_box = soup.find('div', attrs={'class':'price'})
price = price_box.text

print(price)

x = 0
while x < 20:
    with open('index.csv', 'a') as csv_file:                    # where 'a' appends to the end of the file.
        writer = csv.writer(csv_file)
        writer.writerow([name, price, datetime.now()])
    time.sleep(5)
    x += 1