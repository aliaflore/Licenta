from datetime import timedelta
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from licenta.models import AnalysisPDF, AnalysisResult, PatientInvite
from licenta.tasks import add_suggestion, analyze_pdf, notify_patient_about_invite
import logging
from django.utils import timezone


logger = logging.getLogger(__name__)


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
