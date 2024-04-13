import asyncio,aiohttp,aiofiles,re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
crx_type = "C:\selenium\CFHDOJBKJHNKLBPKDAIBDCCDDILIFDDB_3_25_1_0.crx"
mb=1024*1024
items = {}
index = 0
lists = []
async def download_vidoes(url:str,index:int):
    async with ClientSession.get(url) as response:
        async with aiofiles.open(f'F:\mentalist\S01E0{index}','wb') as file:
            items[f'S01E0{index}'] = [0,response.content_length]
            while True:
                data = await response.content.read(mb)
                if not data:
                    break
                items[f'S01E0{index}'][0]+=len(data)
                await file.write(data)
async def extract_final_links(url:str,driver:str):
    global index
    link_ensure = None
    index+=1
    current_temp = index
    try:
            chrome_options = webdriver.ChromeOptions()
            #chrome_options.add_argument("--headless")
            chrome_options.add_extension(crx_type)
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url)
            html = BeautifulSoup(driver.page_source)
            tag = html.find_all("div", {"class": "story downloadss"})
            download_link = tag[0].find_all("a", {"href": re.compile("https://ds2play.com/")})[0].get("href")
            driver.get(download_link)
            driver.find_element(By.XPATH, r"/html/body/div[5]/div/a").click()
            await asyncio.sleep(6)
            driver.find_element(By.XPATH, r"/html/body/div[5]/div/div/a").click()
            await asyncio.sleep(6)
            link_ensure = driver.find_element(By.XPATH, r"/html/body/div/div/div/a").get_attribute('href')
            lists.append((link_ensure,current_temp))
    except:
        pass
async def main(driver:str,*args):
    global ClientSession
    ClientSession = aiohttp.ClientSession()
    await asyncio.gather(*[extract_final_links(f'https://sisi.egybest.land/مسلسل-the-mentalist-الموسم-الاول-حلقة-{i}/',driver) for i in range(*args)])
    await asyncio.gather(*[download_vidoes(i[0],i[1]) for i in (lists)])
    print('Done downloading!')

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(main("C:\selenuim\chromedriver.exe",1,4))
