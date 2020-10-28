from SeleniumLibrary.base import keyword, LibraryComponent
from SeleniumLibrary.keywords import WaitingKeywords
from .elementkeywords import ElementKeywords
import os, shutil, csv, string, time
from random import *
from netaddr import *
from randmac import RandMac
from .tablekeywords import TableKeywords

__version__ = '1.0.0'



class PCNKeywords(LibraryComponent):

    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)
        self.elementkeywords_management = ElementKeywords(ctx)
        self.waiting_management = WaitingKeywords(ctx)
        self.tablekeywords_management = TableKeywords(ctx)

    @keyword
    def compare_element_text_content(self, locator, value):
        element = self.find_element(locator)
        if element.get_textContent() == value:
            print("Content of text field" + locator + " is " + value)
            return element.get_textContent()
        else:
            return False

    @keyword
    def compare_element_value(self, locator, value):
        element = self.find_element(locator)
        if element.get_attribute('value') == value:
            return
        else:
            print(value)
            print(element.get_attribute('value'))
            mess = 'Current value is %s ' % element.get_attribute('value')
            raise AssertionError(mess)

    @keyword
    def split_text_to_list(self, text, character):
        return str(text).replace(" ", "").split(str(character))

    @keyword
    def get_multiple_params(*multiple_params):
        return list(multiple_params)

    @keyword
    def element_value_should_be(self, locator, expected_value):
        '''
        This function will replace for "Element Text Should Be" on edge browsers because text of some element contains space
        character so we cannot use "Element Text Should Be" function

        :param locator: element locator will be compared
        :param expected_value: value will be compared with text of element
        :return: True if element text is same with expected value
        '''
        element = self.find_element(locator)
        if element:
            if element.text.strip() == expected_value.strip():
                return True
            else:
                mess = 'Current value is %s ' % element.text
                raise AssertionError(mess)
        else:
            message = "%s not found" % locator
            raise AssertionError(message)

    @keyword
    def set_selectbox_value(self, locator, value):
        select_box = self.find_element(locator)
        options = select_box.find_elements_by_tag_name("option")
        for option in options:
            if option.get_textContent() == value:
                option.click()
                return
        message = "%s not found" % value
        raise AssertionError(message)

    @keyword
    def set_option(self, option_locator):
        options = self.find_element(option_locator)
        if None != options:
            options.click()
            return
        message = "Locator: %s not found" % option_locator
        raise AssertionError(message)

    @keyword
    def get_number_in_text(self, text):
        data = []
        for i in text:
            if i.isdigit():
                data.append(int(i))
                return data
        mess = "%s is not contain number" % text
        raise AssertionError(mess)

    @keyword
    def get_data_in_text(self, text):
        '''
        This function only use for: text
        :param text: "Text: data"
        :return:  list[data]
        '''
        data = []
        temp = str(text).split(": ")
        data.append(temp[1])
        return data

    @keyword
    def get_element_text_in_list(self, locator, value):
        elements = self.find_element(locator).find_elements_by_tag_name("li")
        for element in range(0, len(elements)):
            if elements[element].text == value:
                return elements[element].text
        mess = "%s not found value: " % value
        raise AssertionError(mess)

    @keyword
    def split_store_number(self, list):
        list_store = []
        for index in range(0, len(list)):
            a = list[index][1:5]
            list_store.append(a)
        return list_store

    @keyword
    def create_directory_by_path(self, path):
        if os.path.isdir(path):
            shutil.rmtree(path)
            os.makedirs(path)
        else:
            os.makedirs(path)
        return path

    @keyword
    def get_obj_attr_by_value(self, obj, value):
        null = None
        data = obj[0].get(value)
        return data

    def get_all_object_by_key_name(self, object, key_name):
        # get value by key in json file
        null = None
        list_data = []
        for obj in range(0, len(object)):
            value = object[obj].get(key_name)
            list_data.append(value)
        return list_data

    @keyword
    def generate_name(self):
        min_char = 8
        max_char = 12
        allchar = string.ascii_letters + string.digits
        name = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
        return name
    
    @keyword
    def remove_directory_by_path(self, path):
        if not os.path.isdir(path):
            mess = "Directory in '%s' not exists." % path
            raise AssertionError(mess)
        else:
            shutil.rmtree(path)
        return path

    @keyword
    def get_random_subnet(self, number_random, path):
        with open(path) as resultsFile:
            readFile = csv.reader(resultsFile)
            list_all_subnet = []
            for row in readFile:
                list_all_subnet.append(row[0])
            list_random_subnet = []
            for x in range(0, int(number_random)):
                subnet = choice(list_all_subnet)
                list_random_subnet.append(subnet)
            return list_random_subnet

    @keyword
    def get_rows_by_column_name(self, path, column_name):
        # this functions just apply to csv,excel...file
        with open(path) as f:
            reader = csv.reader(f)
            columns = next(reader)
            list_column = []
            for column in columns:
                list_column.append(column)
            for i in range(0, len(list_column)):
                if list_column[i] == column_name:
                    index = i
            list_all_data = []
            for row in reader:
                list_all_data.append(row[index])
        return list_all_data

    @keyword
    def compare_two_lists(self, list_1, list_2):
        if len(list_1) == 0 or len(list_2) == 0:
            mess = "List is empty"
            raise AssertionError(mess)
        for item in list_1:
            if item in list_2:
                continue
            else:
                mess = "Compare failed, that lists to diffirence!"
                raise AssertionError(mess)
        message = "Compare successfully!"
        print(message)

    @keyword
    def compare_exact_list(self, list_1, list_2):
        '''
        Documentation: Sort two lists > compare that
        :param list_1:
        :param list_2:
        :return:
        '''
        print(list_1)
        print(list_2)
        temp_1 = self.sort_list_data(list_1)
        temp_2 = self.sort_list_data(list_2)
        if len(temp_1) == 0 or len(temp_2) == 0:
            mess = "Length of list must be > 0"
            raise AssertionError(mess)
        elif len(temp_1) != len(temp_2):
            mess = "Length of 2 lists is difference!"
            raise AssertionError(mess)
        else:
            for i in range(0, len(temp_1)):
                if temp_1[i].strip() == temp_2[i].strip():
                    continue
                else:
                    mess = "Elements in the 2 lists are not the same, compare failed!"
                    raise AssertionError(mess)
        print("Compare successfully!")
        return

    @keyword
    def compare_list(self, list_1, list_2):
        print(list_1)
        print(list_2)
        temp_1 = self.sort_list_data(list_1)
        temp_2 = self.sort_list_data(list_2)
        if len(temp_1) != len(temp_2):
            mess = "Length of 2 lists is difference!"
            raise AssertionError(mess)
        else:
            for i in range(0, len(temp_1)):
                if temp_1[i] == temp_2[i]:
                    continue
                else:
                    mess = "Elements in the 2 lists are not the same, compare failed!"
                    raise AssertionError(mess)
        print("Compare successfully!")
        return

    @keyword
    def get_file_in_directory(self, path):
        dirs = os.listdir(path)
        file = dirs[0]
        return file

    @keyword
    def wait_until_file_is_downloaded(self, path, setTime=None):
        '''
        :param path: folder directory will be contains download file
        :param setTime: timeout of function. Out that time, function will be break. unit: /seconds
        :return: check file is downloaded succeed or failed
        '''
        if setTime == None:
            timeout = time.time() + 30
        else:
            timeout = time.time() + int(setTime)
        dirs = os.listdir(path)
        if len(dirs) == 1:
            for i in dirs:
                a = i.split(".")
            if a[len(a) - 1] == 'csv':
                print(dirs[0])
                return True
            else:
                while a[len(a) - 1] != 'csv':
                    dirs = os.listdir(path)
                    if time.time() > timeout:
                        mess = "Download is break down!"
                        raise AssertionError(mess)
                        return
                    for i in dirs:
                        a = i.split(".")
                    if a[len(a) - 1] == 'csv':
                        print(dirs[0])
                        return True
                    else:
                        continue
        while len(dirs) != 1:
            dirs = os.listdir(path)
            if time.time() > timeout:
                mess = "Too long to respond, download failed!"
                raise AssertionError(mess)
                return
            if len(dirs) == 1:
                for i in dirs:
                    a = i.split(".")
                if a[len(a) - 1] == 'csv':
                    print(dirs[0])
                    return True
                else:
                    while a[len(a) - 1] != 'csv':
                        dirs = os.listdir(path)
                        if time.time() > timeout:
                            mess = "Download is break down!"
                            raise AssertionError(mess)
                            return
                        for i in dirs:
                            a = i.split(".")
                        if a[len(a) - 1] == 'csv':
                            print(dirs[0])
                            return True
                        else:
                            continue

    @keyword
    def get_all_data_in_table_by_selectbox(self, locator, table_locator, column_name):
        '''

        :param locator: this is selectbox locator. Every table will be have next,prev,up button and select box used to paging
        :param table_locator: table locator
        :param column_name: get data of this column
        :return: list contains all data on this table include data is paging
        '''
        list_data = []
        list_all_data = []
        list_length = self.elementkeywords_management.get_length_selectbox(locator)
        for i in range(0, list_length):
            index = i + 1
            self.set_selectbox_value(locator, str(index))
            temp = self.tablekeywords_management.get_all_rows_by_column(table_locator, column_name, is_index=False)
            list_data.append(temp)
        for i in list_data:
            for value in i:
                list_all_data.append(value)
        return list_all_data

    @keyword
    def get_all_data_in_table_by_button(self, locator, table_locator, column_name):
        '''

        :param locator: this is button next locator. Every table will be have next,prev,up button and select box used to paging
        :param table_locator: table locator
        :param column_name: get data of this column
        :return: list contains all data on this table include data is paging
        '''
        list_data = []
        list_all_data = []
        elements = self.find_element(locator)
        data = self.tablekeywords_management.get_all_rows_by_column(table_locator, column_name, is_index=False)
        list_data.append(data)
        while True:
            if elements.is_enabled() == True:
                self.tablekeywords_management.click_element(locator)
                temp = self.tablekeywords_management.get_all_rows_by_column(table_locator, column_name, is_index=False)
                list_data.append(temp)
                continue
            else:
                break
        for i in list_data:
            for value in i:
                list_all_data.append(value)
        return list_all_data

    @keyword
    def get_all_data_in_table(self, locator, table_locator, column_name):
        '''

        :param locator: this is selectbox locator. Every table will be have next,prev,up button and select box used to paging
        :param table_locator: table locator
        :param column_name: get data of this column
        :return: list contains all data on this table include data is paging
        '''
        list_data = []
        list_all_data = []
        data = self.tablekeywords_management.get_all_rows_by_column(table_locator, column_name, is_index=False)
        list_data.append(data)
        for i in list_data:
            for value in i:
                list_all_data.append(value)
        return list_all_data

    @keyword
    def convert_two_list_object_to_list(self, list_1, list_2):
        list_data = []
        for item in list_1:
            for data in item:
                list_data.append(data)
        return list_data

    @keyword
    def get_header_in_file(self, path):
        with open(path, 'rt')as f:
            reader = csv.reader(f)
            columns = next(reader)
            if len(columns) == 0:
                mess = "List is empty"
                raise AssertionError(mess)
            header = []
            for col in columns:
                header.append(col)
            return header

    @keyword
    def get_data_by_row(self, path, position=None):
        with open(path, 'rt')as f:
            print(path)
            reader = csv.reader(f)
            columns = next(reader)
            header = []
            for col in columns:
                header.append(col)
            row_data = []
            list_data = []
            for i in reader:
                list_data.append(i)
            if len(list_data) == 0:
                mess = "List is empty"
                raise AssertionError(mess)
            if position == None:
                for row in list_data:
                    for data in row:
                        row_data.append(data)
                return row_data
            else:
                row_data.append(list_data[position])
            data = []
            for row in row_data:
                for i in row:
                    data.append(i)
            return data


    @keyword
    def export_element_locator(self, locator, count):
        list_data = []
        if count == 0:
            mess = "Array will be return empty!!!"
            raise AssertionError(mess)
        for i in range(0, int(count)):
            temp = locator.replace("']", str(i) + "']")
            list_data.append(temp)
        return list_data

    @keyword
    def check_value_in_list(self, list_value, value):
        if len(list_value) == 0:
            mess = "List is empty!"
            raise AssertionError(mess)
        elif value == None:
            mess = "Value cannot be 'None'!"
            raise AssertionError(mess)
        for i in list_value:
            if value == i:
                return True
            else:
                mess = "Value haven't exist in that list"
                raise AssertionError(mess)

    # @keyword
    # def wait_load_status(self, locator, timeout=None, error=None):
    #     element = self.find_element(locator)
    #     while True:
    #         text = element.text
    #         if text != "On Going" and text != "None" and text != "":
    #             return
    #             print(text)
    #
    #         # self.waiting_management._wait_until(
    #         #     lambda: element.text != "On Going" and element.text != "None" and element.text != "",
    #         #     "Element '%s' still in loading over <TIMEOUT>." % locator,
    #         #     timeout,
    #         #     error
    #         # )
    #     return

    @keyword
    def wait_load_status(self, locator, setTime=None):
        if setTime == None:
            timeout = time.time() + 0
        else:
            timeout = time.time() + int(setTime)
        element = self.find_element(locator)
        while True:
            text = element.text
            if time.time() > timeout:
                mess = "Request timeout"
                raise AssertionError(mess)
            if text != "On Going" and text != "None" and text != "":
                return text

    @keyword
    def wait_until_element_text_is_exactly(self, locator, value, timeout=100, error=None):
        element = self.find_element(locator)
        self.waiting_management._wait_until(
            lambda: element.text == value,
            ("The text of element '%s' should have been '%s' "
               "but it was '%s'." % (locator, value, element.text)),
            timeout,
            error
        )
        print(element.text)
        return element.text

    @keyword
    def wait_until_element_value_is_exactly(self, locator, value, timeout=100, error=None):
        element = self.find_element(locator)
        self.waiting_management._wait_until(
            lambda: element.get_attribute('value') == value,
            ("The text of element '%s' should have been '%s' "
             "but it was '%s'." % (locator, value, element.text)),
            timeout,
            error
        )
        print(element.text)
        return element.text


    @keyword
    def get_table_data_by_keyword(self, locator, keyword):
        c = "\n"
        rows = self.tablekeywords_management.get_table_rows(locator)
        data = []
        for i in range(0, len(rows)):
            if keyword in rows[i].text:
                temp = rows[i].text.replace(c, " ")
                data.append(temp)
        return data

    @keyword
    def get_table_data_by_status(self, locator, status):
        c = "\n"
        rows = self.tablekeywords_management.get_table_rows(locator)
        data = []
        for i in range(0, len(rows)):
            if status in rows[i].text:
                temp = rows[i].text.split(c)
                for item in temp:
                    data.append(item)
        return data

    @keyword
    def get_table_data_by_status_of_column(self, locator, column, status, is_index=False):
        c = "\n"
        rows = self.tablekeywords_management.get_table_rows(locator)
        if not is_index:
            column = self.tablekeywords_management.get_column_index(locator, column)
        data = []
        for row in rows:
            cells = self.tablekeywords_management.get_cells_in_table_row(row)
            if cells[column].text == status:
                temp = rows[row].text.split(c)
                for item in temp:
                    data.append(item)
        return data
    
    @keyword
    def remove_space_of_text(self, text):
        return str(text).strip()

    @keyword
    def sort_list_data(self, list_data):
        '''
        convert all elements in list to string(follow alphabet)
        :param list_data: list data contains all elements
        :return: list has been sort successfully
        '''
        data = []
        for i in list_data:
            data.append(str(i))
        return sorted(data)

    @keyword
    def reserve_list(self, *list):
        if len(list) == 0:
            mess = "Length is 0"
            raise AssertionError(mess)
        data = []
        for i in list:
            data.append(i)
        return data.reverse()

    @keyword
    def export_dhcp_range(self, ip_start, dhcp_range, status):
        '''
        :param ip_start: start range. ex: 241.56.0.6
        :param dhcp_range: size of dhcp range. ex: 4
        :param status: status of dhcp range. ex: DHCP, DHCP Range, DHCP Scope....
        :return: ["241.56.0.6", "DHCP", "241.56.0.7", "DHCP", "241.56.0.8", "DHCP", "241.56.0.9", "DHCP"]
        '''
        temp = ip_start.split(".")
        data = []
        for i in temp:
            a = int(temp[len(temp) - 1])
        prefix = temp[0] + "." + temp[1] + "." + temp[2] + "."
        for i in range(0, int(dhcp_range)):
            data.append(prefix + str(a + i))
            data.append(status)
        return data

    @keyword
    def generate_dhcp_range(self, first, last, status):
        ip_list = list(iter_iprange(str(first), str(last)))
        temp = []
        data = []
        for i in ip_list:
            temp.append(str(i))
        for i in temp:
            data.append(i)
            data.append(str(status))
        return data

    @keyword
    def generate_mac_address(self, numbers_of_mac_addr):
        temp = []
        mac_addr = []
        for i in range(0, numbers_of_mac_addr):
            temp.append(RandMac("00:00:00:00:00:00", True))
        for i in temp:
            mac_addr.append(i.mac)
        return mac_addr

    @keyword
    def load_selectbox_value_by_next_button(self, selectbox_locator, next_button_locator, value):
        select_box = self.find_element(selectbox_locator)
        options = select_box.find_elements_by_tag_name("option")
        while True:
            for i in options:
                if i.text != value:
                    self.tablekeywords_management.click_element(next_button_locator)
                    continue
                else:
                    return
                mess = "%s not found" %value
                raise AssertionError(mess)
            return

    @keyword
    def enable_download_in_headless_chrome(self, driver, download_dir):
        # add missing support for chrome "send_command"  to selenium webdriver
        driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
        command_result = driver.execute("send_command", params)


