from datetime import timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.db.backends.signals import connection_created
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from licenta.models import AnalysisPDF, AnalysisResult, PatientInvite, User
from licenta.tasks import add_suggestion, analyze_pdf, notify_patient_about_invite
import logging
from django.utils import timezone


logger = logging.getLogger(__name__)


@receiver(connection_created)
def setup_sqlite_pragmas(sender, connection, **kwargs):
    if connection.vendor == 'sqlite':
        cursor = connection.cursor()
        cursor.execute('PRAGMA journal_mode=wal;')
        cursor.execute('PRAGMA busy_timeout=5000;')
        cursor.close()


@receiver(post_save, sender=AnalysisPDF)
def start_analysis(sender, instance: AnalysisPDF, **kwargs):
    logger.info("Scheduling analysis for analysis %s", instance.pk)
    analyze_pdf(instance.id)


# @receiver(post_save, sender=AnalysisResult)
def suggest_fix(sender, instance: AnalysisResult, **kwargs):
    created = kwargs.get("created", False)
    if not created:
        return

    if instance.range_min is not None and instance.range_max is not None:
        try:
            result = float(instance.result)
        except ValueError:
            return

        if result < instance.range_min or result > instance.range_max:
            add_suggestion.delay(instance.pk)

    logger.info("Scheduled fix suggestion for AnalysisResult %s", instance.pk)

@receiver(post_save, sender=PatientInvite)
def send_invite_email(sender, instance: PatientInvite, **kwargs):
    if instance.accepted:
        return

    notify_patient_about_invite.delay(instance.pk)

@receiver(pre_save, sender=PatientInvite)
def on_accepted_set(sender, instance: PatientInvite, **kwargs):
    if instance.accepted and not instance.accepted_on:
        instance.accepted_on = timezone.now()
        instance.expires = timezone.now() + timedelta(days=30)

@receiver(post_save, sender=User)
def on_doctor_registered(sender, instance: User, created=False, **kwargs):
    if instance.is_doctor and not instance.is_active:
        logger.info("Doctor %s registered, notifying admins", instance.pk)
        for user in User.objects.filter(is_staff=True):
            send_mail(
                "Doctor registered",
                f"Doctor {instance.email} has registered. Please verify their Doctor proof.",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )


@receiver(pre_save, sender=User)
def on_doctor_activated(sender, instance: User, **kwargs):
    if not instance.pk:
        return
    current_user = User.objects.get(pk=instance.pk)
    if instance.is_doctor and instance.is_active and not current_user.is_active:
        logger.info("Doctor %s activated, notifying the doctor", instance.pk)
        send_mail(
            "Doctor account activated",
            "Your doctor account has been activated. You can now use the platform.",
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
        )


@receiver(post_save, sender=AnalysisPDF)
def notify_doctor_about_new_analysis(sender, instance: AnalysisPDF, **kwargs):
    for invite in PatientInvite.objects.filter(patient=instance.user, accepted=True):
        logger.info("Notifying doctor %s about new analysis %s", invite.doctor.pk, instance.pk)
        send_mail(
            "New analysis uploaded",
            f"Patient {instance.user.email} has uploaded a new analysis. You can now view it.",
            settings.DEFAULT_FROM_EMAIL,
            [invite.doctor.email],
        )
