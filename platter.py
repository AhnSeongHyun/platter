import click
import sys
import shutil
import os


@click.command()
@click.option('--name', prompt='app name', default=None, help='enter app name')
def generate_app(app_name):
    click.echo('Hello World : {}'.format(app_name))
    # 디렉토리 복사
    try:
        cp_path = './_{}'.format(app_name)
        shutil.copytree('./app', cp_path)

        # 리소스 입력 받기
        resources = []
        while True:
            resource = input("Enter Resource: ")
            if resource != 'exit':
                resources.append(resource)

        # DB 정보 입력 받기
        db_host = input("Enter DB Host URL(localhost:3306):")
        db_database = input("Enter DB Scheme(test): ")
        db_user = input("Enter DB User(root): ")
        db_password = input("Enter DB Password(root): ")


        # todo : 순회하면서 기존 파일에서 재작성
        #rendered_template = render_template('.html', result=result)


        # 디렉토리 이동
        mv_path = input("Move to path(.):")
        shutil.move(cp_path, mv_path)

    except Exception as e:
        print(e)