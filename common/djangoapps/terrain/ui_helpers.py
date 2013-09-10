#pylint: disable=C0111
#pylint: disable=W0621

from lettuce import world
import time
import platform
from urllib import quote_plus
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from lettuce.django import django_url
from nose.tools import assert_true  # pylint: disable=E0611


@world.absorb
def wait(seconds):
    time.sleep(float(seconds))


@world.absorb
def visit(url):
    world.browser.visit(django_url(url))


@world.absorb
def url_equals(url):
    return world.browser.url == django_url(url)


@world.absorb
def is_css_present(css_selector, wait_time=10):
    return world.browser.is_element_present_by_css(css_selector, wait_time=wait_time)


@world.absorb
def is_css_not_present(css_selector, wait_time=5):
    return world.browser.is_element_not_present_by_css(css_selector, wait_time=wait_time)


@world.absorb
def css_has_text(css_selector, text, index=0, max_attempts=5):
    return world.css_text(css_selector, index=index, max_attempts=max_attempts) == text


@world.absorb
def wait_for(func, timeout=5):
    WebDriverWait(world.browser.driver, timeout).until(func)


def wait_for_present(css_selector, timeout=30):
    """
    Waiting for the element to be present in the DOM.
    Throws an error if the wait_for time expires.
    Otherwise this method will return None
    """
    WebDriverWait(driver=world.browser.driver,
        timeout=60).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector,)))


def wait_for_visible(css_selector, timeout=30, delay=0):
    """
    Waiting for the element to be visible in the DOM.
    Throws an error if the wait_for time expires.
    Otherwise this method will return None
    """
    wait(delay)
    WebDriverWait(driver=world.browser.driver,
        timeout=timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector,)))


def wait_for_clickable(css_selector, timeout=30, delay=0):
    """
    Waiting for the element to be present and clickable.
    Throws an error if the wait_for time expires.
    Otherwise this method will return None
    """
    # Sometimes the element is clickable then gets obscured.
    # In this case, pause so that it is not reported clickable too early
    wait(delay)
    WebDriverWait(world.browser.driver,
        timeout=timeout).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector,)))


@world.absorb
def css_find(css, wait_time=30):
    wait_for_present(css_selector=css, timeout=wait_time)
    return world.browser.find_by_css(css)


@world.absorb
def css_click(css_selector, index=0, wait_time=30, delay=0):
    """
    Perform a click on a CSS selector, first waiting for the element
    to be present and clickable.

    This method will return True if the click worked.
    """
    wait_for_clickable(css_selector, timeout=wait_time, delay=delay)
    return world.css_find(css_selector)[index].click()


@world.absorb
def css_check(css_selector, index=0, wait_time=30, delay=0):
    """
    Checks a check box based on a CSS selector, first waiting for the element
    to be present and clickable. This is just a wrapper for calling "click"
    because that's how selenium interacts with check boxes and radio buttons.

    This method will return True if the check worked.
    """
    return css_click(css_selector, index, wait_time, delay)


@world.absorb
def css_click_at(css_selector, x_cord=10, y_cord=10, wait_time=5, delay=0):
    '''
    A method to click at x,y coordinates of the element
    rather than in the center of the element
    '''
    wait_for_clickable(css_selector, wait_time=wait_time, delay=delay)
    element = css_find(css_selector).first
    element.action_chains.move_to_element_with_offset(element._element, x_cord, y_cord)
    element.action_chains.click()
    element.action_chains.perform()


@world.absorb
def id_click(elem_id):
    """
    Perform a click on an element as specified by its id
    """
    world.css_click('#%s' % elem_id)


@world.absorb
def css_fill(css_selector, text, index=0, max_attempts=5):
    assert is_css_present(css_selector)
    return world.retry_on_exception(lambda: world.browser.find_by_css(css_selector)[index].fill(text), max_attempts=max_attempts)


@world.absorb
def click_link(partial_text, index=0, max_attempts=5):
    return world.retry_on_exception(lambda: world.browser.find_link_by_partial_text(partial_text)[index].click(), max_attempts=max_attempts)


@world.absorb
def css_text(css_selector, index=0, max_attempts=5):

    # Wait for the css selector to appear
    if is_css_present(css_selector):
        return world.retry_on_exception(lambda: world.browser.find_by_css(css_selector)[index].text, max_attempts=max_attempts)
    else:
        return ""


@world.absorb
def css_value(css_selector, index=0, max_attempts=5):

    # Wait for the css selector to appear
    if is_css_present(css_selector):
        return world.retry_on_exception(lambda: world.browser.find_by_css(css_selector)[index].value, max_attempts=max_attempts)
    else:
        return ""


@world.absorb
def css_html(css_selector, index=0, max_attempts=5):
    """
    Returns the HTML of a css_selector and will retry if there is a StaleElementReferenceException
    """
    assert is_css_present(css_selector)
    return world.retry_on_exception(lambda: world.browser.find_by_css(css_selector)[index].html, max_attempts=max_attempts)


@world.absorb
def css_has_class(css_selector, class_name, index=0, max_attempts=5):
    return world.retry_on_exception(lambda: world.css_find(css_selector)[index].has_class(class_name), max_attempts=max_attempts)


@world.absorb
def css_visible(css_selector, index=0, max_attempts=5):
    assert is_css_present(css_selector)
    return world.retry_on_exception(lambda: world.browser.find_by_css(css_selector)[index].visible, max_attempts=max_attempts)


@world.absorb
def dialogs_closed():
    def are_dialogs_closed(_driver):
        '''
        Return True when no modal dialogs are visible
        '''
        return not css_visible('.modal')
    wait_for(are_dialogs_closed)
    return not css_visible('.modal')


@world.absorb
def save_the_html(path='/tmp'):
    url = world.browser.url
    html = world.browser.html.encode('ascii', 'ignore')
    filename = "{path}/{name}.html".format(path=path, name=quote_plus(url))
    with open(filename, "w") as f:
        f.write(html)


@world.absorb
def click_course_content():
    course_content_css = 'li.nav-course-courseware'
    world.css_click(course_content_css)


@world.absorb
def click_course_settings():
    course_settings_css = 'li.nav-course-settings'
    world.css_click(course_settings_css)


@world.absorb
def click_tools():
    tools_css = 'li.nav-course-tools'
    world.css_click(tools_css)


@world.absorb
def is_mac():
    return platform.mac_ver()[0] is not ''


@world.absorb
def is_firefox():
    return world.browser.driver_name is 'Firefox'


@world.absorb
def trigger_event(css_selector, event='change', index=0):
    world.browser.execute_script("$('{}:eq({})').trigger('{}')".format(css_selector, index, event))


@world.absorb
def retry_on_exception(func, max_attempts=5):
    attempt = 0
    while attempt < max_attempts:
        try:
            return func()
            break
        except WebDriverException:
            world.wait(1)
            attempt += 1
        except:
            attempt += 1
    assert_true(attempt < max_attempts, 'Ran out of attempts to execute {}'.format(func))
