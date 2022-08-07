import re
from selenium.webdriver.chrome.options import Options


def table_namer(string: str) -> str:
    """
    Function for parsing soon-to-be SQL table names.

    Args:
        string (str): Some string to be converted into a table name.
    Returns:
        str: new table name
    Notes:
    Todo:
    """
    # Replace any hyphens
    new_table_name = string.replace("-", "_")
    # Grab [a-zA-Z0-9_]
    new_table_name = re.sub("\W+", "", new_table_name)
    # Convert to lowercase
    new_table_name = new_table_name.lower()
    # Remove leading/trailing whitespace
    new_table_name = new_table_name.strip()

    return new_table_name


def get_driver(driver_name: str = "", options: Options = None):
    if driver_name == "Google Chrome":
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service as ChromeService
        from webdriver_manager.chrome import ChromeDriverManager

        return webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=options
        )
    elif driver_name == "Chromium":
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service as ChromiumService
        from webdriver_manager.chrome import ChromeDriverManager
        from webdriver_manager.core.utils import ChromeType

        return webdriver.Chrome(
            service=ChromiumService(
                ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
            ),
            options=options,
        )
    elif driver_name == "Brave":
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service as BraveService
        from webdriver_manager.chrome import ChromeDriverManager
        from webdriver_manager.core.utils import ChromeType

        return webdriver.Chrome(
            service=BraveService(
                ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()
            ),
            options=options,
        )
    elif driver_name == "Firefox":
        from selenium import webdriver
        from selenium.webdriver.firefox.service import Service as FirefoxService
        from webdriver_manager.firefox import GeckoDriverManager

        return webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()), options=options
        )
    elif driver_name == "Internet Explorer":
        from selenium import webdriver
        from selenium.webdriver.ie.service import Service as IEService
        from webdriver_manager.microsoft import IEDriverManager

        return webdriver.Ie(service=IEService(IEDriverManager().install()))
    elif driver_name == "Edge":
        from selenium import webdriver
        from selenium.webdriver.edge.service import Service as EdgeService
        from webdriver_manager.microsoft import EdgeChromiumDriverManager

        return webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()), options=options
        )
    elif driver_name == "Opera":
        from selenium import webdriver
        from webdriver_manager.opera import OperaDriverManager

        return webdriver.Opera(
            executable_path=OperaDriverManager().install(), options=options
        )
    else:
        return None
