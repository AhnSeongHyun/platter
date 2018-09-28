./compile.sh
gunicorn -c app:app -c config.ini