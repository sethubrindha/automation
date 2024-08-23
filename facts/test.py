
# ******** Undetected chrome***********#
# from undetected_chromedriver import Chrome, ChromeOptions
# print("inside chrome >>>>>>>")

# options = ChromeOptions()
# # options.add_argument("--headless")
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
# options.add_argument("--blink-settings=imagesEnabled=false")


# with Chrome(options=options) as driver:
#     driver.get("https://whatismyipaddress.com/")
#     # Perform your automated actions here

# ******** generate useragent***********#
# from user_agent import generate_user_agent, generate_navigator
# from pprint import pprint

# pprint(generate_navigator())



#***********change ip***********#
# import requests
# from bs4 import BeautifulSoup
# import random

# def get_hide_my_ass_proxies():
#     # URL of the HideMyAss free proxy list
#     url = 'https://www.hidemyass.com/proxy-list'

#     # Fetch the HTML content of the page
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     print("soup >>>>>>>",soup)

#     # Extract the proxy addresses
#     proxies = [row.select_one('.hx').text for row in soup.select('.hm-table tbody tr')]
    
#     return proxies

# def get_ssl_proxy_list():
#     # URL of the SSL Proxy list
#     url = 'https://www.sslproxies.org/'

#     # Fetch the HTML content of the page
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')

#     proxies = str(soup).split('Free proxies from free-proxy-list.net')[1].split('</textarea>')[0].replace('Updated at 2023-12-22 08:22:02 UTC.','').split('\n')
#     proxies.pop(); proxies.pop(0); proxies.pop(1); proxies.pop(2); proxies.pop(3)

#     # Extract the proxy addresses and ports
#     # proxies = [f"{row.select_one('td:nth-child(1)').text}:{row.select_one('td:nth-child(2)').text}" for row in soup.select('#proxylisttable tbody tr')]
    
#     return proxies

# if __name__ == "__main__":
#     # Get a list of HideMyAss proxies
#     proxy_list = get_hide_my_ass_proxies()
#     print("proxy_list >>>>>>>>",proxy_list)
#     if not proxy_list:
#         proxy_list = get_ssl_proxy_list()

#     # Choose a random proxy from the list
#     selected_proxy = random.choice(proxy_list)
#     print("selected_proxy >>>>>>>>",selected_proxy)


import google.auth
from googleapiclient.discovery import build

# Load credentials from the JSON file you downloaded
credentials, project = google.auth.default()

# Create a Gmail API service
service = build('gmail', 'v1', credentials=credentials)

# Define the account information
account_info = {
    'emailAddress': 'newuser@example.com',
    'password': 'securepassword123'
}

# Use the Gmail API to create the account
created_account = service.users().create(body=account_info).execute()

print(f'Account created: {created_account}')
