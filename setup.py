from setuptools import setup

setup(
    name='platter',
    version='0.1',
    py_modules=['platter'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        platter=platter:cli
    ''',
)