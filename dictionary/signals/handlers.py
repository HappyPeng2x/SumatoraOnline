from os.path import join, basename
from glob import glob

from django.dispatch import receiver
from django.db.backends.signals import connection_created

@receiver(connection_created)
def my_receiver(connection, **kwargs):
    with connection.cursor() as cursor:
        # Attaching dictionaries
        for f in glob(join('dictionary', 'dictionaries', '*.db')):
            name = basename(f)
            cursor.execute("ATTACH '" + f + "' AS " + name[:name.find(".")])