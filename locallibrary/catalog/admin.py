from django.core.exceptions import ValidationError

from .forms import DesignRequestAdminForm
from .models import CustomUser
from .models import DesignRequest
from .models import Category
from django.contrib import admin

admin.site.register(CustomUser)
admin.site.register(Category)


from django.contrib import admin
from .models import DesignRequest


class DesignRequestAdmin(admin.ModelAdmin):
    form = DesignRequestAdminForm
    list_display = ('title', 'status', 'user', 'timestamp')

    def save_model(self, request, obj, form, change):
        if obj.status == 'Completed' and not obj.design_image:
            raise ValidationError("При изменении статуса на 'Выполнено' необходимо прикрепить изображение дизайна.")
        elif obj.status == 'In Progress' and not obj.comments:
            raise ValidationError("При изменении статуса на 'Принято в работу' необходимо указать комментарий.")
        elif obj.status in ['In Progress', 'Completed']:
            raise ValidationError("Смена статуса с 'Принято в работу' или 'Выполнено' невозможна.")
        obj.save()

admin.site.register(DesignRequest, DesignRequestAdmin)