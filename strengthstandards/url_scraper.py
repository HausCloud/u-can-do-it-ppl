from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from helper.utils import get_driver
import toml
import json


def main():
    """
    Function for scraping urls

    Args:
        None
    Returns:
        None
    Notes:
        None
    Todo:
        None
    """

    with open("../config.toml") as f:
        config = toml.load(f)

    # Setup options
    options = Options()
    options.headless = True
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    # This fixes errors w/ headless for some reason.
    options.add_argument("window-size=1920,1080")

    # Open browser
    driver = get_driver("Google Chrome", options=options)
    driver.get(url="https://strengthlevel.com/strength-standards")

    more_locator = (By.XPATH, "//button[text()='More Exercises...']")

    # Wait until button is in DOM
    btn_element = WebDriverWait(driver, 3).until(
        method=expected_conditions.presence_of_element_located(more_locator),
        message="Timed out trying to find btn on DOM.",
    )

    # Open the entire "grid"
    while btn_element and btn_element.get_attribute("disabled") == None:
        driver.execute_script("arguments[0].scrollIntoView();", btn_element)
        WebDriverWait(driver, 3).until(
            method=expected_conditions.visibility_of_element_located(more_locator),
            message="Timeout trying to click btn.",
        ).click()

    # Export data
    url_elements = driver.find_elements(
        by=By.XPATH, value="//a[contains(@href,'/strength-standards/')]"
    )
    with open(file=config["strengthstandards"]["urls_path"], mode="w") as f:
        json.dump(
            [url_element.get_attribute("href") for url_element in url_elements],
            f,
        )

    driver.quit()


if __name__ == "__main__":
    main()
