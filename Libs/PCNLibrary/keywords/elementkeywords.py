from SeleniumLibrary.base import keyword, LibraryComponent
from SeleniumLibrary.keywords import ElementKeywords as SeleniumElementKeywords
from SeleniumLibrary.keywords import FormElementKeywords, WaitingKeywords
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement


class ElementKeywords(LibraryComponent):

    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)
        self.element_management = SeleniumElementKeywords(ctx)
        self.formelement_management = FormElementKeywords(ctx)
        self.waiting_management = WaitingKeywords(ctx)

    @keyword
    def clear_textfield_value(self, locator):
        text = self.element_management.get_value(locator)
        i = 0
        while i < len(text):
            i += 1
            self.element_management.press_key(locator, Keys.BACK_SPACE)
            self.element_management.press_key(locator, Keys.DELETE)

    @keyword
    def scroll_to_element(self, locator):
        self.waiting_management.wait_until_element_is_visible(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", self.find_element(locator))

    @keyword
    def scroll_to_top(self, webelement):
        js = "arguments[0].scrollTo(0,-2*arguments[0].scrollHeight);"
        self.driver.execute_script(js, webelement)

    @keyword
    def scroll_to_bottom(self, webelement):
        js = "arguments[0].scrollTo(0,2*arguments[0].scrollHeight);"
        self.driver.execute_script(js, webelement)

    @keyword
    def special_click_element(self, locator):
        try:
            element = self.find_element(locator)
            element.remove_hidden_attribute()
            element.js_click()
        except:
            raise AssertionError("Failed to click element")
            return

    @keyword
    def my_click(self, locator):
        self.find_element(locator).click()

    @keyword
    def set_toggle_button_value(self, element_locator, value):
        element = self.find_element(element_locator)
        current_status = element.get_attribute('className')
        if current_status != value:
            element.js_click()
            return
        return "Failed to set toggle button value"

    @keyword
    def get_toggle_button_value(self, element_locator):
        element = self.find_element(element_locator)
        current_status = element.get_attribute('className')
        if current_status == "toggle active":
            return "True"
        return "False"

    @keyword
    def click_hidden_element(self, locator):
        try:
            if not self._is_element(locator):
                if "auto-tag" in locator:
                    element = self.get_element_by_auto_tag(locator)
                else:
                    element = self.find_element(locator)
            element.remove_hidden_attribute()
            element.js_click()
        except:
            message = "Failed to click on hidden element %s" % locator
            raise AssertionError(message)

    @keyword
    def input_text(self, locator, text):
        self.scroll_to_element(locator)
        # self.clear_textfield_value(locator)
        self.formelement_management.input_text(locator, text)

    @keyword
    def input_password(self, locator, password):
        self.scroll_to_element(locator)
        self.formelement_management.input_password(locator, password)

    @keyword
    def get_elements_by_attribute(self, attribute):
        """
        Get element that has attribute with value
        :param attribute: <attribute_name>=<attribute_value>
        :return: list of found elements
        """
        attribute_name = attribute.split('=')[0]
        attribute_value = attribute.split('=')[1].replace('"', '')
        return self.driver.find_elements_by_xpath("//*[@" + attribute_name + "='" + attribute_value + "']")

    @keyword
    def get_element_by_attribute(self, attribute):
        elements = self.get_elements_by_attribute(attribute)
        return elements[0] if len(elements) > 0 else elements

    @keyword
    def get_element_by_auto_tag(self, auto_tag):
        return self.get_element_by_attribute(auto_tag)

    @keyword
    def get_elements_by_auto_tag(self, auto_tag):
        return self.get_elements_by_attribute(auto_tag)

    @keyword
    def get_elements_by_tag(self, locator, tag):
        try:
            elements = self.find_elements(locator)
            if len(elements) == 1:
                if elements[0].get_property("tagName") == tag.upper():
                    return elements
                else:
                    return elements[0].find_elements_by_tag_name(tag)
            else:
                return [e for e in elements if e.get_property("tagName") == tag.upper()]
        except:
            message = "Cannot get element(s) by tag '%s' with locator '%s'" % (tag, locator)
            raise AssertionError(message)

    @keyword
    def find_element_contains_class(self, class_name):
        class_list = class_name.split(' ')
        elements = self.driver.find_elements_by_class_name(class_list[0])
        for element in elements:
            actual_class_list = element.get_attribute("class").split(' ')
            if Utilities().is_sublist(actual_class_list, class_list[1:]):
                return element
        message = "Not found any element has '%s'" % class_name
        raise AssertionError(message)

    @keyword
    def wait_until_element_has_class(self, element, class_name, timeout=5, error=None):
        """
        Wait until element contain class name
        :param element: element
        :param class_name: class name to expect element will has
        :param timeout: timeout in second
        :param error: error message
        :return: None
        """
        self.waiting_management._wait_until(
            lambda: class_name in element.get_attribute("class"),
            "Element '%s' has no class name '%s' in <TIMEOUT>" % (element, class_name),
            timeout,
            error
        )

    @keyword
    def wait_until_element_has_number_child(self, element, class_name, children_num=1, timeout=5, error=None):
        """
        Wait until the element has number of children as expected
        :param element: parent element
        :param class_name: class name of child element
        :param children_num: expected number of children need to wait for
        :param timeout: timeout in second
        :param error: error message
        :return: None
        """
        self.waiting_management._wait_until(
            lambda: len(element.find_elements_by_class_name(class_name)) == children_num,
            "Element '%s' has more than one child '%s' in <TIMEOUT>" % (element, class_name),
            timeout,
            error
        )

    def _is_element(self, item):
        return isinstance(item, WebElement)

    @keyword
    def get_element_contains_text_in_list(self, elements, text):
        """
        Get the element from the list which has input text
        :param elements: list of elements
        :param text: text of finding element
        :return: the element which has input text
        """
        for element in elements:
            actual = element.get_textContent()
            if str(text).strip() == actual:
                return element
        message = "Not found %s in list!" % text
        raise AssertionError(message)

    @keyword
    def select_item_in_list(self, elements, value):
        try:
            element = self.get_element_contains_text_in_list(elements, value)
            element.js_click()
        except:
            message = "Failed to select item %s in list!" % value
            raise AssertionError(message)

    @keyword
    def get_element_text(self, locator):
        text = self.find_element(locator)
        result = text.get_attribute("textContent")
        return result

    @keyword
    def set_special_list_value(self, locator, value):
        list_value = self.find_element(locator)
        values = list_value.find_elements_by_tag_name('span')
        for val in values:
            if val.get_textContent() == value:
                val.click()
                return
        mess = "Not Found By %s" %value
        raise AssertionError(mess)

    @keyword
    def compare_special_element_text(self, locator, value):
        element = self.find_element(locator)
        props = element.get_attribute("textContent")
        if value == props:
            return True
        else:
            mess = ("The text of element '%s' should have been '%s' "
             "but it was '%s'." % (locator, value, props))
            raise AssertionError(mess)

    @keyword
    def is_disabled(self, locator):
        element = self.find_element(locator)
        props = element.get_attribute("disabled")
        if props == 'true':
            return True
        mess = "Element still is enabled"
        raise AssertionError(mess)

    @keyword
    def wait_until_element_is_disabled(self, locator, timeout=30, error=None):
        self.waiting_management._wait_until(
            lambda: self.is_disabled(locator),
            "Element '%s' still in enable over <TIMEOUT>." % locator,
            timeout,
            error
        )

    @keyword
    def text_field_is_disabled(self, locator):
        element = self.find_element(locator)
        props = element.get_attribute("readonly")
        if props == "true":
            return True
        mess = "Text field %s is enabled" % locator
        raise AssertionError(mess)

    @keyword
    def wait_until_text_field_is_disabled(self, locator, timeout=30, error=None):
        self.waiting_management._wait_until(
            lambda: self.text_field_is_disabled(locator),
            "Element '%s' still in enable over <TIMEOUT>." % locator,
            timeout,
            error
        )

    @keyword
    def get_length_selectbox(self, locator):
        element = self.find_element(locator)
        props = element.find_elements_by_tag_name('option')
        return len(props)

    # @keyword
    # def upload_file_in_edge_browser(self, file_path, element_locator):
    #     element = self.find_element(element_locator)
    #     element.js_click()
    #     try:
    #         autoit.control_focus("Open", "Edit1")
    #         autoit.control_set_text("Open", "Edit1", str(file_path))
    #         autoit.control_click("Open", "Button1")
    #     except ValueError:
    #         raise AssertionError(ValueError)
    #         return