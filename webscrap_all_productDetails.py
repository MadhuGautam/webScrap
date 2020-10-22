import bs4 as bs
import urllib.request
import mysql.connector
import time

links=[]
###############################################################################################
#
# url fetch from databse table productlinks
#
###############################################################################################

mydb1 = mysql.connector.connect(host="localhost", user="root", password="", database="skinstore_webscrap")
mycursor_fetch = mydb1.cursor()

mycursor_fetch.execute("SELECT distinct(url) FROM `productlinks` WHERE url not in(SELECT product_url FROM `productdetails`)")

myresult = mycursor_fetch.fetchall() #fetchall()fetchone

for x in myresult:
    #print(x[0])
    links.append(x[0])

mydb1.close() 
 
##########################################################################################

url1 = 'https://www.skinstore.com/skinceuticals-gentle-cleanser-6.76-oz/11535230.html'
                                                                            
brand_name=""
product_name=""
ingredients=""
siteName="skinstore"
total_links = len(links)
print("Total Links in db"+str(total_links))

############################################################################################
#
# fetch product details from given product links
#
###############################################################################################
for x in links:
    try:
        print(x)
        mydb = mysql.connector.connect(host="localhost", user="root", password="", database="skinstore_webscrap")
        mycursor = mydb.cursor()
        source_url = urllib.request.urlopen(x)
        source = source_url.read()
        
        soup = bs.BeautifulSoup(source,'html.parser')

        for tag in soup.findAll('div', attrs={'data-information-component':'brand'}):   
            brand_name = tag.text   
        for tag in soup.findAll('div',attrs={'class':'productName'}):   
            product_name = tag.text   
        for tag in soup.findAll('div',attrs={'data-information-component':'ingredients'}):   
            for inner_tag in tag.findAll('p'): 
                ingredients = inner_tag.text   

        #print(brand_name+"\n"+product_name+"\n"+ingredients)
        sql = "INSERT INTO productDetails (brandName, productName, image_url, product_url, ingredients, siteName) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (brand_name,product_name,"", x,ingredients,siteName)
        mycursor.execute(sql, val)
        mydb.commit()
        total_links = total_links-1
        print(total_links)

    except:
        print("Something went wrong") 
    finally:
        source_url.close()
        mydb.close()

   
