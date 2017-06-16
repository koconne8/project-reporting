from django.db import connection
from django.shortcuts import render, HttpResponse
import datetime
from pr.settings.base import LOGGING_CATEGORY_NAME


def rates_home(request):
    # connect to our database
    cur = connection.cursor()

    cur.execute("SELECT charge_rate_id, start_date, end_date, category, rate, internal, cores_display"
                " FROM charge_rates"
                " ORDER BY start_date, internal desc, cores_display;")

    rates = cur.fetchall()

    rate_list = []
    group = ''
    dark = False
    for rate in rates:
        if rate[1] != group:
            group = rate[1]
            dark = not dark

        rate_list.append({
            'id': rate[0],
            'start_date': rate[1].strftime('%Y-%m-%d'),
            'end_date': rate[2].strftime('%Y-%m-%d'),
            'category': rate[3],
            'rate': rate[4],
            'internal': rate[5],
            'cores_display': rate[6],
            'dark': dark
        })

    # get a list of categories that this could be for
    cur.execute("select possible_values from custom_fields "
                "where lower(name) = lower(%s);", [LOGGING_CATEGORY_NAME])

    categories = cur.fetchall()
    category_list = []
    for category in categories[0][0].split('\n')[1:]:
        if category[2:] != '':
            category_list.append(category[2:])


    # compute next fiscal year ranges
    add_year = 0
    if datetime.datetime.today().month >= 7:
        add_year = 1
    next_fiscal_start = datetime.datetime(datetime.datetime.today().year + add_year, 7, 1)
    next_fiscal_end = datetime.datetime(datetime.datetime.today().year + add_year + 1, 6, 30)

    return render(request, 'rates.html', {'rates': rate_list, 'categories': category_list,
                                          'next_fiscal_start': next_fiscal_start,
                                          'next_fiscal_end': next_fiscal_end})


def save_rate(request):
    # connect to our database
    cur = connection.cursor()

    cur.execute("UPDATE charge_rates "
                "SET category = %s, "
                "cores_display = %s "
                "WHERE charge_rate_id = %s;", [request.GET['category'], request.GET['cores_display'], int(request.GET['id'])])

    return HttpResponse(200)


def save_start_date(request):
    ids = request.GET.getlist('ids[]')
    id_list = []
    for id in ids:
        id_list.append(int(id))

    # connect to our database
    cur = connection.cursor()

    cur.execute("UPDATE charge_rates "
                "SET start_date = %s::date "
                "WHERE charge_rate_id = ANY(%s);",
                [request.GET['start_date'], id_list])

    return HttpResponse(200)


def save_end_date(request):
    ids = request.GET.getlist('ids[]')
    id_list = []
    for id in ids:
        id_list.append(int(id))

    # connect to our database
    cur = connection.cursor()

    cur.execute("UPDATE charge_rates "
                "SET end_date = %s::date "
                "WHERE charge_rate_id = ANY(%s);",
                [request.GET['end_date'], id_list])

    return HttpResponse(200)


def save_rates(request):
    ids = request.GET.getlist('ids[]')
    id_list = []
    for id in ids:
        id_list.append(int(id))

    # connect to our database
    cur = connection.cursor()

    cur.execute("UPDATE charge_rates "
                "SET rate = %s "
                "WHERE charge_rate_id = ANY(%s);",
                [request.GET['rate'], id_list])

    return HttpResponse(200)


def delete_rates(request):
    ids = request.GET.getlist('ids[]')
    id_list = []
    for id in ids:
        id_list.append(int(id))

    # connect to our database
    cur = connection.cursor()

    cur.execute("DELETE FROM charge_rates "
                "WHERE charge_rate_id = ANY(%s);",
                [id_list])

    return HttpResponse(200)


def add_single_category(request):
    # connect to our database
    cur = connection.cursor()

    # get the name of the category selected
    category = request.GET['category']

    cur.execute("INSERT INTO charge_rates "
                "(start_date, end_date, category, rate, cores_display) "
                "VALUES "
                "(%s, %s, %s, %s, %s);", [request.GET['start_date'],
                                          request.GET['end_date'],
                                          category,
                                          request.GET['rate'],
                                          category
                                          ])

    return HttpResponse(200)

def add_rates(request):
    # connect to our database
    cur = connection.cursor()

    # get a list of categories that this could be for
    cur.execute("select possible_values from custom_fields "
                "where lower(name) = lower(%s);", [LOGGING_CATEGORY_NAME])

    categories = cur.fetchall()
    category_list = []
    for category in categories[0][0].split('\n')[1:]:
        if category[2:] != '':
            category_list.append(category[2:])

    for category in category_list:
        cur.execute("INSERT INTO charge_rates "
                    "(start_date, end_date, category, rate, cores_display) "
                    "VALUES "
                    "(%s, %s, %s, %s, %s);", [request.GET['start_date'],
                                              request.GET['end_date'],
                                              category,
                                              request.GET['rate'],
                                              category
                                              ])

    return HttpResponse(200)
