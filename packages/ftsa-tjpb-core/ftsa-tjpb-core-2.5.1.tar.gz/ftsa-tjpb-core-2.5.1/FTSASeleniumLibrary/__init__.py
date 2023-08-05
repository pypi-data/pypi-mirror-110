from SeleniumLibrary import SeleniumLibrary
from SeleniumLibrary.keywords import BrowserManagementKeywords, ScreenshotKeywords, WaitingKeywords, \
                                     FormElementKeywords, ElementKeywords, JavaScriptKeywords
from robot.api import logger
from robot.api.deco import library, keyword

from shutil import which
import docker
import os
import socket
import time
import shutil
from datetime import datetime

from ftsa.core.properties import VERSION, REMOTE_VERSION, SLEEP_SECONDS, REC_VIDEO_VERSION
from ftsa.core.utils import extract_name_from, extract_type_from, sanitize_camel_case


@library(scope='GLOBAL', version=VERSION)
class FTSASeleniumLibrary(SeleniumLibrary):

    def __init__(self):
        SeleniumLibrary.__init__(self)

    @keyword
    def abrir_o_navegador(self, url, browser, maximized=True, speed="0.3s", timeout="20s", implicit_wait="10s"):
        self.open_browser(self, url, browser, maximized=maximized, speed=speed, timeout=timeout,
                          implicit_wait=implicit_wait)

    @keyword
    def open_browser(self, url, browser="chrome", remote_url=None, maximized=True, speed="0.3s", timeout="20s",
                     implicit_wait="10s", download_path=f"output{os.sep}downloads"):
        """*FTSA opens a new browser instance*

        Open the ``browser`` with initial tests ``url``.

        Default options used:
        | browser       | chrome |
        | remote_url    | None   |
        | maximized     | True   |
        | speed         | 0.3s   |
        | timeout       | 20s    |
        | implicit_wait | 10s    |
        | download_path | output/downloads (Chrome, only) |

        _Returns_ the *page title*

        """
        # Configuring DOWNLOAD_PATH
        download_path = os.path.join(os.getcwd(), download_path)
        if not os.path.isdir(download_path):
            os.mkdir(download_path)
            logger.info(f'Download directory created: "{download_path}"')
        else:
            logger.info(f'Directory already exists: "{download_path}"')
        # Configuring BROWSER OPTIONS
        config_options = None
        browser_management = BrowserManagementKeywords(self)
        if browser.lower() == 'firefox':
            from selenium.webdriver.firefox.options import Options, FirefoxProfile
            config_options = Options()
            profile = FirefoxProfile(FirefoxProfile.DEFAULT_PREFERENCES)
            config_options.profile = profile
            config_options.binary = which("firefox")
            logger.info(f'Browser FIREFOX config options enabled.')
        elif browser.lower() == 'opera':
            from selenium.webdriver.opera.options import Options
            config_options = Options()
            config_options.binary = which("opera")
            logger.info(f'Browser OPERA config options enabled.')
        elif browser.lower() == 'edge':
            from selenium.webdriver.edge.options import Options
            config_options = Options()
            config_options.binary = which("edge")
            logger.info(f'Browser EDGE config options enabled.')
        elif browser.lower() == 'chrome':
            from selenium.webdriver.chrome.options import Options
            config_options = Options()
            logger.info(f'## Configuring Chrome Browser with download path created at "{download_path}" ##')
            config_options.add_experimental_option("prefs", {"download.default_directory": f"{download_path}",
                                                             "download.prompt_for_download": False,
                                                             "download.directory_upgrade": True,
                                                             "safebrowsing.enabled": True})
            config_options.binary = which("chrome")
            logger.info(f'Browser CHROME config options enabled.')
        else:
            raise RuntimeError(f'{browser} browser is not supported.')
        # Configuring MAXIMIZED
        if maximized:
            logger.info(f'Setting {browser.upper()} browser to open MAXIMIZED.')
            config_options.add_argument('--start-maximized')
        logger.info(f'Setting SELENIUM SPEED to "{speed}".')
        browser_management.set_selenium_speed(speed)
        logger.info(f'Setting SELENIUM TIMEOUT to "{timeout}".')
        browser_management.set_selenium_timeout(timeout)
        logger.info(f'Setting SELENIUM IMPLICIT WAIT to "{implicit_wait}".')
        browser_management.set_selenium_implicit_wait(implicit_wait)
        # Open Browsing with/without remote URL
        if remote_url is not None:
            browser_management.open_browser(url, browser, options=config_options, remote_url=remote_url)
            logger.info(f'Browser {browser.upper()} opened in remote url {remote_url}.')
        else:
            browser_management.open_browser(url, browser, options=config_options)
            logger.info(f'Browser {browser.upper()} opened locally.')
        return browser_management.get_title()

    @keyword
    def close_all_browsers(self):
        """*FTSA closes all open browsers*

        Closes all open browsers and resets the browser cache.

        """
        browser_management = BrowserManagementKeywords(self)
        screenshot = ScreenshotKeywords(self)
        screenshot.capture_page_screenshot()
        browser_management.close_all_browsers()

    @keyword
    def login_user(self, username, password):
        """*FTSA Login the user*

        FTSA Login the user with ``username`` and ``password``.

        | *Obs:* | To properly work, page must contains id locators to ``id:username`` and ``id:password``; and a submit button with ``name:submit`` locator |

        """
        logger.info(f'FTSA logins the "{username}" user with password "{password}"')
        form_elements = FormElementKeywords(self)
        elements = ElementKeywords(self)
        waiting = WaitingKeywords(self)
        waiting.wait_until_element_is_visible(locator='id:username')
        waiting.wait_until_element_is_visible(locator='id:password')
        form_elements.input_text(locator='id:username', text=username, clear=True)
        form_elements.input_text(locator='id:password', text=password, clear=True)
        waiting.wait_until_element_is_enabled(locator='name:submit')
        elements.click_element('name:submit')

    @keyword
    def login_user_with_redirect(self, username, password, url=None):
        """*FTSA Login the user*

        FTSA Login the user with ``username`` and ``password``, redirecting to the ``url`` at the end.

        | *Obs:* | To properly work, page must contains id locators to ``id:username`` and ``id:password``; and a submit button with ``name:submit`` locator |

        """
        browser_management = BrowserManagementKeywords(self)
        elements = ElementKeywords(self)
        waiting = WaitingKeywords(self)
        if url is not None:
            browser_management.go_to(url)
        waiting.wait_until_element_is_visible(locator='xpath://*[@id="content"]/div/div/p[3]/a')
        elements.click_element(locator='xpath://*[@id="content"]/div/div/p[3]/a')
        self.login_user(username, password)
        waiting.assert_page_contains(locator='//*[@id="content"]/div[@class="alert alert-success"]')
        browser_management.go_to(url)

    @keyword
    def input_text_js(self, locator, value):
        """*FTSA input text directly from javascript*

        FTSA Input Text JavaScript with ``locator`` and ``value``. You must declare into ``locator`` type and name like this: "id:username", "xpath://input[0]", etc.

        Available ``locator`` types are: id, className, name, tagName, cssSelector and xPath

        Examples of use:
        | INPUT TEXT JS | id:username | john |
        | INPUT TEXT JS | name:password | john123 |

        *Obs:* for locator types different from ``id``, click only applied to the first result encountered.

        """
        the_type = extract_type_from(locator)
        name = extract_name_from(locator)
        javascript = JavaScriptKeywords(self)
        waiting = WaitingKeywords(self)
        waiting.wait_until_element_is_visible(locator=locator)

        if the_type.lower() == 'id':
            javascript.execute_javascript(f'document.getElementById("{name}").value = "{value}";')
        elif the_type.lower() == 'classname':
            javascript.execute_javascript(f'document.getElementsByClassName("{name}")[0].value = "{value}";')
        elif the_type.lower() == 'name':
            javascript.execute_javascript(f'document.getElementsByName("{name}")[0].value = "{value}";')
        elif the_type.lower() == 'tagname':
            javascript.execute_javascript(f'document.getElementsByTagName("{name}")[0].value = "{value}";')
        elif the_type.lower() == 'cssselector':
            javascript.execute_javascript(f'document.querySelectorAll("{name}")[0].value = "{value}";')
        elif the_type.lower() == 'xpath':
            javascript.execute_javascript(
                f'document.evaluate("{name}", document, null, '
                f'XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.value = "{value}";')
        else:
            raise Exception(f'"{the_type}" is not a valid locator type!')

    @keyword
    def click_element_js(self, locator):
        """*FTSA input text directly from javascript*

        FTSA Input Text JavaScript with ``locator`` and ``value``. You must declare into ``locator`` type and name like this: "id:confirm", "xpath://button[0]", etc.

        Available ``locator`` types are: id, className, name, tagName, cssSelector and xPath

        Examples of use:
        | CLICK ELEMENT JS | id:confirm |
        | CLICK ELEMENT JS | name:submit |

        *Obs:* for locator types different from ``id``, click only applied to the first result encountered.

        """
        the_type = extract_type_from(locator)
        name = extract_name_from(locator)
        logger.info(f'\n\nSearching for element TYPE = {the_type} ; and LOCATOR NAME = {name}\n\n')
        javascript = JavaScriptKeywords(self)
        waiting = WaitingKeywords(self)
        waiting.wait_until_element_is_visible(locator=locator)

        if the_type.lower() == 'id':
            javascript.execute_javascript(f'document.getElementById("{name}").click();')
        elif the_type.lower() == 'classname':
            javascript.execute_javascript(f'document.getElementsByClassName("{name}")[0].click();')
        elif the_type.lower() == 'name':
            javascript.execute_javascript(f'document.getElementsByName("{name}")[0].click();')
        elif the_type.lower() == 'tagname':
            javascript.execute_javascript(f'document.getElementsByTagName("{name}")[0].click();')
        elif the_type.lower() == 'cssselector':
            javascript.execute_javascript(f'document.querySelectorAll("{name}")[0].click();')
        elif the_type.lower() == 'xpath':
            javascript.execute_javascript(
                f'document.evaluate("{name}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();')
        else:
            raise Exception(f'"{the_type}" is not a valid locator type!')

    @keyword
    def init_remote_server(self, browser="chrome",
                           grid_name="grid", selenium_name='selenium',
                           port="4444", ):
        """*FTSA initialize remote server*

        FTSA creates a new container instance to run FTSA-TJPB tests inside, with the following configurations:

        | browser | The name of the browser: chrome, firefox, opera or edge are allowed |
        | grid_name | The name used to run/up network, by default: grid |
        | selenium_name | The name used to run/up selenium container, by default: selenium |
        | port | The external available port (entrypoint) to the container, by default: 4444 |

        ***If USER_GRID_NAME environment variable is set, it will be used to replace 'grid_name' during network setup.***
        ***If SELENIUM_NAME environment variable is set, it will be used to replace 'selenium_name' during container up.***
        ***If SELENIUM_EXEC_HOST environment variable is set, it will be used to replace the default hostname machine
        (you may use IP directly, for example).***
        """
        docker_client = docker.from_env()
        date_str = datetime.now().strftime("%Y%m%d%H%M%S")
        if browser == "firefox":
            browser_image_name = f'selenium/standalone-firefox:{REMOTE_VERSION}'
        elif browser == "opera":
            browser_image_name = f'selenium/standalone-opera:{REMOTE_VERSION}'
        elif browser == "edge":
            browser_image_name = f'selenium/standalone-edge:{REMOTE_VERSION}'
        elif browser == "chrome" or browser == "chromium":
            browser_image_name = f'selenium/standalone-chrome:{REMOTE_VERSION}'
        else:
            raise RuntimeError(f'{browser} browser is not supported.')

        grid_name_env = os.getenv('USER_GRID_NAME')
        if grid_name_env is None:
            grid_name = f'{date_str}_{grid_name}'
            network = docker_client.networks.create(grid_name)
            logger.info(f'{network.attrs}')
            logger.info(f'Network {grid_name} initialized.')
        else:
            grid_name = grid_name_env

        selenium_name_env = os.getenv('SELENIUM_NAME')
        if selenium_name_env is None:
            selenium_name = f'{date_str}_{selenium_name}'
        else:
            selenium_name = selenium_name_env

        try:
            selenium = docker_client.containers.get(selenium_name)
        except BaseException:
            selenium = docker_client.containers.run(
                name=f'{selenium_name}', network=f'{grid_name}',
                image=f'{browser_image_name}',
                detach=True, privileged=False,
                ports={
                    f'{port}': '4444',
                    '6900': '5900'
                }
            )
            logger.info(f'{selenium.attrs}')
            logger.info(f'Selenium container "{selenium_name}" initialized into "{grid_name}" network.')
        selenium.logs()

        host = os.getenv('SELENIUM_EXEC_HOST')
        if host is None:
            # logger.info(f'SELENIUM_EXEC_HOST environment variable was NOT FOUND!')
            # network = docker_client.networks.get(grid_name)
            # host = network.attrs["Containers"][selenium.id]["IPv4Address"].split("/")[0]
            # if host is None:
            #     logger.info(f'SELENIUM_EXEC_HOST was NOT FOUND inside {grid_name} network!')
            host = socket.gethostbyname(socket.gethostname())
        logger.info(f'Server {host}:{port} initialized.')

        time.sleep(SLEEP_SECONDS)
        return {
            "host": host,
            "port": port,
            "grid_name": grid_name,
            "selenium_name": selenium_name
        }


    @keyword
    def end_remote_server(self, grid_name="grid", selenium_name="selenium"):
        """*FTSA finalizes remote server*

        FTSA finalizes remote server:

        | grid_name | The name used to run/up network, by default: grid |
        | selenium_name | The name used to run/up selenium container, by default: selenium |

        ***If USER_EXEC_CONTAINER environment variable is set, it will be used to finish the server.***
        """
        docker_client = docker.from_env()

        try:
            selenium = docker_client.containers.get(selenium_name)
            selenium.stop()
            selenium.remove()
        except BaseException:
            logger.info(f'There is no {selenium_name} container available.')

        try:
            network = docker_client.networks.get(grid_name)
            network.remove()
        except BaseException:
            logger.info(f'There is no {grid_name} network available.')
        time.sleep(SLEEP_SECONDS)

    @keyword
    def init_record_test_video(self, test_name=None, grid_name="grid", video_name="video",
                               selenium_name="selenium"):
        """*FTSA initialize record test video*

        FTSA creates a new container instance to record test video, with the following configurations:

        | test_name | Inform the test case name. By defult, None. |
        | grid_name | The name used to initialize network, by default: grid |
        | video_name | The name user to run/up video recording container, by default: video |
        | selenium_name | The name user to reference selenium browser container, by default: selenium |
        """
        docker_client = docker.from_env()
        videos_path = f'{os.getcwd()}{os.sep}videos'
        if not os.path.isdir(videos_path):
            os.makedirs(videos_path)
        if os.getenv('VOLUME_VIDEO_RECORDING') is not None:
            videos_path = 'video_recording_volume'

        date_str = datetime.now().strftime("%Y%m%d%H%M%S")
        if test_name is not None:
            logger.info(f'Test Name was found with value "{test_name}"')
            test_name = f'-{sanitize_camel_case(test_name)}'

        selenium_name_env = os.getenv('SELENIUM_NAME')
        if selenium_name_env is not None:
            logger.info(f'Selenium Name Environment was found with value "{selenium_name_env}"')
            selenium_name = selenium_name_env

        video_image_name = f'selenium/video:{REC_VIDEO_VERSION}'
        logger.info(f'Videos path "{videos_path}" is enable to store recordings.')
        try:
            video = docker_client.containers.get(video_name)
        except BaseException:
            video = docker_client.containers.run(
                name=f'{video_name}', network=f'{grid_name}',
                image=f'{video_image_name}',
                detach=True, privileged=False,
                environment=[
                    f'DISPLAY_CONTAINER_NAME={selenium_name}',
                    f'FILE_NAME={date_str}{test_name}-video.mp4'
                ],
                volumes={
                    f'{videos_path}': {'bind': '/videos', 'mode': 'rw'}
                }
            )
            logger.info(f'{video.attrs}')
            logger.info(f'Record video server initialized into "{grid_name}" network.')
        video.logs()
        time.sleep(SLEEP_SECONDS)

    @keyword
    def end_record_test_video(self, video_name="video"):
        """*FTSA finalizes record test video*

        FTSA finalizes remote test video recorder:

        | video_name | The name used to run/up video container, by default: video |
        """
        docker_client = docker.from_env()
        try:
            video = docker_client.containers.get(video_name)
            video.stop()
            video.remove()
        except BaseException:
            logger.info(f'There is no {video_name} container available.')
        time.sleep(SLEEP_SECONDS)
