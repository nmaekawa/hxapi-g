# -*- coding: utf-8 -*-

import logging
import os
import re

from gsheets import GSheets


HXYDRA_SLATE_PROJECT_NICKNAME_RANGE = 'D:D'
HXYDRA_INTAKE_ASSIGNMENT_HEADER_RANGE = 'A12:H'

HXYDRA_INTAKE_HEADER_MAP = {
    'name': 'assignment_name',
    'instructions': 'instructions',
    'date': 'release_date',
    'link': 'link',
    'notes': 'extra_info',
    'type': 'type',
}
# unpack dict keys into a list; python>=3.5
HXYDRA_INTAKE_HEADER_KEYS = [*HXYDRA_INTAKE_HEADER_MAP]


logger = logging.getLogger(__name__)


class HxapiGSheets(object):

    def __init__(self, gsheets):
        self.gs = gsheets


    def get_nicknames(self, sheet_id):
        nickname_ranges = self.gs.get_range(
            sheet_id,
            HXYDRA_SLATE_PROJECT_NICKNAME_RANGE,
        )

        nicknames = []
        items = nickname_ranges
        for item in items:
            nick = item[0].strip()
            if nick \
               and nick not in ['TBD', 'Project Nickname'] \
               and nick not in nicknames:
                nicknames.append(nick)

        nicknames.sort()
        return nicknames


    def parse_intake_assignment_rows(self, intake_rows):
        # map required headers to known strings
        headers = []
        intake_headers = intake_rows[0]
        for header in intake_headers:
            found = False
            for h_key in HXYDRA_INTAKE_HEADER_KEYS:
                if h_key in header.lower():
                    headers.append(HXYDRA_INTAKE_HEADER_MAP[h_key])
                    found = True
                    break
            if not found:
                # remove non-work chars
                clean_header = re.sub(r'\W', '_', header.lower())
                headers.append(clean_header)

        assignment_list = []

        for row in intake_rows[1:]:  # skip row of headers
            assignment = {k: v for k,v in zip(headers, row)}
            assignment_list.append(assignment)

        return assignment_list



if __name__ == '__main__':
    """ main() works as usage example and live test.

    requires environment variables:
        GOOGLE_APPLICATION_CREDENTIALS: path to json key file
        SLATE_SHEET_ID: spreadsheet id
        INTAKE_SHEET_ID: spreadsheet id
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
    hsheets = HxapiGSheets(gsheets)

    slate_sheet_id = os.getenv('SLATE_SHEET_ID', None)
    if slate_sheet_id:
        nicknames = hsheets.get_nicknames(slate_sheet_id)
    else:
        print('missing SLATE_SHEET_ID')
        exit(1)

    print('NICKNAMES({}): {}'.format(
        len(nicknames), nicknames
    ))

    intake_sheet_id = os.getenv('INTAKE_SHEET_ID', None)
    if intake_sheet_id:
        intake_assignment_rows = gsheets.get_range(
            intake_sheet_id,
            HXYDRA_INTAKE_ASSIGNMENT_HEADER_RANGE,
        )
    else:
        print('missing INTAKE_SHEET_ID')
        exit(1)

    intake = hsheets.parse_intake_assignment_rows(intake_assignment_rows)
    print('INTAKE: {}'.format(intake))






