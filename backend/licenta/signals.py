from django.db.models.signals import post_save
from django.dispatch import receiver
from licenta.models import AnalizePDF
from licenta.tasks import analyze_pdf


@receiver(post_save, sender=AnalizePDF)
def start_analysis(sender, instance: AnalizePDF, **kwargs):
    print(
        "incepe ciuc sa ma enerveze dar e ok ca il iubesc sau cel putin incerc sa il iubesc si acum trag de timp dar ciuc nu isi da seama si acum"
    )
    # add.delay(1, 2)
    analyze_pdf.delay(instance.id, instance.user.id)
