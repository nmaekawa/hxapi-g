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

    slate_sheet_id = os.getenv('SLATE_SHEET_ID', None)
    if slate_sheet_id:
        # range for all info in the slate
        slate_rows = gsheets.get_range(
            slate_sheet_id,
            'A:AF',
        )
    else:
        print('missing SLATE_SHEET_ID')
        exit(1)

    #print('slate results have ({}) rows'.format(len(slate_rows)))
    #print('{}'.format(json.dumps(slate_rows, indent=4)))
    #print('{}'.format(json.dumps(slate_rows[0], indent=4)))

    slate_items = GSheets.map_rows_into_dict(
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
    intake_sheet_id = os.getenv('INTAKE_SHEET_ID', None)
    if intake_sheet_id:
        intake_assignment_rows = gsheets.get_range(
            intake_sheet_id,
            HXYDRA_INTAKE_ASSIGNMENT_HEADER_RANGE,
        )
    else:
        print('missing INTAKE_SHEET_ID')
        exit(1)

    intake = GSheets.map_rows_into_dict(HXYDRA_INTAKE_HEADER_MAP, intake_assignment_rows)

    print('INTAKE: {}'.format(json.dumps(intake, indent=4)))
    '''

    users_sheet_id = os.getenv('USERNAME_SHEET_ID', None)
    if not users_sheet_id:
        print('missing USERNAME_SHEET_ID')
        exit(1)

    users_row = gsheets.get_range(users_sheet_id, 'A:F')
    users_items = GSheets.map_rows_into_dict(
        HXYDRA_USERS_HEADER_MAP, users_row)

    print(json.dumps(users_items, indent=4))

    # range for usernames




