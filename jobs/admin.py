from django.contrib import admin
from jobs.models import Sectors,Company,Jobs, Applications

# Register your models here.
admin.site.register(Sectors)
admin.site.register(Company)
admin.site.register(Jobs)
admin.site.register(Applications)
