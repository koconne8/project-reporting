"""
WSGI config for pr project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
import sys
#import site

# Define the virtualenv to use
#site.addsitedir('/opt/project_reports/pr/env')

from django.core.wsgi import get_wsgi_application
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pr.settings.production")

# Activate the virtualenv
#activate_env = os.path.expanduser('/opt/project_reports/pr/env/bin/activate_this.py')
#execfile(activate_env, dict(__file__=activate_env))

application = get_wsgi_application()
