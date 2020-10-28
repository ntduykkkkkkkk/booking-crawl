import json
import requests
import urllib3
from SeleniumLibrary.base import keyword, LibraryComponent
from robot.libraries.BuiltIn import BuiltIn

from Libs.Share.Actions import Main as CommonFunction

__version__ = '1.0.0'


class Main(LibraryComponent):

    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)

    @keyword
    def get_data(self):
        return CommonFunction.get_setup_data(self)

    @keyword
    def parse_url(self):
        return self.get_data().get(BuiltIn().get_variable_value("${RESOURCE}")).get('url')

    @keyword
    def query_by_keyword(self, query_string):
        headers = {
            "Content-Type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
        }
        urllib3.disable_warnings()
        response = requests.get(self.parse_url() + "/v4/search/stories?query="+query_string+"&fields=stories%28id%2Ctitle%2CvoteCount%2CreadCount%2CcommentCount%2Cdescription%2Ccompleted%2Cmature%2Ccover%2Curl%2CisPaywalled%2Cuser%28name%29%2CnumParts%2ClastPublishedPart%28createDate%29%2Cpromoted%2Csponsor%28name%2Cavatar%29%2Ctags%2Ctracking%28clickUrl%2CimpressionUrl%2CthirdParty%28impressionUrls%2CclickUrls%29%29%2Ccontest%28endDate%2CctaLabel%2CctaURL%29%29%2Ctotal%2Ctags%2Cnexturl&limit=15&offset=15",
                                headers=headers, verify=False)
        print(response)
        return json.loads(response.content.decode("utf-8"))

    @keyword
    def query_story_by_id(self, id):
        headers = {
            "Content-Type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
        }
        urllib3.disable_warnings()
        response = requests.get(self.parse_url() + "v3/stories/" + id,headers=headers, verify=False)
        print(response)
        return json.loads(response.content.decode("utf-8"))