platter
=========

platter is script for creation Flask-based project skeleton.


### Install

```shell
> python3 setup.py install
```

### Run

```shell
> platter

 #####  #        ##   ##### ##### ###### #####
 #    # #       #  #    #     #   #      #    #
 #    # #      #    #   #     #   #####  #    #
 #####  #      ######   #     #   #      #####
 #      #      #    #   #     #   #      #   #
 #      ###### #    #   #     #   ###### #    #

> App Name: flask_app
> Default Resource : user, admin
> Enter Resource(stop 'end'): push
> Enter Resource(stop 'end'): order
> Enter Resource(stop 'end'): pay
> Enter Resource(stop 'end'): end

> Enter DB Host URL(localhost:3306):
> Enter DB Scheme(test):
> Enter DB User(root):
> Enter DB Password(root):
> App Info : {'app': 'flask_app',
 'db_host': 'localhost:3306',
 'db_password': 'root',
 'db_scheme': 'test',
 'db_user': 'root',
 'resources': ['user', 'admin', 'push', 'team', 'order', 'pay']}

> create file : ..
> create model : ..
> create resoruce : ..

Move to path(.):
========================================
platter complete : flask_app
========================================

```

```
> flask_app  tree                                                                                                            ✓  4954  23:29:27
.
├── README.md
├── __init__.py
├── app.py
├── commons
│   ├── __init__.py
│   ├── cipher
│   │   ├── __init__.py
│   │   └── aes256.py
│   ├── jwt_token.py
│   ├── logger.py
│   ├── sentry.py
│   └── utils.py
├── compile.sh
├── config.py
├── extensions.py
├── gunicorn_config.ini
├── models
│   ├── __init__.py
│   ├── admin.py
│   ├── base.py
│   ├── order.py
│   ├── pay.py
│   ├── push.py
│   ├── team.py
│   └── user.py
├── requirements
├── resources
│   ├── __init__.py
│   ├── admin
│   │   ├── __init__.py
│   │   ├── admin_api.py
│   │   └── admin_view.py
│   ├── base.py
│   ├── order
│   │   ├── __init__.py
│   │   ├── order_api.py
│   │   └── order_view.py
│   ├── pay
│   │   ├── __init__.py
│   │   ├── pay_api.py
│   │   └── pay_view.py
│   ├── push
│   │   ├── __init__.py
│   │   ├── push_api.py
│   │   └── push_view.py
│   ├── response_data.py
│   ├── team
│   │   ├── __init__.py
│   │   ├── team_api.py
│   │   └── team_view.py
│   └── user
│       ├── __init__.py
│       ├── user_api.py
│       └── user_view.py
├── start.sh
├── templates
│   ├── errors
│   │   └── error.html
│   └── resource_html
│       └── index.html
└── tests
    └── __init__.py
```
