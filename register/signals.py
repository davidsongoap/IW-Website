##### Signals #####
import random
import string

from django.db.models.signals import post_save
from django.dispatch import receiver
from IW.models import ConfirmationCode, ProfileImage
from django.contrib.auth.models import User
from django.core.mail import send_mail


@receiver(post_save, sender=User)
def login_logger(sender, instance, created, **kwargs):
    if created:
        cc = ConfirmationCode(user=instance, code=generate_code())
        # print("New Code generated", cc)
        pi = ProfileImage(user=instance)

        pi.save()
        cc.save()

        send_mail(
            'ISEL Winner Confirmation Code',
            'Your confirmation code is: ' + str(cc.code),
            from_email=None,
            recipient_list=[instance.email],
            fail_silently=False
        )


def generate_code(size=15):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=size))
