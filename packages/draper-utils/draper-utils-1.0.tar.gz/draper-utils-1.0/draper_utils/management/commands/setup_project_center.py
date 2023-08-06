import time
from genericpath import exists
from os.path import abspath, join, dirname
import requests

from sqlalchemy import create_engine
from sqlalchemy import text

from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from project_center.models import Project, ProjectCategory, ProjectStatus, ProjectStage, ProjectActivity, User, Company
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils.timezone import make_aware
from django.template.defaultfilters import slugify
from django.contrib.auth.models import Group


def full_path(filename):
    return abspath(join(dirname(__file__), filename))


class Command(BaseCommand):
    help = """Sets up initial Groups for Draper Project Center."""

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit', action='store', dest='limit', default=None,
            help="Import Limit"
        )
        parser.add_argument(
            '--order', action='store', dest='order', default=None,
            help="Import Order"
        )
        parser.add_argument(
            '--reset', action='store_true', dest='reset', default=False,
            help="Clear all projects before importing"
        )

    def handle(self, *args, **options):
        engine = create_engine(settings.PROJECT_CENTER_IMPORT_DATABASE_URL)
        limit = options['limit']
        order = options['order']
        reset = options['reset']
        tic = time.perf_counter()
        pc_user_group = Group.objects.get_or_create(name=settings.PROJECT_CENTER_USER_GROUP_NAME)
        pc_admin_group = Group.objects.get_or_create(name=settings.PROJECT_CENTER_ADMINISTRATOR_GROUP_NAME)
        pc_company_admin_group = Group.objects.get_or_create(name=settings.PROJECT_CENTER_COMPANY_ADMINISTRATOR_GROUP_NAME)
        pdb = User.objects.get(username='pdbethke')
        pdb.first_name = 'Peter'
        pdb.last_name = 'Bethke'
        print(pdb)
        pdb.save()


        print(pc_user_group, pc_admin_group, pc_company_admin_group)
        # if reset:
        #     projects = Project.objects.all().delete()
        #     activities = ProjectActivity.objects.all().delete()
        #     stages = ProjectStage.objects.all().delete()
        #     statuses = ProjectStatus.objects.all().delete()
        #     categories = ProjectCategory.objects.all().delete()
        # self.import_project_categories(engine, full_path('../../sql/list_project_categories.sql'))
        # self.import_project_status(engine, full_path('../../sql/list_project_statuses.sql'))
        # self.import_project_stages(engine, full_path('../../sql/list_project_stages.sql'))
        # self.import_project_users(engine, full_path('../../sql/list_project_users.sql'))
        # self.import_projects(engine, full_path('../../sql/list_projects.sql'), limit=limit, order=order)
        # self.import_project_activities(engine, full_path('../../sql/list_project_activities.sql'), limit=limit)
        toc = time.perf_counter()
        print(settings.SITE_ID)
        # if user:
        #     user.delete()

        # for x in (get_candidate_data_rest(candidate_id).keys()):
        #     print(x)