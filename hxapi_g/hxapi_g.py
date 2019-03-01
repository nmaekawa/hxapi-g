# -*- coding: utf-8 -*-

from itertools import zip_longest
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


HXYDRA_SLATE_HEADER_MAP = {
    'launch date': 'launch_date',
    'end date': 'end_date',
    'project nickname': 'course_nickname',
    'project title': 'course_title',
    'project lead': 'project_lead',
    'other team members': 'other_team_members',
    'duration _wks': 'duration_in_weeks',
    'platform': 'platform',
    'common project name': 'course_group_name',
    'approximate course id for courses on edx.org only': 'context_id',
    'public course url': 'public_edx_url',
}
HXYDRA_USERS_HEADER_MAP = {
    'row': 'row',
}


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


    def map_rows_into_dict(self, item_keys_map, input_rows):
        # translate headers to known strings
        # and map each row from input_rows into a list of dicts
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
                # remove non-work chars
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
        SLATE_SHEET_ID: spreadsheet id
        INTAKE_SHEET_ID: spreadsheet id
    """
    import json

    credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', None)
    if credentials_path:
        credentials = GSheets.get_credentials(credentials_path)
        if credentials is None:
            print('no credentials; failing...')
            exit(1)
    else:
        print('missing GOOGLE_APPLICATION_CREDENTIALS')
        exit(1)

    #print(
    #    'project_id: {}; scopes: {}, token: {}'.format(
    #        credentials.project_id,
    #        credentials.scopes,
    #        credentials.token,
    #    )
    #)

    gsheets = GSheets(credentials)
    hsheets = HxapiGSheets(gsheets)

    slate_sheet_id = os.getenv('SLATE_SHEET_ID', None)
    if slate_sheet_id:
        nicknames = hsheets.get_nicknames(slate_sheet_id)
    else:
        print('missing SLATE_SHEET_ID')
        exit(1)


    # range for all info in the slate
    slate_rows = gsheets.get_range(
        slate_sheet_id,
        'A:AF',
    )
    #print('slate results have ({}) rows'.format(len(slate_rows)))
    #print('{}'.format(json.dumps(slate_rows, indent=4)))
    #print('{}'.format(json.dumps(slate_rows[0], indent=4)))

    slate_items = hsheets.map_rows_into_dict(
        HXYDRA_SLATE_HEADER_MAP,
        slate_rows,
    )

    # cleanup a little
    for item in slate_items:
        nickname = item['course_nickname'].lower()
        course_group = nickname.split('_')[0]
        item['course_nickname'] = nickname
        item['course_group'] = course_group

    print('{}'.format(json.dumps(slate_items, indent=4)))


    '''
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

    intake = hsheets.map_rows_into_dict(HXYDRA_INTAKE_HEADER_MAP, intake_assignment_rows)

    print('INTAKE: {}'.format(json.dumps(intake, indent=4)))
    '''

    users_sheet_id = os.getenv('USERNAME_SHEET_ID', None)
    if not users_sheet_id:
        print('missing USERNAME_SHEET_ID')
        exit(1)

    users_row = gsheets.get_range(users_sheet_id, 'A:F')
    users_items = hsheets.map_rows_into_dict(
        HXYDRA_USERS_HEADER_MAP, users_row)

    #print(json.dumps(users_items, indent=4))

    # range for usernames




