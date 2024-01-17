import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import numpy as np
from tqdm import tqdm

names = []
cities = []
companies = []
salaries = []
vacancy_info = []
publications_time = []
descriptions = []
urls = []


def parsing(vacancy_name: str) -> pd.DataFrame:

    """
    Take the name of the profession about which
    collect vacancies from hh.ru
    """

    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_experimental_option(
            "prefs", {
                # block image loading
                "profile.managed_default_content_settings.images": 2,
            })
    # open chrome
    driver = webdriver.Chrome(options=options)

    vacancy_name = '+'.join(vacancy_name.split())

    # go to prime page with vacancies for last day
    url = f'https://hh.ru/search/vacancy?ored_clusters=true&text={vacancy_name}&search_period=1'

    driver.get(url)
    driver.maximize_window()

    # take vacancies
    vacancies = driver.find_elements(By.CLASS_NAME, 'serp-item__title')
    time.sleep(2)

    # save the original tab id
    prime_tab = driver.current_window_handle

    for vacancy in tqdm(vacancies):

        # open new tab with vacancy
        try:
            vacancy.click()
        except:
            driver.execute_script("arguments[0].click();", vacancy)

        # go to new tab
        for window_handle in driver.window_handles:
            if window_handle != prime_tab:
                driver.switch_to.window(window_handle)
                break

        # extract and save info
        description = driver.find_elements(By.CLASS_NAME, 'g-user-content')
        if not description:
            description = driver.find_elements(By.CLASS_NAME, 'vacancy-branded-user-content')

        description = ' '.join([x.text for x in description])
        descriptions.append(description)

        # vacancy name
        name = driver.find_elements(By.CLASS_NAME,
                                    'vacancy-title')
        name = ' '.join([x.text for x in name])
        names.append(name)
        driver.implicitly_wait(2)

        # try to take salary
        try:
            salary = driver.find_element(By.XPATH,
                                     '''//*[@id="HH-React-Root"]/div/div[4]/div[1]
                                     /div/div/div/div/div/div[1]/div[1]/div/div[1]/div[2]/span''')\
                            .text
            driver.implicitly_wait(1)
        except:
            salary = np.nan

        salaries.append(salary)

        # try to take vacancy_info
        try:
            info = driver.find_elements(By.CLASS_NAME,
                                    'vacancy-description-list-item')
            info = [x.text for x in info]

            driver.implicitly_wait(1)
        except:
            info = np.nan

        vacancy_info.append(info)


        # company
        company = driver.find_element(By.CLASS_NAME,
                                  'vacancy-company-name')\
                        .text
        companies.append(company)


        # city
        city = driver.find_elements(By.CLASS_NAME,
                               '''vacancy-view-location''')
        city = [x.text for x in city]
        cities.append(city)

        # publication time
        time_pub = driver.find_element(By.CLASS_NAME,
                                   'vacancy-creation-time-redesigned')\
                         .text
        publications_time.append(time_pub)

        # url
        link = driver.current_url
        urls.append(link)

        # Close the tab or window
        driver.close()

        # Switch back to the old tab or window
        driver.switch_to.window(prime_tab)

    # привинтить конкретную дату к имени файла

    time.sleep(6)
    driver.close()
    driver.quit()


    df = pd.DataFrame({'name': names, 'company': companies,
                       'city': cities, 'salary': salaries,
                       'vacancy_info': vacancy_info,
                       'publication_time': publications_time,
                       'description': descriptions,
                       'link': urls
                      })

    return df