# system modules
import os
import inspect
import time
import logging
import functools
import itertools
import operator
import types
import re
from dataclasses import dataclass

# internal modules

# external modules
import rich
from rich.console import Console
import selenium.webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import (
    text_to_be_present_in_element,
)
import click

logger = logging.getLogger(__name__)


class Timeout(Exception):
    """
    Class for timeout errors
    """

    pass


def sanitize_rpm(s):
    """
    Produce a string usable for comparison of RPM names because OpenRepos does
    some changes to the RPM names
    """
    return re.sub(r"[^a-zA-Z0-9]+", r"", os.path.basename(str(s)).lower())


def action(description=None):
    """
    Create a decorator to ask before calling a function
    """

    def decorator(decorated_function):
        @functools.wraps(decorated_function)
        def wrapper(self, *args, **kwargs):
            docline = next(
                filter(
                    bool,
                    re.split(
                        r"\s*\n+\s*",
                        getattr(decorated_function, "__doc__", "") or "",
                    ),
                ),
                None,
            )
            actiontext = next(
                filter(bool, filter(bool, (description, docline))),
                decorated_function.__name__,
            )
            if self.interactive:
                while True:
                    proceed = click.prompt(
                        "{indent}{question}?".format(
                            indent=" " * (getattr(action, "depth", 0) * 2),
                            question=actiontext,
                        ),
                        type=click.Choice(("y", "n", "skip", "shell")),
                        default="y",
                    )
                    if proceed.lower() == "y":
                        logger.info("Executing {}".format(repr(actiontext)))
                        setattr(
                            action, "depth", getattr(action, "depth", 0) + 1
                        )
                        logger.info("Executing {}".format(repr(actiontext)))
                        ret = decorated_function(self, *args, **kwargs)
                        setattr(
                            action,
                            "depth",
                            max(0, getattr(action, "depth", 0) - 1),
                        )
                        return ret
                    elif proceed.lower() == "n":
                        raise click.Abort()
                    elif proceed.lower() == "skip":
                        return
                    elif proceed.lower() == "shell":
                        import IPython

                        client = self

                        IPython.embed(
                            header="The client can be accessed "
                            "via the `client` variable. "
                            "The webdriver instance is "
                            "accessible through `client.webdriver`. "
                            "Run `exit` or press CTRL-D to "
                            "quit the interactive session."
                        )
            setattr(action, "depth", getattr(action, "depth", 0) + 1)
            logger.info("Executing {}".format(repr(actiontext)))
            ret = decorated_function(self, *args, **kwargs)
            setattr(action, "depth", max(0, getattr(action, "depth", 0) - 1))
            return ret

        return wrapper

    return decorator


action.depth = 0


