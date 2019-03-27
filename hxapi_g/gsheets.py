# -*- coding: utf-8 -*-

from itertools import zip_longest
import logging
import re
import os

from googleapiclient import discovery
import google.auth
from google.oauth2 import service_account


GSHEETS_API_VERSION = os.getenv('GOOGLEAPI_VERSION_SHEETS', 'v4')
GSHEETS_SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
GSHEETS_DOCLINK_REGEX = re.compile(r'https://docs.google.com/spreadsheets/d/(\w+)/')


class GSheets(object):

    def __init__(self, credentials, version=GSHEETS_API_VERSION):
        self.version = version
        self.creds = credentials

        # TODO: find docs on exceptions to handle them...
        self.service = self.get_service()


    @classmethod
    def get_credentials(cls, credentials_path):
        """ read google creds from file.

        throws FileNotFoundError if credentials_path not readable
        """
        credentials = service_account.Credentials \
                .from_service_account_file(
                    credentials_path, scopes=GSHEETS_SCOPES
                )
        return credentials


    def get_service(self):
        service = discovery.build(
            'sheets',
            self.version,
            cache_discovery=False,
            credentials=self.creds
        )
        return service


    def get_range(
        self, spreadsheet_id, range_txt):

        request = self.service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range_txt,
        ).execute()

        return request.get('values', [])


    def get_sheets(
        self, spreadsheet_id):

        request = self.service.spreadsheets().get(
            spreadsheetId=spreadsheet_id
        ).execute()

        return request.get('sheets', [])


    @classmethod
    def find_id_from_link(cls, spreadsheet_link):
        matches = GSHEETS_DOCLINK_REGEX.match(spreadsheet_link)
        if matches:
            return matches.group(1)
        else:
            return None


    @classmethod
    def map_rows_into_dict(self, item_keys_map, input_rows):
        """turn input_rows into list of dicts with item_keys_map as keys.

        translates input headers to known strings
        map each row in input_rows into dict, using translated headers as keys
        result dict contains all keys in input_rows, translated or not
        """
        key_headers = []
        input_headers = input_rows[0]
        for ih in input_headers:
            found = False
            for h_key in item_keys_map:
                if h_key == ih.lower():
                    key_headers.append(item_keys_map[h_key])
                    found = True
                    break
            if not found:  # extra header, adding just in case
                # remove non-word chars
                clean_header = re.sub(r'\W', '_', ih.lower())
                key_headers.append(clean_header)

        item_list = []

        for row in input_rows[1:]:  # skip row of headers
            item = {k: v for k,v in zip_longest(key_headers, row)}
            item_list.append(item)

        return item_list


if __name__ == '__main__':
    """ main() works as usage example and live test.

    requires environment variables:
        GOOGLE_APPLICATION_CREDENTIALS: path to json key file
        SPREADSHEET_ID: spreadsheet id
        SPREADSHEET_RANGE: spreadsheet range, e.g. "D:D"
        SPREADSHEET_LINK: url for a spreadsheet
    """

    credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', None)
    if credentials_path:
        credentials = GSheets.get_credentials(credentials_path)
        if credentials is None:
            print('no credentials; failing...')
            exit(1)
    else:
        print('missing GOOGLE_APPLICATION_CREDENTIALS')
        exit(1)

    print(
        'project_id: {}; scopes: {}, token: {}'.format(
            credentials.project_id,
            credentials.scopes,
            credentials.token,
        )
    )

    gsheets = GSheets(credentials)

    sheet_id = os.getenv('SPREADSHEET_ID', None)
    if sheet_id:
        sheets = gsheets.get_sheets(sheet_id)
        print('sheets: {}'.format(sheets))
        print('DIR sheets: {}'.format(dir(sheets[0])))
    else:
        print('missing SPREADSHEET_ID')
        exit(1)

    sheet_range = os.getenv('SPREADSHEET_RANGE', None)
    if sheet_range:
        spreadsheet_rows = gsheets.get_range(sheet_id, sheet_range)
        print('range: {}'.format(spreadsheet_rows))
    else:
        print('missing SPREADSHEET_RANGE')
        exit(1)

    sheet_link = os.getenv('SPREADSHEET_LINK', None)
    if sheet_link:
        sid = GSheets.find_id_from_link(sheet_link)
        print('id({}) from link({})'.format(sid, sheet_link))
    else:
        print('missing SPREADSHEET_LINK')
        exit(1)

    exit(0)





