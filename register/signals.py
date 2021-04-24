##### Signals #####
import random
import string

from django.db.models.signals import post_save
from django.dispatch import receiver
from IW.models import ConfirmationCode
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def login_logger(sender, instance, created, **kwargs):
    if created:
        cc = ConfirmationCode(user=instance, code=generate_code())
        print("New Code generated", cc)
        cc.save()


def generate_code(size=15):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=size))
