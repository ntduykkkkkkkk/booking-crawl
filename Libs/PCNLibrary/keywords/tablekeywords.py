from SeleniumLibrary.base import keyword, LibraryComponent
from .elementkeywords import ElementKeywords
from SeleniumLibrary.keywords import WaitingKeywords

class TableKeywords(LibraryComponent):

    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)
        self.elementkeywords_management = ElementKeywords(ctx)
        self.waiting_management = WaitingKeywords(ctx)

    def get_table(self, locator):
        self.wait_until_table_loaded(locator)
        # return self.find_element(locator)
        return self.elementkeywords_management.get_element_by_auto_tag(locator).find_element_by_tag_name("table")

    @keyword
    def wait_until_table_loaded(self, locator, timeout=150, error=None):
        try:
            self.wait_until_table_loading(locator)
        except:
            None
        self.waiting_management._wait_until(
            lambda: self.is_table_loaded(locator),
            "Table '%s' still in loading over <TIMEOUT>." % locator,
            timeout,
            error
        )

    def wait_until_table_loading(self, locator, timeout=2, error=None):
        self.waiting_management._wait_until(
            lambda: not self.is_table_loaded(locator),
            "Table '%s' still in loading over <TIMEOUT>." % locator,
            timeout,
            error
        )

    def is_table_loaded(self, locator):
        table_loader = self.get_table_loader(locator)
        return not table_loader.is_visible()

    def get_table_loader(self, locator):
        return self.elementkeywords_management.get_element_by_auto_tag(locator).find_element_by_tag_name("core-loader")

    def get_table_header(self, locator):
        return self.get_table(locator).find_element_by_tag_name("thead")

    def get_table_body(self, locator):
        return self.get_table(locator).find_element_by_tag_name("tbody")

    def get_header_columns(self, locator):
        return self.get_table_header(locator).find_elements_by_tag_name("th")

    def get_header_texts(self, locator):
        header_cols = self.get_header_columns(locator)
        headers = []
        for header_col in header_cols:
            try:
                headers.append(header_col.get_textContent())
            except:
                headers.append("")
        return headers

    @keyword
    def get_table_rows(self, locator):
        return self.get_table_body(locator).find_elements_by_tag_name("tr")

    def get_cells_in_table_row(self, row):
        return row.find_elements_by_tag_name("td")

    @keyword
    def get_column_index(self, locator, column_title):
        """
        Get the index of column in table.
        :locator: locator of table
        :column_title: string of column title to get index
        :return: index of the column
        """
        headers = self.get_header_texts(locator)
        return headers.index(column_title)

    @keyword
    def get_row_by_column_cell(self, locator, column, value, is_index=False):
        """
        Get the row of table
        :locator: locator of table
        :column: string of column title or column index that contains value
        :value: string of cell's value
        :is_index: True if column is index, False if column is column title
        :return: row of value identified by column title
        """
        rows = self.get_table_rows(locator)
        if not is_index:
            column = self.get_column_index(locator, column)
        for row in rows:
            cells = self.get_cells_in_table_row(row)
            if cells[column].get_textContent() == value:
                return row
        message = "Not found the value '%s' in any row!" % value
        raise AssertionError(message)

    @keyword
    def get_all_rows_by_column(self, table_locator, column_name, is_index=False):
        list_data = []
        rows = self.get_table_rows(table_locator)
        if len(rows) == 0:
            mess = "Table is empty!"
            raise AssertionError(mess)
        if not is_index:
            column = self.get_column_index(table_locator, column_name)
        for row in rows:
            cells = self.get_cells_in_table_row(row)[column].text
            list_data.append(cells)
        return list_data

    @keyword
    def get_table_length(self, locator):
        rows = self.get_table_rows(locator)
        table_length = len(rows)
        return table_length

    @keyword
    def get_table_row(self, locator, value):
        rows = self.get_table_rows(locator)
        """
        Get a row from table
        :param locator: table locator
        :param row_values: list values of row <value1> <value2> e.g. 1/1/1 10 Enable. Or a Dictionary Values list from YAML
        :return: table row
        """
        for row in range(0, len(rows)):
            if value == rows[row].text:
                return value
        message = "Not found the value '%s' in any row!" % value
        raise AssertionError(message)

    @keyword
    def get_radio_on_row(self, locator, value):
        """
        Get all row of this locator
        :param locator: table locator
        :param value: row text contains radio button
        :return: True if radio button is selected and else
        """

        rows = self.get_table_rows(locator)
        for row in range(0, len(rows)):
            if rows[row].text == value:
                if rows[row].find_element_by_tag_name('td').find_element_by_tag_name('span').find_element_by_tag_name('input').is_selected():
                    return True
                else:
                    message = "Value not be selected" % value
                    raise AssertionError(message)
                    return False


    def _is_text_in_list(self, elements, *text):
        if len(text) > 1:
            checking_text = text
        else:
            checking_text = text[0]
        for t in filter(lambda x: x != "" and x is not None, checking_text):
            try:
                self.elementkeywords_management.get_element_contains_text_in_list(elements, t)
            except:
                message = "Not found the value '%s' in table!" % text
                raise AssertionError(message)
                return False
        return True

    @keyword
    def is_table_has_value(self, locator, column, value):
        """
        Check if table contains column's value
        :param locator: table locator
        :param column: column title (string)
        :param value: column value (string)
        :return: True if value is found other wise False
        """
        try:
            row = self.get_row_by_column_cell(locator, column, value)
            return not (row is None)
        except:
            return False

    @keyword
    def get_row_by_index(self, locator, index):
        return self.get_table_rows(locator)[index]

    @keyword
    def get_status_in_row(self, locator, index, value):
        rows = self.get_row_by_index(locator, index)
        fail_status = "Failed"
        complete_errors_status = "Completed with Errors"
        on_going_status = "On Going"
        if value in rows.text:
            return value
        elif fail_status in rows.text:
            return fail_status
        elif complete_errors_status in rows.text:
            return complete_errors_status
        return on_going_status

    @keyword
    def click_element(self, locator):
        return self.find_element(locator).js_click()

    @keyword
    def click_on_row(self, locator, column_title, value):
        self.get_row_by_column_cell(locator, column_title, value).click()

    @keyword
    def click_on_row_radio_button(self, locator, column_title, value):
        row = self.get_row_by_column_cell(locator, column_title, value)
        self.click_on_radio_button(row)

    def click_on_radio_button(self, element):
        self.get_radio_button(element).js_click()

    def get_radio_button(self, element):
        return element.find_element_by_tag_name("input")

    def get_link(self, element):
        return element.find_element_by_tag_name("a")

    @keyword
    def click_on_link(self, element):
        self.get_link(element).click()

    @keyword
    def is_table_has_text(self, locator, text):
        """
        The function help check search result in table
        :param locator: locator of table
        :param text: verify text
        :return: True if text contains in table otherwise False
        """
        self.wait_until_table_loaded(locator)
        table_data = self.get_table_body(locator)
        text_content = table_data.get_textContent()
        if text == text_content[0:12]:
            return True
        else:
            message = "Not found the value '%s' in table!" % text
            raise AssertionError(message)

    @keyword
    def is_table_contains_text(self, locator, text):
        """
        The function help check search result in table
        :param locator: locator of table
        :param text: verify text
        :return: True if text contains in table otherwise False
        """
        self.wait_until_table_loaded(locator)
        table_data = self.get_table_body(locator)
        text_content = table_data.get_textContent()
        if text in text_content:
            return True
        else:
            message = "Not found the value '%s' in table!" % text
            raise AssertionError(message)

    @keyword
    def table_should_be_empty(self, locator):
        table_data = self.get_table_body(locator)
        if len(table_data.text) == 0:
            return True
        message = "Table still has data"
        raise AssertionError(message)

    @keyword
    def table_should_be_none(self, locator):
        element = self.find_element(locator).find_elements_by_name("tbody")
        if len(element) > 0:
            mess = "Table %s is not empty" % locator
            raise AssertionError(mess)
        return


    @keyword
    def click_on_link_in_row(self, locator, column, value, is_index=False):
        """
        Click on link in a table row
        :locator: locator of table
        :column: string of column title or column index that contains value
        :value: string of cell's value
        :is_index: True if column is index, False if column is column title
        :return: row of value identified by column title
        """
        rows = self.get_table_rows(locator)
        if not is_index:
            column = self.get_column_index(locator, column)
        for row in rows:
            cells = self.get_cells_in_table_row(row)
            if cells[column].get_textContent() == value:
                return row.find_element_by_tag_name("a").js_click()
        message = "Not found the value '%s' in any row!" % value
        raise AssertionError(message)

    @keyword
    def get_all_data_of_table(self, locator):
        rows = self.get_table_body(locator).find_elements_by_tag_name("span")
        data = []
        for i in rows:
            data.append(i.text)
        return data

    @keyword
    def get_text_on_table_without_empty_text(self, locator):
        rows = self.get_table_body(locator).find_elements_by_tag_name("span")
        data = []
        for i in range(0, len(rows)):
            if rows[i].text != '':
                data.append(rows[i].text)
        return data


