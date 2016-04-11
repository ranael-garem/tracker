from django.db import models


class ScreenShot(models.Model):
    """
    Represents a Screen shot saved using html2canvas
    """
    image = models.ImageField(blank=True, null=True, upload_to='screenshots')
