from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
from multiprocessing import Pool
from loggi import log
import re


# TODO
# Дописать парсер одной страницы +
# Написать Сохраниение данных +/-
# Написать Логи
# Графики

logger = log()


def url(num:int):
    url = f'https://rabota.by/vacancies/specialist_po_informacionnoy_bezopasnosti?page={num}&search&hhtmFrom=vacancy_search_list'
    logger.info(f'Open page: {url}')
    return url


def opt():
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    logger.debug('headless mode')
    my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 MyAwesomeBot/1.0"
    options.add_argument(f"--user-agent={my_user_agent}")
    return options


def get_driver():
    options = opt()
    driver = webdriver.Chrome(options=options)
    logger.info('driver was started')
    return driver


def get_page(url: str, driver: webdriver.Chrome) -> webdriver.Chrome:
    driver.get(url)
    logger.info(f'Get page: {url}')
    return driver

def format_selery(s: str) -> int | float:
    flag = False
    if '₽' in s:
        flag = True
    numbers = re.findall(r'\d[\d\s]*', s)
    nums = [int(n.replace(' ', '')) for n in numbers]
    
    if not nums:
        return None
    elif len(nums) == 1:
        ans = nums[0]
    else:
        ans =  sum(nums) / len(nums)
    
    if flag:
        ans = ans * 0.043
        logger.error('rr was founded')
    
    return ans

def analyze_csv(filename: str = "res.csv"):
    df = pd.read_csv(filename)
    df = df[df["Зарплата"] != "None"]

    df["Зарплата"] = pd.to_numeric(df["Зарплата"], errors="coerce")

    avg_salary = df["Зарплата"].mean()

    exp = df["Опыт работы"].dropna()
    exp = exp[exp != "None"]

    exp_counts = exp.value_counts()

    logger.info(f"Средняя зарплата: {avg_salary:.2f} Br")
    logger.info("Распределение по опыту работы:")
    for k, v in exp_counts.items():
        logger.info(f"  {k}: {v}")

    return avg_salary, exp_counts

def parser_list(url:str, time_wait: int, driver: webdriver.Chrome) -> list:
    answer = []
    driver = get_page(url, driver)
    sleep(time_wait)
    list_divs = driver.find_elements(By.CLASS_NAME, 'vacancy-info--ieHKDTkezpEj0Gsx')
    sleep(time_wait)
    for div in list_divs:
        href = div.find_element(By.TAG_NAME, 'a').get_attribute('href')
        answer.append(href)
    logger.info('return answer')
    return answer

def safe_text(path:str, driver:webdriver.Chrome):
    el = driver.find_elements(By.CSS_SELECTOR, path)
    return el[0].text if el else 'None'

def parser_vacancy(vacancy: str):
    driver = get_driver()
    driver.get(vacancy)
    sleep(2)
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
    
    selery = format_selery(selery)
    
    logger.info(f'page with name: {name} do, ')
    logger.debug(f'scr: {vacancy}')
    driver.quit()
    logger.info('driver out')
    data = (name, selery, compensation_frequency, work_exp, employment, work_schedule, working_hours, work_formats, vacancy)
    return data


def save_to_csv(data: list, filename: str = 'res.csv'):
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
    logger.info(f"\n сохранено в файл: {filename}")


def main():
    driver = get_driver()
    num_pages = 1
    all_links = []
    for i in range(num_pages):
        all_links += parser_list(url(i), 1, driver)
    driver.quit()

    logger.info(f" Найдено {len(all_links)} вакансий.")

    with Pool(processes=5) as pool:
        results = pool.map(parser_vacancy, all_links)

    logger.info(f"\n {len(results)} вакансий.")
    save_to_csv(results)
    analyze_csv()


if __name__ == '__main__':
    main()
