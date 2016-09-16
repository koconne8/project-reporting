"""pr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from management.planning import Home as PlanningHome, GetAllDevAssignments, GetAssignments, GetPlanningProjection, \
    DeveloperAssignments, Deactivate, Activate, UpdateSupervisor, RemoveAssignment, AddAssignment

from management.home import Home, GetEntries, GetDistribution
from management.time_entries import EntriesHome, GetDateRange, GetProjectActivities, UpdateEntries, DeleteEntry
from management.calendar_view import CalendarHome, UpdateEntryData, CopyEntry
from management.distribution import DistibutionHome, GetEntities
from management.report_generation import ReportGeneratorHome, GenerateExternalReport, GenerateInternalReport, GenerateCSRReport, MissingHours
from management.reports import WeeklyReportFromUrl

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # ------------- For Everyone ----------------#
    # Home Page
    url(r'^home/$', Home, name='home'),
    url(r'^get_entries/$', GetEntries, name="get_entries"),
    url(r'^get_distribution/$', GetDistribution, name="get_distribution"),

    # Time Entries (row-by-row)
    url(r'^time_entries/$', EntriesHome, name="time_entries"),
    url(r'^get_dates/$', GetDateRange, name='get_dates'),
    url(r'^get_activities/$', GetProjectActivities, name="get_activities"),
    url(r'^update_entries/$', UpdateEntries, name="update_entries"),
    url(r'^del_entry/$', DeleteEntry, name='del_entry'),

    # Calendar View
    url(r'^calendar/$', CalendarHome, name="calendar"),
    url(r'^update_entry_data/$', UpdateEntryData, name="update_entry_data"),
    url(r'^copy_entry/$', CopyEntry, name="copy_entry_data"),

    # Time Distribution View
    url(r'^distribution/$', DistibutionHome, name="distribution"),
    url(r'^get_entities/$', GetEntities, name="get_entities"),





    #------------- Marcy's Report Generator for CORES -----------#
    url(r'^report_generator/$', ReportGeneratorHome, name='report_generator'),
    url(r'^generate_internal_report/$', GenerateInternalReport, name="report"),
    url(r'^generate_external_report/$', GenerateExternalReport, name="report_external"),
    url(r'^generate_csr_report/$', GenerateCSRReport, name="report_external"),
    url(r'^missing_hours/$', MissingHours, name="unassigned_hours"),



    #------------- MANAGERS ONLY ----------------#

    # Project Planning
    url(r'^planning/$', PlanningHome, name='planning_home'),
    url(r'^get_all_dev_assignments/$', GetAllDevAssignments, name='get_all_dev_assignments'),
    url(r'^get_assignments/$', GetAssignments, name='get_assignments'),
    url(r'^get_planning_projection$', GetPlanningProjection, name='getProjections'),
    url(r'^developer_assignments/$', DeveloperAssignments, name='dev_assignments'),
    url(r'^deactivate_developer/$', Deactivate, name='deactivate'),
    url(r'^activate_developer/$', Activate, name='activate'),
    url(r'^update_supervisor/$', UpdateSupervisor, name='update_supervisor'),
    url(r'^remove_project_distribution_entry/$', RemoveAssignment, name='remove_assignment'),
    url(r'^add_developer/$', AddAssignment, name='add_developer'),

    # Weekly Report Generator (callable via the following URL):
    url(r'^weekly_report/$', WeeklyReportFromUrl, name='weekly_report'),

]
