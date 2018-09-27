# -*- coding:utf-8 -*-
import click
import sys
import shutil
import os
import signal 
from uuid import uuid1 

@click.command()
@click.option('--app_name', prompt='app name', default=None, help='enter app name')
def generate_app(app_name):
    click.echo('Hello World : {}'.format(app_name))
    # 디렉토리 복사
    try:
        cp_path = None 
        mv_path = None 
        def sig_test(signum, frame):
            print('cp_path:{}'.format(cp_path))

            if cp_path:
                shutil.rmtree(cp_path)
            if mv_path:
                shutil.rmtree(mv_path)
            sys.exit()

        signal.signal(signal.SIGINT, sig_test)

        cp_path = './_{}_{}'.format(app_name, str(uuid1()))
        shutil.copytree('./app', cp_path)

        # 리소스 입력 받기
        resources = []
        while True:
            r = input("Enter Resource(stop 'end'): ")
            print(r)
            if r:
               if r.lower() == 'end':
                    break 
               else:
                    resources.append(r)


        # DB 정보 입력 받기
        db_host = input("Enter DB Host URL(localhost:3306):").strip()
        db_host = db_host if db_host else 'localhost:3306'
        
        db_scheme = input("Enter DB Scheme(test): ").strip()
        db_scheme = db_scheme if db_scheme else 'test'

        db_user = input("Enter DB User(root): ").strip()
        db_user = db_user if db_user else 'root'

        db_password = input("Enter DB Password(root): ").strip()
        db_passowrd = db_password if db_password else 'root'

        print('resources:{}'.format(resources))

        # todo : 순회하면서 기존 파일에서 재작성
        for root, dirs, files, in os.walk(cp_path, topdown=False):
            print(root, dirs, files)
 






        #rendered_template = render_template('.html', result=result)


        # 디렉토리 이동
        #mv_path = input("Move to path(.):")
        #shutil.move(cp_path, mv_path)

    except Exception as e:
        import traceback 
        print(traceback.format_exc())
        print(e)


def render_file(template_file_path, app_name, resoucre=None):
    from jinja2 import Environment
    from jinja2 import PackageLoader
    
    env = Environment(loader=PackageLoader(package, 'templates'), autoescape=False, extensions=['jinja2.ext.autoescape'])
    t = env.get_template(template_file_path)
    rendered_template = t.render({'app':app_name, 'resource':resource})
    return rendered_template


if __name__ == '__main__':
    generate_app()
