import pytest
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.service import Service as FFService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options

@pytest.fixture(scope="session")
def driver():
    opts = Options()
    opts.add_argument("--headless")
    service = FFService(GeckoDriverManager().install())
    drv = Firefox(service=service, options=opts)
    drv.implicitly_wait(5)
    yield drv
    drv.quit()
