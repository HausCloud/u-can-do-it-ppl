from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, WebDriverException
from helper.utils import table_namer
from helper.enums import HumanProperty
from multiprocessing import cpu_count, Pool
from math import ceil
from pprint import pprint
import toml
import json


def pull_table_data(args):
    url, config = args[0], args[1]
    timer = 3

    options = Options()
    options.headless = True
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("window-size=1920,1080")

    service = Service(executable_path=config["strengthstandards"]["chrome_driver_path"])
    driver = webdriver.Chrome(service=service, options=options)

    weight_locator = (By.XPATH, f"//a[text()='{HumanProperty.W.value}']")
    age_locator = (By.XPATH, f"//a[text()='{HumanProperty.A.value}']")

    driver.get(url=url)
    try:
        btn_element = WebDriverWait(driver, timer).until(
            method=expected_conditions.presence_of_element_located(weight_locator),
            message="Timed out trying to find btn on DOM.",
        )
        driver.execute_script("arguments[0].scrollIntoView();", btn_element)
        WebDriverWait(driver, timer).until(
            method=expected_conditions.visibility_of_element_located(weight_locator),
            message="Timeout trying to click btn.",
        ).click()
    except TimeoutException:
        return ([], [], None)
    """
    Gonna rely that their naming convention for the button is consistent w/ first table header
    Pull lifts by weight
    """
    tbl_element = driver.find_element(
        by=By.XPATH,
        value=f"//table[./thead/tr/th/abbr[@title='{HumanProperty.W.value.split(' ')[1]}']]",
    )
    rows = tbl_element.find_elements(by=By.XPATH, value=".//tbody/tr")

    lift_attr = "one_rep_max"

    weight_data = []
    try:
        for row in rows:
            row_data = []
            for tag in row.find_elements(by=By.XPATH, value="./td"):
                if not tag.text.isdigit():
                    lift_attr = "many_rep_max"
                    row_data.append(1)
                    # row_data.append(tag.text)
                else:
                    row_data.append(int(tag.text))
            if row_data:
                weight_data.append(row_data)
    except WebDriverException as e:
        return ([], [], None)

    try:
        WebDriverWait(driver, timer).until(
            method=expected_conditions.presence_of_element_located(age_locator),
            message="Timed out trying to find btn on DOM.",
        ).click()
    except TimeoutException:
        return ([], [], None)

    tbl_element = driver.find_element(
        by=By.XPATH,
        value=f"//table[./thead/tr/th/abbr[@title='{HumanProperty.A.value.split(' ')[1]}']]",
    )
    rows = tbl_element.find_elements(by=By.XPATH, value=".//tbody/tr")
    age_data = []

    try:
        for row in rows:
            row_data = []
            for tag in row.find_elements(by=By.XPATH, value="./td"):
                if not tag.text.isdigit():
                    lift_attr = "many_rep_max"
                    row_data.append(1)
                    # row_data.append(tag.text)
                else:
                    row_data.append(int(tag.text))
            if row_data:
                age_data.append(row_data)
    except WebDriverException as e:
        return ([], [], None)

    driver.quit()

    # Add into final table
    return (weight_data, age_data, lift_attr)


def main():
    with open("../config.toml") as f:
        config = toml.load(f)

    with open(file=config["strengthstandards"]["urls_path"]) as f:
        urls = json.load(f)

    pool_count = cpu_count()
    pool_count = ceil(pool_count / 4) if pool_count > 10 else ceil(pool_count / 2)

    with Pool(pool_count) as p:
        try:
            all_data = p.map(pull_table_data, [[url, config] for url in urls])
        except Exception as e:
            exit(-1)

        all_table_data = {
            table_namer(url.rsplit("/", 1)[-1]): {
                "weight": data[0],
                "age": data[1],
                "lift_attr": data[2],
            }
            for url, data in zip(urls, all_data)
            if url.rsplit("/", 1)[-1] not in ("lb", "kg")
        }

    with open(file=config["strengthstandards"]["table_data_path"], mode="w") as f:
        json.dump(obj=all_table_data, fp=f)


if __name__ == "__main__":
    main()
