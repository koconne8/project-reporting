#!/usr/bin/python

'''
This file is used to define the cost of each Service Description.
'''

# Constants define how much each service costs:
# INTERNAL
COMP_SCI = 81
GIS = 56
HPC = 56
OUTREACH = 0
PROGRAMMING = 60

# EXTERNAL
EX_COMP_SCI = 125
EX_GIS = 100
EX_HPC = 125
EX_OUTREACH = 0
EX_PROGRAMMING = 90


class Service:
    def __init__(self, cores='', redmine='', cost=0):
        self.cores_name = cores
        self.redmine_name = redmine
        self.cost = cost


class ServiceCost:
    def __init__(self):
        self.services = []

        comp_sci = Service('Computational Scientist Services', 'Computational Scientist (internal)', COMP_SCI)
        gis = Service('GIS', 'GIS Support (internal)', GIS)
        vis = Service('Visualization', 'Visualization (internal)', GIS)
        hpc = Service('HPC Services', 'HPC Engineer (internal)', HPC)
        programming = Service('Programming', 'Programming (internal)', PROGRAMMING)

        comp_sci_ex = Service('Computational Scientist Services', 'Computational Scientist (external)', EX_COMP_SCI)
        gis_ex = Service('GIS', 'GIS Support (external)', EX_GIS)
        vis_ex = Service('Visualization', 'Visualization (external)', EX_GIS)
        hpc_ex = Service('HPC Services', 'HPC Engineer (external)', EX_HPC)
        programming_ex = Service('Programming', 'Programming (external)', EX_PROGRAMMING)

        self.services.append(comp_sci)
        self.services.append(gis)
        self.services.append(vis)
        self.services.append(hpc)
        self.services.append(programming)

        self.services.append(comp_sci_ex)
        self.services.append(gis_ex)
        self.services.append(vis_ex)
        self.services.append(hpc_ex)
        self.services.append(programming_ex)

    def get_cost(self, service_name=''):
        if service_name == '':
            return 0

        for service in self.services:
            if service.redmine_name == service_name or service.cores_name == service_name:
                return service.cost

    def get_cores_name(self, service_name=''):
        if service_name == '':
            return ''

        for service in self.services:
            if service.redmine_name == service_name or service.cores_name == service_name:
                return service.cores_name
