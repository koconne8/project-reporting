from django.shortcuts import HttpResponse, render
from django.db import connection
import datetime
import json


def DistibutionHome(request):
    return render(request, 'distribution.html', {})

def GetEntities(request):
    # first check to make sure we have all we need
    # do we have a date range?
    if 'start_date' not in request.GET or request.GET['start_date'] == '':
        return HttpResponse('No Start Date Found')
    if 'end_date' not in request.GET or request.GET['end_date'] == '':
        return HttpResponse('No End Date Found')

    # do we have a type?
    if 'type' not in request.GET:
        return HttpResponse('No Type Found')

    # is it a valid type?
    if request.GET['type'] != 'project' and request.GET['type'] != 'programmer':
        return HttpResponse('No valid type found')

    # otherwise, let's grab the list of "type" based on the date range!
    # connect to the database
    cur = connection.cursor()

    if request.GET['type'] == 'project':
        query = "select distinct(projects.name), projects.id, CASE WHEN time_entries.spent_on >= '%(start)s' and time_entries.spent_on <= '%(end)s' THEN 2 ELSE 1 end AS t from projects inner join time_entries on time_entries.project_id = projects.id ORDER BY t desc, projects.name;" % {
            'start': request.GET['start_date'], 'end': request.GET['end_date']}
    if request.GET['type'] == 'programmer':
        query = "select distinct(users.id), users.firstname, users.lastname, max(CASE WHEN time_entries.spent_on >= '%(start)s' and time_entries.spent_on <= '%(end)s' THEN 2 ELSE 1 end) AS t from users inner join time_entries on time_entries.user_id = users.id GROUP BY users.id, users.firstname, users.lastname ORDER BY t desc, users.firstname;" % {
            'start': request.GET['start_date'], 'end': request.GET['end_date']}

    cur.execute(query)

    results = cur.fetchall()

    # construct our list
    list = []
    for result in results:
        new_result = {}

        if request.GET['type'] == 'project':
            new_result['name'] = result[0]
            new_result['id'] = result[1]
        if request.GET['type'] == 'programmer':
            new_result['name'] = result[1] + ' ' + result[2]
            new_result['id'] = result[0]
        list.append(new_result)

    context = {'entries': list}

    return HttpResponse(json.dumps(context))