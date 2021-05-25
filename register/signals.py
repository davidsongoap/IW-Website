##### Signals #####
import random
import string

from django.db.models.signals import post_save
from django.dispatch import receiver
from IW.models import ConfirmationCode, ProfileImage, Participation, Tournament
from django.contrib.auth.models import User
from django.core.mail import send_mail
from IW.views import is_tournament_full


@receiver(post_save, sender=User)
def login_logger(sender, instance, created, **kwargs):
    if created:
        cc = ConfirmationCode(user=instance, code=generate_code())
        if instance.is_superuser:
            cc.validated = True
        pi = ProfileImage(user=instance)

        pi.save()
        cc.save()

        # TODO email with html
        send_mail(
            'ISEL Winner Confirmation Code',
            'Your confirmation code is: ' + str(cc.code),
            from_email=None,
            recipient_list=[instance.email],
            fail_silently=False
        )


@receiver(post_save, sender=Participation)
def add_participation(sender, instance, created, **kwargs):
    if created:
        t = instance.tournament_id
        if is_tournament_full(t):
            t.state = 'CL'
            t.save()


def generate_code(size=15):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=size))
