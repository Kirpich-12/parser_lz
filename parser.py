from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
from multiprocessing import Pool, cpu_count


# TODO
# Дописать парсер одной страницы +
# Написать Сохраниение данных +/-
# Написать Логи
# Графики


url = 'https://rabota.by/search/vacancy?text=%D0%A1%D0%BF%D0%B5%D1%86%D0%B8%D0%B0%D0%BB%D0%B8%D1%81%D1%82+%D0%BF%D0%BE+%D0%BA%D0%B8%D0%B1%D0%B5%D0%B7%D0%BE%D0%BF%D0%B0%D1%81%D0%BD%D0%BE%D1%81%D1%82%D0%B8&salary=&ored_clusters=true&excluded_text=&area=1002&page=1&search'
url2 = 'https://rabota.by/search/vacancy?text=%D0%A1%D0%BF%D0%B5%D1%86%D0%B8%D0%B0%D0%BB%D0%B8%D1%81%D1%82+%D0%BF%D0%BE+%D0%BA%D0%B8%D0%B1%D0%B5%D0%B7%D0%BE%D0%BF%D0%B0%D1%81%D0%BD%D0%BE%D1%81%D1%82%D0%B8&salary=&ored_clusters=true&excluded_text=&area=1002&page=0&search'


def opt():
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 MyAwesomeBot/1.0"
    options.add_argument(f"--user-agent={my_user_agent}")
    return options


def get_driver():
    options = opt()
    driver = webdriver.Chrome(options=options)
    return driver


def get_page(url: str, driver: webdriver.Chrome) -> webdriver.Chrome:
    driver.get(url)
    return driver


def parser_list(url, time_wait: int, driver: webdriver.Chrome) -> list:
    """Парсит список ссылок на вакансии с одной страницы"""
    answer = []
    driver = get_page(url, driver)
    sleep(time_wait)
    list_divs = driver.find_elements(By.CLASS_NAME, 'vacancy-info--ieHKDTkezpEj0Gsx')
    sleep(time_wait)
    for div in list_divs:
        href = div.find_element(By.TAG_NAME, 'a').get_attribute('href')
        answer.append(href)
    return answer

def safe_text(selector, driver):
    el = driver.find_elements(By.CSS_SELECTOR, selector)
    return el[0].text if el else 'None'

def parser_vacancy(vacancy: str):
    driver = get_driver()
    driver.get(vacancy)
    sleep(1)

    try:
        name_raw = driver.find_element(By.CSS_SELECTOR, "[data-qa='vacancy-title']")
        names_raw_list = name_raw.find_elements(By.TAG_NAME, 'span')
        name = ' '.join([n.text for n in names_raw_list])
    except:
        name = 'None'

    selery = safe_text("[data-qa='vacancy-salary-compensation-type-net']", driver)
    selery_1 = safe_text("[data-qa='vacancy-salary-compensation-type-gross']", driver)
    compensation_frequency = safe_text("[data-qa='compensation-frequency-text']", driver)
    work_exp = safe_text("[data-qa='work-experience-text']", driver)
    employment = safe_text("[data-qa='common-employment-text']", driver)
    work_schedule = safe_text("[data-qa='work-schedule-by-days-text']", driver)
    working_hours = safe_text("[data-qa='working-hours-text']", driver)
    work_formats = safe_text("[data-qa='work-formats-text']", driver)


    if selery == 'None':
        selery = selery_1


    driver.quit()

    print(name)
    data = (name, selery, compensation_frequency, work_exp, employment, work_schedule, working_hours, work_formats, vacancy)
    print('============================================================')
    print(len(data))
    print('============================================================')
    return data


def save_to_csv(data: list, filename: str = 'vacancies.csv'):
    columns = [
        "Название вакансии",
        "Зарплата",
        "Частота выплат",
        "Опыт работы",
        "Тип занятости",
        "График работы",
        "Рабочие часы",
        "Формат работы",
        "Ссылка"
    ]
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(filename, index=False)
    print(f"\n сохранено в файл: {filename}")


def main():
    driver = get_driver()
    ll = parser_list(url2, 1, driver)
    #ll0 = parser_list(url, 1, driver)
    all_links = ll
    driver.quit()

    print(f" Найдено {len(all_links)} вакансий.")

    with Pool(processes=5) as pool:
        results = pool.map(parser_vacancy, all_links)

    print(f"\n {len(results)} вакансий.")
    save_to_csv(results, 'res.csv')


if __name__ == '__main__':
    main()
