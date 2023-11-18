from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Category, DesignRequest


@receiver(pre_delete, sender=Category)
def delete_category_with_requests(sender, instance, **kwargs):
    DesignRequest.objects.filter(category=instance).delete()
