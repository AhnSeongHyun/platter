# -*- coding:utf-8 -*-
import os
import pprint
import shutil
import signal
import sys
from os.path import join as path_join
from os.path import split as path_split
from uuid import uuid1

import click
from colorama import Fore, Style
from colorama import init
from jinja2 import FileSystemLoader, Environment

init()
ci = """                                                
 #####  #        ##   ##### ##### ###### #####  
 #    # #       #  #    #     #   #      #    # 
 #    # #      #    #   #     #   #####  #    # 
 #####  #      ######   #     #   #      #####  
 #      #      #    #   #     #   #      #   #  
 #      ###### #    #   #     #   ###### #    #                                                 
"""
print(Fore.BLUE)
print(ci)

@click.command()
@click.option('--app_name', prompt=Fore.YELLOW + 'App Name', default=None, help='enter app name')
def generate_app(app_name):

    working_dir = os.getcwd()
    package_dir = os.path.dirname(os.path.abspath(__file__))

    # 디렉토리 복사
    try:
        cp_path = None 
        mv_path = None

        def sig_test(signum, frame):
            if cp_path:
                shutil.rmtree(cp_path)
            if mv_path:
                shutil.rmtree(mv_path)
            sys.exit()

        signal.signal(signal.SIGINT, sig_test)

        template_app_dir_path = path_join(package_dir, 'app')
        cp_path = path_join(working_dir, '{}_{}'.format(app_name, str(uuid1())))
        shutil.copytree(template_app_dir_path, cp_path)

        # 리소스 입력 받기
        resources = ['user', 'admin']
        print(Fore.GREEN + 'Default Resource : user, admin')

        while True:
            print(Fore.YELLOW, end='')
            r = input("Enter Resource(stop 'end'): ")
            if r:
                if r.lower() == 'end':
                    break
                else:
                    if r.lower() in resources:
                        print(Fore.RED + '{} is already exist.'.format(r.lower()))
                    else:
                        resources.append(r)

        # DB 정보 입력 받기
        print(Fore.YELLOW)
        db_host = input("Enter DB Host URL(localhost:3306):").strip()
        db_host = db_host if db_host else 'localhost:3306'
        
        db_scheme = input("Enter DB Scheme(test): ").strip()
        db_scheme = db_scheme if db_scheme else 'test'

        db_user = input("Enter DB User(root): ").strip()
        db_user = db_user if db_user else 'root'

        db_password = input("Enter DB Password(root): ").strip()
        db_password = db_password if db_password else 'root'

        render_params = {'db_host': db_host,
                         'db_user': db_user,
                         'db_scheme': db_scheme,
                         'db_password': db_password,
                         'app': app_name,
                         'resources': resources}

        print(Fore.BLUE + 'App Info : {}'.format(pprint.pformat(render_params)))

        # create file
        conv_file_list = ['app.py.j2',
                          'README.md.j2',
                          '.travis.yml.j2',
                          'gunicorn_config.ini.j2',
                          'config.py.j2',
                          'resources{}base.py.j2'.format(os.sep),
                          'models{}base.py.j2'.format(os.sep),
                          'commons{}jwt_token.py.j2'.format(os.sep),
                          'commons{}logger.py.j2'.format(os.sep),
                          'commons{}sentry.py.j2'.format(os.sep),
                          ]
        conv_file_path_list = [path_join(cp_path, file) for file in conv_file_list]

        print(Fore.MAGENTA)
        for conv_file_path in conv_file_path_list:
            directory, template_file = path_split(conv_file_path)
            rendered_template = render_from_template(directory, template_file, **render_params)
            with open(conv_file_path[:conv_file_path.find('.j2')], 'w') as f:
                f.write(rendered_template)

            print('create file    : {}'.format(conv_file_path))
            os.remove(conv_file_path)

        model_template = 'models{}model_template.py.j2'.format(os.sep)

        # create model
        model_template_path = path_join(cp_path, model_template)
        for r in resources:
            dst_model_path = path_join(cp_path, 'models/{}.py'.format(r))
            shutil.copy(model_template_path, dst_model_path)

            directory, template_file = path_split(dst_model_path)
            render_params['resource'] = r[0].upper() + r[1:]  # user => User
            rendered_template = render_from_template(directory, template_file, **render_params)
            with open(dst_model_path, 'w') as f:
                f.write(rendered_template)
            print('create model   : {} => {}'.format(model_template_path, dst_model_path))
        os.remove(model_template_path)

        # create resources
        resources_template_dir = 'resources{}resource_template'.format(os.sep)
        resources_template_dir_path = path_join(cp_path, resources_template_dir)

        blueprint_list = []
        for r in resources:
            r = r.lower()
            dst_resource_dir_path = path_join(cp_path, 'resources{}{}'.format(os.sep, r))
            shutil.copytree(resources_template_dir_path, dst_resource_dir_path)
            print('create resource: {} => {}'.format(resources_template_dir_path, dst_resource_dir_path))

            template_api_file_path = path_join(dst_resource_dir_path, 'resource_api.py.j2')
            template_view_file_path = path_join(dst_resource_dir_path, 'resource_view.py.j2')
            dst_api_file_path = path_join(dst_resource_dir_path, '{}_api.py'.format(r))
            dst_view_file_path = path_join(dst_resource_dir_path, '{}_view.py'.format(r))
            shutil.move(template_api_file_path, dst_api_file_path)
            shutil.move(template_view_file_path, dst_view_file_path)

            for dst_file_path in [dst_api_file_path, dst_view_file_path]:
                directory, template_file = path_split(dst_file_path)
                render_params['resource'] = r
                rendered_template = render_from_template(directory, template_file, **render_params)
                with open(dst_file_path, 'w') as f:
                    f.write(rendered_template)

            blueprint_list.append('{}_api'.format(r))
            blueprint_list.append('{}_view'.format(r))

        # register resource flask bule prints
        resource_init_file_path = path_join(cp_path, 'resources{}__init__.py'.format(os.sep))
        with open(resource_init_file_path, 'w') as f:
            f.write('resource_blueprints = ' + str(pprint.pformat(blueprint_list, indent=4)))
        shutil.rmtree(resources_template_dir_path)

        # move directory
        print(Fore.YELLOW)
        mv_path = input("Move to path(.):")
        mv_path = mv_path if mv_path else '.'
        mv_path = path_join(mv_path, app_name)
        shutil.copytree(cp_path, mv_path)
        shutil.rmtree(cp_path)

        # remove __pycache__
        for d, folders, files in os.walk(mv_path):
            if '__pycache__' in d:
                shutil.rmtree(d)

        print(Fore.BLUE, end='')
        print(Style.DIM, end='')
        print('=' * 40)
        print('platter complete : {}'.format(os.path.abspath(mv_path)))
        print('=' * 40)
    except Exception as e:
        import traceback 
        print(traceback.format_exc())
        print(e)


def render_from_template(directory, template_name, **kwargs):
    loader = FileSystemLoader(directory)
    env = Environment(loader=loader)
    template = env.get_template(template_name)
    return template.render(**kwargs)