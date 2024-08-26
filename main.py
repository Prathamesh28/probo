import requests
# import pandas as pd
# from bs4 import BeautifulSoup
# from selenium import webdriver

# driver = webdriver.Chrome()

# driver.get("https://www.indiavotes.com/lok-sabha/2019/haryana/17/31")

# page_source = driver.page_source

# soup = BeautifulSoup(page_source, "html.parser")

# data_element = soup.find_all("table")
# data = data_element.text

# driver.quit()

# # url = "https://www.indiavotes.com/lok-sabha/2019/haryana/17/31?cache=yes"
# # data = requests.get(url).text
# print(data)
# # soup = BeautifulSoup(data, 'html.parser')

# # print('Classes of each table:')
# # for table in soup.find_all('div'):
# #     print(table.get('class'))

requests.get("https://min-api.cryptocompare.com/data/histo/minute/daily?apiKey=e471405e501d405ced14457f2554c1e080328f4c1796a63a5ae56eba42a0b46a&fsym=BTC&tsym=USDT&e=cccagg&date=2024-07-11")