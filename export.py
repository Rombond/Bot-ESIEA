import datetime

from request import Request
from tokenClass import Token


class Export(Request, Token):

    def __init__(self, token):
        super().__init__(token)

    async def getCalendarDaily(self):
        now = datetime.datetime.now()
        day = await Request.get(self, function='core_calendar_get_calendar_day_view', year=now.year, month=now.month, day=now.day)

        data = []

        for events in day['events']:
            if events['modulename'] == 'attendance':
                splited = events['formattedtime'].split(':')
                data.append(
                    [
                        events['course']['fullname'],
                        splited[1][::-1][0:2][::-1] + ':' + splited[2][0:2],
                        splited[2][::-1][0:2][::-1] + ':' + splited[3][0:2],
                        events['url'],
                    ]
                )
        return data
