from django.contrib import admin
from .models import CustomUser
from .models import DesignRequest

admin.site.register(DesignRequest)
admin.site.register(CustomUser)
