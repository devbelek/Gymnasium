from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import UserProfile, Donation, ConfirmedDonation


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get('email', '').lower()
        if email:
            try:
                email_address = EmailAddress.objects.get(email__iexact=email)
                if email_address.user:
                    sociallogin.connect(request, email_address.user)
            except EmailAddress.DoesNotExist:
                pass


@receiver(post_save, sender=Donation)
def create_confirmed_donation(sender, instance, created, **kwargs):
    if instance.is_verified and not hasattr(instance, 'confirmed_donation'):
        ConfirmedDonation.objects.create(
            donation=instance,
            user=instance.user,
            comment=instance.comment
        )