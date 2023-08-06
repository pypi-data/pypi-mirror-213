import json
import requests
from dws_merkle.common import get_version


class Base:

    def __init__(self, stage, username, key):

        self.__version__ = get_version()
        
        if stage == 'develop':
            self.headers = {"Authorization": username + "," + key}
            self.url = "https://test-api.dcentralab.com/"
        if stage == 'staging':
            self.headers = {"Authorization": username + "," + key}
            self.url = "https://staging.dcentralab.com/"
        if stage == 'main':
            self.headers = {"Authorization": username + "," + key}
            self.url = "https://api.dcentralab.com/"