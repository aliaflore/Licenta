from django.db.models.signals import post_save
from django.dispatch import receiver
from licenta.models import AnalizePDF
from licenta.tasks import analyze_pdf


@receiver(post_save, sender=AnalizePDF)
def start_analysis(sender, instance: AnalizePDF, **kwargs):
    print("Scheduled analysis for", instance.id, instance.user.id)
    analyze_pdf.delay(instance.id, instance.user.id)
