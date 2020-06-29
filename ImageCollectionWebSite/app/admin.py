from django.contrib import admin

import app.models as models


admin.site.register(models.Image)
admin.site.register(models.Comment)