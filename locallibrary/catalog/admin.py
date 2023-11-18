from django.contrib import admin
from .models import CustomUser
from .models import DesignRequest
from django.contrib import admin
from .models import Category

admin.site.register(DesignRequest)
admin.site.register(CustomUser)
admin.site.register(Category)


