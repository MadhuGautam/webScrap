#################################################################################
#   Script for fetching products link from url https://www.skinstore.com/       #
#                                                                               #
#################################################################################

import bs4 as bs
import urllib.request
import mysql.connector

products=[]
pagination_products=[]

#################################################################################

url1 = 'https://www.skinstore.com/'
productName=""
product_url=""
siteName="skinstore"
total_products=0
productLinks=""

def unique(list1): 
  
  # intilize a null list 
  unique_list = [] 
    
  # traverse for all elements 
  for x in list1: 
      # check if exists in unique_list or not 
      if x not in unique_list: 
          unique_list.append(x) 

  return unique_list
###############################################################################################
#
# url fetch from MAIN WEBPAGE MENUS OR NAVBAR
#
#################################################################################
try:
    source_url = urllib.request.urlopen(url1)
    source = source_url.read()
    
    soup = bs.BeautifulSoup(source,'html.parser')
    
    for tag in soup.findAll('a',attrs={'class':'responsiveFlyoutMenu_levelThreeLink'}):   
        productName = tag.text 
        productLinks = "https://www.skinstore.com"+tag.get('href')
        #print(productName+":"+productLinks)  
        products.append(productLinks)
    
except:
    print("Something went wrong in getting nav url") 
finally:
    source_url.close()
 
products=unique(products)
count=0
print("Total_product_nav_url: "+str(len(products))) 
###############################################################################################
#
# GET pagination url from EACH WEBPAGE
#
###############################################################################################

for pagination in products:
    pagination_last_number=0
    try:
    
        count=count + 1
        print(count)
        print(pagination)
        source_url = urllib.request.urlopen(pagination)
        source = source_url.read()

        soup = bs.BeautifulSoup(source,'html.parser')
        for url in soup.find('h1', attrs={'class':'responsiveProductListHeader_title'}):
            print(url)
            
        #########################################################################################
        # 
        # GET PAGINATION LAST NUMBER AND ADD URL IN ARRAY WITH FOR LOOP
        #       
        ########################################################################################## 
        if(soup.findAll('a', href=True, attrs={'class':'responsivePaginationButton--last'})):        
            for inner_url in soup.findAll('a', href=True, attrs={'class':'responsivePaginationButton--last'}):
                pagination_last_number = inner_url.text
                pagination_last_number = int(pagination_last_number.replace("\n",""))
        print("pagination_last_number"+str(pagination_last_number))
        if(pagination_last_number > 0):    
            for pg in range(pagination_last_number):
                newUrl = pagination+"?pageNumber="+str(pg+1)
                pagination_products.append(newUrl)
  
    except:
        print("Something went wrong in getting pagination url") 
    finally:
        source_url.close()
        
###########################################################################################
# 
# CREATE ONE ARRAY FOR ALL PRODUCTS LINK
#       
########################################################################################## 
pagination_products=unique(pagination_products)   
products.extend(pagination_products)
products=unique(products) 
print("Total_product_url: "+str(len(products))) 
  
###################################################################################################
# 
# INSERT ALL THE EACH PRODUCT LINK IN DB
#       
####################################################################################################
     
for x in products:
    thisdict =	{}
    try:
        print(x)
        mydb = mysql.connector.connect(host="localhost", user="root", password="", database="skinstore_webscrap")
        mycursor = mydb.cursor()
        source_url = urllib.request.urlopen(x)
        source = source_url.read()

        soup = bs.BeautifulSoup(source,'html.parser') 

        for tag in soup.find_all('a', href=True, attrs={'class':'productBlock_link'}):
            for inner_tag in tag.find_all('div', attrs={'class':'productBlock_title'}):
                for heading_tag in inner_tag.find_all('h3', attrs={'class':'productBlock_productName'}):
                    productLinks = "https://www.skinstore.com"+tag.get('href')
                    productName = heading_tag.text
                    productName =  productName.replace("\n","")
                    #print(productName+":"+productLinks)
                    thisdict[productName] = productLinks
                    
                    
                    
            
        for x, y in thisdict.items():
            print(x, y)
            sql = "INSERT INTO productLinks (productName, url, siteName) VALUES (%s, %s, %s)"
            val = (x,y,siteName)
            mycursor.execute(sql, val)
            mydb.commit()
            total_products=total_products + 1
        print(total_products)

    except:
        print("Something went wrong in getting product url") 
    finally:
        mydb.close()
    source_url.close()

