import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv

count = 0
count_lock = threading.Lock() 

def process_url(url):
    global count
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    
    page = 1
    
    while True:
        products = driver.find_elements(By.XPATH, '/html/body/main/div[1]/div[1]/div[2]/div/div[1]/form[2]/ul/li')
        
        if not products:
            break
        
        for product in products:
            try:
                product_name = product.find_element(By.XPATH, './div/div[2]/div[1]/a').text
                product_link = product.find_element(By.XPATH, './div/div[2]/div[1]/a').get_attribute('href')
                with count_lock:
                    count += 1
            except:
                product_name = 'N/A'
                product_link = 'N/A'

            try:
                product_price = product.find_element(By.XPATH, './div/div[2]/div[2]/p').text
            except:
                try:
                    product_price = f"{product.find_element(By.XPATH, './div/div[2]/div[2]/div/span[1]').text} → {product.find_element(By.XPATH, './div/div[2]/div[2]/div/span[2]').text}"
                except:
                    product_price = 'N/A'

            print(f"Product Name: {product_name}")
            print(f"Product Price: {product_price}")
            print(f"Product Link: {product_link}")
            print(f"Total Products: {count}")
            print()

            csv_writer.writerow([product_name, product_price, product_link])

        page += 1
        driver.get(driver.current_url + f'&page={page}')

    driver.quit()

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

csv_file = open('ansgear_products.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Product Name', 'Price', 'Product Link'])

urls = ["guns","packages","tanks-tank-acc","loaders","masks","barrels","parts","pads","pod-packs-pods","bags-backpacks","clothing-apparel","paintballs","laser-engraving"]

threads = []
for a in urls:
    url = f'https://ansgear.com/{a}?page=1'
    thread = threading.Thread(target=process_url, args=(url,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

csv_file.close()
