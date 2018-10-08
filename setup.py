import os

from setuptools import setup

data_dir = os.path.join('./', 'app')
data_files = []

for d, folders, files in os.walk(data_dir):
    for f in files:
        data_files.append((d, [os.path.join(d, f)]))

setup(
    name='platter',
    version='0.1',
    py_modules=['platter'],
    url='',
    license='MIT',
    author='ash84',
    author_email='sh84.ahn@gmail.com',
    description='platter',
    data_files=data_files,
    long_description=open('README.md').read(),
    install_requires=[
        'Click',
        'colorama'
    ],
    entry_points='''
        [console_scripts]
        platter=platter:generate_app
    '''
)
