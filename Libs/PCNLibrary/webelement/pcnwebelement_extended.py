from selenium.webdriver.remote.webelement import WebElement


def js_click(self):
    # self.scroll_to_webelement()
    self.parent.execute_script("arguments[0].click();", self)

def remove_hidden_attribute(self):
    self.parent.execute_script("arguments[0].removeAttribute('hidden');", self)

def scroll_to_webelement(self):
    self.parent.execute_script("arguments[0].scrollIntoView();", self)

def get_textContent(self):
    return self.get_attribute("textContent").strip()

def is_visible(self):
    return self.parent.execute_script("return arguments[0].style.display != 'none';", self)

WebElement.js_click = js_click
WebElement.scroll_to_webelement = scroll_to_webelement
WebElement.get_textContent = get_textContent
WebElement.is_visible = is_visible
WebElement.remove_hidden_attribute = remove_hidden_attribute