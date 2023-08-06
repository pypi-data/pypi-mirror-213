from django.db.models.signals import pre_save, post_save
from django.core.signals import request_finished
from django.dispatch import receiver
from ..models import ProjectActivity

@receiver(post_save, sender=ProjectActivity)
def duplicate(sender, instance, **kwargs):
    print('foo*******************')
post_save.connect(duplicate, sender=ProjectActivity)
