from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from pprint import pprint

# Определяем список ключевых слов:
keywords = ['дизайн', 'фото', 'web', 'python']


def wait_element(browser, delay=3, by=By.TAG_NAME, value=None):
    return WebDriverWait(browser, delay).until(
        expected_conditions.presence_of_element_located((by, value))
    )


chrome_path = ChromeDriverManager().install()
broser_service = Service(executable_path=chrome_path)
browser = Chrome(service=broser_service)

browser.get('https://habr.com/ru/articles/')
new_list = browser.find_elements(by=By.CLASS_NAME, value='tm-articles-list__item')

parsed_data = []
ll = []

for cont in new_list:
    link = wait_element(browser=cont, by=By.CLASS_NAME, value='tm-article-snippet__readmore').get_attribute('href')
    ll.append(link)

for links in ll:
    browser.get(links)
    time = wait_element(browser=browser, by=By.TAG_NAME, value='time').get_attribute('datetime')
    title = wait_element(browser=browser, by=By.CLASS_NAME, value='tm-title').text
    content = wait_element(browser=browser, by=By.CLASS_NAME, value='tm-article-presenter__content').text

    for keyword in keywords:
        if keyword in title or keyword in content:
            parsed_data.append({
                'date': time,
                'title': title,
                'link': links,
            })
            break
pprint(parsed_data)