import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()
u = User.objects.get(username='user')
u.is_staff = True
u.save()
print('Done: user is_staff =', u.is_staff)
