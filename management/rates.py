from django.db import connection
from django.shortcuts import render
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
                "where name = %s;", [LOGGING_CATEGORY_NAME])

    categories = cur.fetchall()
    category_list = []
    for category in categories[0][0].split('\n')[1:]:
        if category[2:] != '':
            category_list.append(category[2:])

    return render(request, 'rates.html', {'rates': rate_list, 'categories': category_list})

