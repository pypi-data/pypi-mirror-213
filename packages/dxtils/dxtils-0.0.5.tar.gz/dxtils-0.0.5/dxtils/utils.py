import platform
import subprocess

import requests as rq
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import read_version_from_cmd, PATTERN, os_type


PLATFORM = platform.system()
BRAVE_EXECUTABLE = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
CHROMEDRIVERS_URL = "https://chromedriver.chromium.org/downloads"


class CustomChromeDriver(ChromeDriver):

    def get_url(self) -> str:
        return self._url


def get_sub_version(major_version: str) -> str:
    soup = BeautifulSoup(rq.get(CHROMEDRIVERS_URL).text, "html.parser")
    prefix = f"ChromeDriver {major_version}"
    text = soup.find(text=lambda t: t and t.startswith(prefix))
    return text.split()[1].strip()


def version_install(version: str) -> str:
    url = f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_mac_arm64.zip"
    manager = ChromeDriverManager()
    manager.driver = CustomChromeDriver(
        "chromedriver", version, os_type(), url, "")
    return manager.install()


def set_up_driver(
    undetected: bool = False, kwargs_only: bool = False
) -> Chrome | uc.Chrome | dict:
    options = ChromeOptions()
    if PLATFORM != "Windows":
        version = read_version_from_cmd(
            f'"{BRAVE_EXECUTABLE}" --version', PATTERN["brave-browser"])
        version = get_sub_version(version)
        driver_binary = version_install(version)
        options.binary_location = BRAVE_EXECUTABLE
        executable_path = BRAVE_EXECUTABLE
    else:
        driver_binary = ChromeDriverManager().install()
        executable_path = None        
    if not undetected:
        if kwargs_only:
            return {"service": Service(driver_binary), "options": options}
        return Chrome(service=Service(driver_binary), options=options)
    if PLATFORM != "Windows":
        subprocess.run(("codesign", "--remove-signature", driver_binary))
        subprocess.run(
            ("codesign", "--force", "--deep", "-s", "-", driver_binary))
    if kwargs_only:
        return {
            "driver_executable_path": driver_binary,
            "browser_executable_path": executable_path
        }
    return uc.Chrome(
        driver_executable_path=driver_binary,
        browser_executable_path=executable_path)
