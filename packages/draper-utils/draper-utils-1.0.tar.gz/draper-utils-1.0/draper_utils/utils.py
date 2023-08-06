import time
from genericpath import exists
from os.path import abspath, join, dirname
import requests

from sqlalchemy import create_engine
from sqlalchemy import text

from django.contrib.auth import authenticate
from django.core.management.base import BaseCommand
from project_center.models import Project, ProjectCategory, ProjectStatus, ProjectStage, ProjectActivity, User, Company
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils.timezone import make_aware
from django.template.defaultfilters import slugify
from django.contrib.auth.models import Group


def full_path(filename):
    return abspath(join(dirname(__file__), filename))

def import_project_categories(engine, file):
    with engine.connect() as conn:
        with open(file) as file:
            query = text(file.read())
            result = conn.execute(query)
            for row in result:
                category, created = ProjectCategory.objects.update_or_create(
                    import_id=int(row.category_id),
                defaults={
                    'name':row.category_name
                })

def import_project_status(engine, file):
    with engine.connect() as conn:
        with open(file) as file:
            query = text(file.read())
            result = conn.execute(query)
            for row in result:
                status, created = ProjectStatus.objects.update_or_create(
                    import_id=int(row.status_id),
                defaults={
                    'name':row.status_name
                })


def import_project_stages(engine, file):
    with engine.connect() as conn:
        with open(file) as file:
            query = text(file.read())
            result = conn.execute(query)
            for row in result:
                status, created = ProjectStage.objects.update_or_create(
                    import_id=int(row.stage_id),
                defaults={
                    'name':row.stage_name
                })

def import_project_users(engine, file):
    company, created = Company.objects.update_or_create(name='Veolia')
    usergroup, created = Group.objects.get_or_create(name='Commdep User')
    with engine.connect() as conn:
        with open(file) as file:
            query = text(file.read())
            result = conn.execute(query)
            for row in result:
                user, created = User.objects.update_or_create(
                    import_id=int(row.user_id),
                defaults={
                    'first_name':row.first_name,
                    'last_name': row.last_name,
                    'email': row.email,
                    'username': row.email,
                    'company':company
                })
                # if created or not user.companies:
                #     user.companies.add(company)
                #     user.save()
                if created or user.groups.filter(name='Commdep User').exists() is False:
                    user.set_password(row.password)

                    user.groups.add(usergroup)
                    user.save()

def import_project_activities(engine, file, project=None, limit=None):
        with engine.connect() as conn:
            with open(file) as file:
                query = 'SELECT * FROM `ssm_commdep_projects_activities` WHERE ' \
                        'project_id = {project_id}'.format(project_id=project.import_id)

                result = conn.execute(text(query))
                for row in result:
                    try:
                        project = Project.objects.get(import_id=int(row.project_id))
                    except:
                        project = None
                    try:
                        activity_date =  make_aware(row.activity_date)
                    except:
                        activity_date = None
                    if row.file_name:
                        url = 'http://uw.commdep.com/projects/uw/{project_id}/{activity_id}/{file_name}'.format(
                            project_id=row.project_id,
                            activity_id=row.activity_id,
                            file_name=row.file_name,

                        )

                    else:
                        url = None

                    print(url)
                    activity, created = ProjectActivity.objects.update_or_create(
                        import_id=int(row.activity_id),
                    defaults={
                        'name':row.activity_name,
                        'project':project,
                        'date':activity_date,
                        'user':User.objects.get(import_id=row.creator_id),
                    })
                    activity._change_reason = activity.name
                    activity.save()
                    if url:
                        r = requests.get(url)
                        if r.status_code == 200:
                            data = r.content
                            filename = url.split('/')[-1]
                            activity.file.save(filename, ContentFile(data))
                            activity.save()

def import_projects(engine, file, limit=None, order=None):
    with engine.connect() as conn:
        with open(file) as file:
            query = file.read()
            if order:
                query = str(query).strip()
                query += ' ORDER BY ' + order
            if limit:
                query = str(query).strip()
                query += ' LIMIT ' + limit
            result = conn.execute(text(query))
            for row in result:
                try:
                    project_category = ProjectCategory.objects.get(import_id=int(row.category_id))
                except:
                    project_category = None
                try:
                    project_status = ProjectStatus.objects.get(import_id=int(row.status_id))
                except:
                    project_status = None
                try:
                    project_stage = ProjectStage.objects.get(import_id=int(row.stage_id))
                except:
                    project_stage = None

                company, created = Company.objects.update_or_create(name='Veolia')
                project, created = Project.objects.update_or_create(
                    import_id=int(row.project_id),
                    defaults={
                        'title': row.project_title,
                        'slug': '{slug}-{project_id}'.format(slug=slugify(row.project_title),
                                                             project_id=row.project_id),
                        'code': row.project_code,
                        'internal': row.is_internal,
                        'category': project_category,
                        'status': project_status,
                        'stage': project_stage,
                        'company': company
                    })

                project.save()

                import_project_activities(
                    engine=engine,
                    file=full_path('list_project_activities.sql'),
                    project=project,
                    limit=None)