@dataclass
class Client:
    """
    OpenRepos.net web client
    """

    OPENREPOS_HOMEPAGE = "https://openrepos.net"

    username: str = ""
    password: str = ""
    interactive: bool = False
    webdriver_name: str = os.environ.get("OPENREPOS_WEBCLIENT_WEBDRIVER", "")
    console: Console = Console()

    @staticmethod
    def matching_webdriver(s=""):
        """
        Generator yielding matching :any:`WebDriver` classes
        """
        for subcls in WebDriver.__subclasses__():
            for name, v in selenium.webdriver.__dict__.items():
                if v is subcls:
                    if s.lower() in name.lower():
                        yield (name, subcls)

    @action("Open the webdriver")
    def create_webdriver(self):
        """
        Create the webdriver
        """
        webdrivers = list(self.matching_webdriver(self.webdriver_name))
        logger.debug(f"{webdrivers = }")
        if not webdrivers:
            raise ValueError(f"No useable webdrivers??")
        name, webdriver = webdrivers[0]
        logger.debug(f"Creating {name} webdriver")
        return webdriver()

    @functools.cached_property
    def webdriver(self):
        webdriver = self.create_webdriver()
        # logger.debug(f"⏳ Waiting 10 seconds for the webdriver to load...")
        # webdriver.implicitly_wait(10)
        return webdriver

    def find_element(self, *args, timeout=10, multiple=False, **kwargs):
        time_before = time.time()
        time_shown_last = time_before
        desc = " ".join(
            itertools.chain(
                map(repr, args), [f"{k}={v!r}" for k, v in kwargs.items()]
            )
        )
        finder = (
            self.webdriver.find_elements
            if multiple
            else self.webdriver.find_element
        )
        with self.console.status(f"⏳🔎 Waiting for {desc} to appear..."):
            for n in itertools.count(1):
                if time.time() - time_before > timeout:
                    logger.warning(
                        f"🤷 Couldn't find {desc} after {n} tries and {time.time() - time_before}s"
                    )
                    return None
                if time.time() - time_shown_last > 2:
                    logger.info(f"⏳🔎 Still Waiting for {desc} to appear...")
                    time_shown_last = time.time()
                try:
                    element = finder(*args, **kwargs)
                except NoSuchElementException as e:
                    element = None
                if element:
                    logger.debug(
                        f"✅ Found {len(element) if isinstance(element,(list,tuple)) else 1} "
                        f"matches for {desc} "
                        f"after {n} tries in {time.time() - time_before}s"
                    )
                    return element
                time.sleep(0.5)

    def find_elements(self, *args, **kwargs):
        return (
            self.find_element(*args, **{**kwargs, **dict(multiple=True)}) or []
        )

    def execute_action(
        self, fun, *args, mask_args=False, description=None, **kwargs
    ):
        decorator = action(description=description)
        if logger.getEffectiveLevel() < logging.DEBUG:
            logger.debug("Decorating {} with {}".format(fun, decorator))
        if not isinstance(getattr(fun, "__self__", object), type(self)):
            if logger.getEffectiveLevel() < logging.DEBUG:
                logger.debug("Converting to methodtype")

            def wrapper(self, *args, **kwargs):
                return fun(*args, **kwargs)

            decorated_function = decorator(wrapper)
        else:
            decorated_function = decorator(fun)
        try:
            delay = float(os.environ.get("OPENREPOS_ACTION_DELAY", 0))
        except (TypeError, ValueError):
            logger.warning(
                "Weird OPENREPOS_ACTION_DELAY ({})".format(
                    repr(os.environ.get("OPENREPOS_ACTION_DELAY"))
                )
            )
            delay = None
        if delay:
            if logger.getEffectiveLevel() < logging.DEBUG:
                logger.debug(
                    "Waiting {} seconds before calling {} with {}, {}".format(
                        delay,
                        decorated_function,
                        "***" if mask_args else args,
                        kwargs,
                    )
                )
            time.sleep(delay)
        if logger.getEffectiveLevel() < logging.DEBUG:
            logger.debug(
                "Calling {} with {}, {}".format(
                    decorated_function, "***" if mask_args else args, kwargs
                )
            )
        return decorated_function(self, *args, **kwargs)

    def wait(
        self,
        condition=lambda driver: True,
        interval=1,
        timeout=10,
        tries=float("inf"),
    ):
        """
        Wait until a condition is met

        Args:
            condition (callable): callable taking the driver as single argument
                and returning a boolean whether the waiting should stop
            interval (float, optional): at what intervals the condition should
                be checked
            timeout (float, optional): after what time the waiting should
                timeout and raise an error.
            tries (int, optional): how many times the conditions should be
                tried. Defaults to infinity.

        Raises:
            Timeout : if the waiting timed out
        """
        try_ = itertools.count(0)
        time_before = time.time()
        time_last_check = 0
        desc = str(
            getattr(condition, "__doc__", inspect.getsource(condition))
        ).strip()
        with self.console.status(f"⏳ Waiting for {desc}..."):
            while True:
                if next(try_) > tries:
                    raise Timeout(
                        f"Timeout waiting for {desc!r} after {try_} tries"
                    )
                if time.time() - time_before > timeout:
                    raise Timeout(
                        f"Timeout waiting for {desc!r} "
                        f"after {time.time() - time_before:.1f} seconds"
                    )
                if time.time() - time_last_check < interval:
                    time.sleep(0.1)
                    continue
                logger.debug(f"Checking {desc!r}...")
                if result := condition(self.webdriver):
                    logger.info(f"Condition {desc!r} met!")
                    return
                else:
                    logger.debug(f"Condition {desc!r} not met yet...")
                    time_last_check = time.time()

    @action()
    def go_to_home_page(self):
        """
        Go to the home page
        """
        self.webdriver.get(self.OPENREPOS_HOMEPAGE)

    @action()
    def go_to_my_apps(self):
        """
        Go to the My Applications page
        """
        my_apps_link = self.find_element(
            By.LINK_TEXT, "My Applications", timeout=2
        )
        if my_apps_link:
            my_apps_link.click()
        else:
            logger.debug(
                "Can't find 'My Applications' link. Probably not logged in."
            )
            self.login()
            logger.debug("Retrying to go to My Applications")
            self.find_element(By.LINK_TEXT, "My Applications").click()

    @action()
    def go_to_new_app(self):
        """
        Go to Add Application page
        """
        try:
            link = self.find_element(By.LINK_TEXT, "Add Application")
            self.execute_action(
                link.click, description="Click ”Add Application” link"
            )
        except NoSuchElementException:
            logger.debug(
                "Can't find Add Application link. Probably not logged in."
            )
            self.login()
            logger.debug("Retrying to go to New Application")
            link = self.find_element(By.LINK_TEXT, "Add Application")
            self.execute_action(
                link.click, description="Click Add Aplication link"
            )

    @action()
    def new_app(self, name, platform, category):
        """
        Create a new app
        """
        self.go_to_new_app()
        links = self.find_elements(
            By.XPATH, "//div[@id='block-system-main']//a"
        )
        try:
            link = next(
                filter(
                    lambda e: re.match(r"(.*?)\s+Application$", e.text)
                    and str(platform).lower() in e.text.lower(),
                    links,
                )
            )
        except (StopIteration, NoSuchElementException):
            raise click.UsageError(
                "Can't find link for platform {}. "
                "Possible values are {}".format(
                    repr(platform),
                    ", ".join(
                        map(
                            repr,
                            map(
                                operator.methodcaller("group", 1),
                                filter(
                                    bool,
                                    map(
                                        lambda e: re.match(
                                            r"(.*?)\s+Application$", e.text
                                        ),
                                        links,
                                    ),
                                ),
                            ),
                        )
                    ),
                )
            )
        self.execute_action(
            link.click, description="Click {} link".format(repr(link.text))
        )
        title_field = self.find_element(By.ID, "edit-title")
        self.execute_action(
            title_field.send_keys,
            name,
            description="Enter {} title".format(repr(name)),
        )
        category_menu = Select(
            self.find_element(
                By.ID, "edit-field-category-und-hierarchical-select-selects-0"
            )
        )
        try:
            index = next(
                (
                    i
                    for i, e in enumerate(category_menu.options)
                    if (
                        category.lower() in e.text.lower()
                        and "none" not in e.text.lower()
                    )
                )
            )
        except StopIteration:
            raise click.UsageError(
                "No such category {}. "
                "Possible selections include {}".format(
                    repr(category),
                    ", ".join(
                        map(
                            repr,
                            map(
                                operator.methodcaller("group", 1),
                                filter(
                                    bool,
                                    map(
                                        lambda e: re.match(
                                            r"(?!<)(.*?)\s*(?:\(\d+\))?$",
                                            e.text,
                                        ),
                                        category_menu.options,
                                    ),
                                ),
                            ),
                        )
                    ),
                )
            )
        self.execute_action(
            category_menu.select_by_index,
            index,
            description="Select category {}".format(
                repr(category_menu.options[index].text)
            ),
        )

        def save():
            save_button = self.find_element(By.ID, "edit-submit--2")
            save_button.click()

            def wait_for_messages(driver):
                """
                Wait for a div with id 'messages' containing 'has been updated'
                """
                return any(
                    "has been created" in t
                    for t in [
                        e.text
                        for e in driver.find_elements(
                            By.XPATH, "//div[@id='messages']"
                        )
                    ]
                )

            self.wait(wait_for_messages)
            logger.info("Saved!")

        self.execute_action(save, description="Click Save button")

    @action()
    def find_applink_in_my_apps(self, appname=None):
        """
        Find the link to the App in 'My Applications'
        """
        self.go_to_my_apps()

        logger.info("🔎 Looking for existing app links...")
        applinks = self.find_elements(
            By.XPATH, "//div[@class='content']//tbody//tr//td[1]//a"
        )
        logger.info(
            f"Found {len(applinks)} exsiting apps: {[e.text for e in applinks]}"
        )
        applink = next(
            itertools.chain(
                filter(lambda e: e.text.lower() == appname.lower(), applinks),
                filter(lambda e: e.text.lower() in appname.lower(), applinks),
            ),
            None,
        )
        return applink

    @action()
    def delete_app(self, appname=None):
        """
        Delete App
        """
        applink = self.find_applink_in_my_apps(appname)

        if not applink:
            logger.error(f"App {appname} doesn't exist, no need to delete it.")
            return

        self.execute_action(
            applink.click,
            description="Click {} link".format(repr(applink.text)),
        )

        edit_link = self.find_element(By.LINK_TEXT, "Edit")
        self.execute_action(
            edit_link.click,
            description=f"Click {edit_link.text!r} link",
        )

        delete_button = self.find_element(
            By.CSS_SELECTOR, "input[value=Delete]"
        )
        self.execute_action(
            delete_button.click,
            description=f"Click {delete_button.text!r} link",
        )

        delete_button = self.find_element(
            By.CSS_SELECTOR, "input[value=Delete]"
        )
        self.execute_action(
            delete_button.click,
            description=f"Click confirmation {delete_button.text!r} link",
        )

        def wait_for_messages(driver):
            """
            Wait for a div with id 'messages' containing 'has been deleted'
            """
            return any(
                "has been deleted" in t
                for t in [
                    e.text
                    for e in driver.find_elements(
                        By.XPATH, "//div[@id='messages']"
                    )
                ]
            )

        self.wait(wait_for_messages)
        logger.info("✅ Successfully deleted! 🗑️")

    @action()
    def upload_rpm(
        self,
        appname=None,
        rpmfiles=None,
        create_app=False,
        platform=None,
        category=None,
    ):
        """
        Upload RPM file(s)
        """
        applink = self.find_applink_in_my_apps(appname)

        if not applink:
            logger.info(
                "It seems the app {} doesn't exist yet.".format(repr(appname))
            )
            if create_app:
                logger.info("Creating app {}".format(repr(appname)))
                self.new_app(
                    name=appname, platform=platform, category=category
                )
                logger.info(
                    "Now trying to upload the RPM(s) to {} again.".format(
                        repr(appname)
                    )
                )
                self.upload_rpm(
                    appname=appname,
                    rpmfiles=rpmfiles,
                    create_app=False,
                )
                return
            else:
                raise ValueError(
                    "App {} doesn't exist. Can't upload RPM(s).".format(
                        repr(appname)
                    )
                )

        logger.info("Found matching app link {}".format(repr(applink.text)))

        self.execute_action(
            applink.click,
            description="Click {} link".format(repr(applink.text)),
        )

        rpmlinks = self.find_elements(
            By.XPATH, "//div[@class='content']//tbody//tr//td[1]//a"
        )

        logger.debug("This app has {} RPMs".format(len(rpmlinks)))

        rpmfiles_to_upload = []

        for rpmfile in rpmfiles:
            rpmfilename = os.path.basename(rpmfile)
            if any(
                sanitize_rpm(e.text) == sanitize_rpm(rpmfilename)
                for e in rpmlinks
            ):
                logger.warning(
                    f"RPM file {rpmfilename!r} is already present. Skipping!"
                )
                continue
            rpmfiles_to_upload.append(rpmfile)

        edit_link = self.find_element(By.LINK_TEXT, "Edit")
        self.execute_action(
            edit_link.click,
            description="Click {} link".format(repr(edit_link.text)),
        )

        if not rpmfiles_to_upload:
            click.echo("No RPM files to upload that aren't already there.")

        for rpmfile in rpmfiles_to_upload:
            rpmfile = os.path.abspath(rpmfile)

            def select_rpmfile_for_upload():
                logger.info(
                    "Selecting rpm file '{}' for upload...".format(rpmfile)
                )
                package_upload_selector = next(
                    filter(
                        lambda e: all(
                            w in e.get_attribute("id")
                            for w in ("package", "upload")
                        ),
                        self.find_elements(By.XPATH, "//input[@type='file']"),
                    ),
                    None,
                )
                if not package_upload_selector:
                    raise ValueError(
                        "Don't know where to select the RPM to upload... "
                        "Can't find the button."
                    )
                package_upload_selector.send_keys(rpmfile)
                logger.info(
                    "rpm file '{}' selected for upload...".format(rpmfile)
                )

            self.execute_action(
                select_rpmfile_for_upload,
                description="Select RPM file {} for upload".format(
                    repr(rpmfile)
                ),
            )

            def upload_rpm_file():
                logger.info("Uploading RPM file '{}'...".format(rpmfile))
                package_upload_button = next(
                    filter(
                        lambda e: all(
                            w in e.get_attribute("id")
                            for w in ("package", "upload")
                        ),
                        self.find_elements(
                            By.XPATH, "//input[@type='submit']"
                        ),
                    ),
                    None,
                )
                if not package_upload_button:
                    raise ValueError(
                        "Don't know where to click to upload the RPM to... "
                        "Can't find the button."
                    )
                package_upload_button.click()

                def wait_for_rpm_in_table(driver):
                    """
                    Wait for the RPM file to appear in the list
                    """
                    return sanitize_rpm(os.path.basename(rpmfile)) in [
                        sanitize_rpm(e.text)
                        for e in driver.find_elements(
                            By.XPATH, "//table//span[@class='file']"
                        )
                    ]

                self.wait(wait_for_rpm_in_table)
                logger.info(f"RPM file {rpmfile!r} uploaded.")

            self.execute_action(
                upload_rpm_file,
                description="Upload RPM file {}".format(repr(rpmfile)),
            )

            time.sleep(1)

        def save():
            logger.info("Saving...")
            self.find_element(By.CSS_SELECTOR, "input[value=Save]").click()

            def wait_for_messages(driver):
                """
                Wait for a div with id 'messages' containing 'has been updated'
                """
                return any(
                    "has been updated" in t
                    for t in [
                        e.text
                        for e in driver.find_elements(
                            By.XPATH, "//div[@id='messages']"
                        )
                    ]
                )

            self.wait(wait_for_messages)
            logger.info("Saved!")

        self.execute_action(save, description="Save")

    @action()
    def login(self, username=None, password=None):
        """
        Log in to the account
        """
        if self.webdriver.current_url != self.OPENREPOS_HOMEPAGE:
            self.go_to_home_page()

        if not username:
            username = self.username
        if not password:
            password = self.password

        if not (username and password):
            raise ValueError("Both username and password must be specified!")

        username_field = self.find_element(By.ID, "edit-name")
        self.execute_action(
            username_field.send_keys, username, description="Type username"
        )

        password_field = self.find_element(By.ID, "edit-pass")
        self.execute_action(
            password_field.send_keys,
            password,
            mask_args=True,
            description="Type password",
        )

        login_button = self.find_element(By.ID, "edit-submit--3")
        self.execute_action(
            login_button.click, description="Click Login Button"
        )

    @action()
    def close(self):
        """
        Close the webdriver
        """
        if webdriver := self.__dict__.get("webdriver"):
            try:
                webdriver.close()
                del self.webdriver
            except BaseException as e:
                logger.error(
                    "There was an error closing the webdriver. Oh well... 🤷"
                )

    def __del__(self):
        self.interactive = False
        if getattr(self, "_webdriver", None):
            self.close()
