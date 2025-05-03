# db/mysql_connection.py

import pymysql
from django.conf import settings

def get_connection():
    return pymysql.connect(
        host=settings.DATABASES['default']['HOST'],
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        db=settings.DATABASES['default']['NAME'],
        charset='utf8mb4',  # Ensure proper encoding for extended characters
        cursorclass=pymysql.cursors.DictCursor
    )
