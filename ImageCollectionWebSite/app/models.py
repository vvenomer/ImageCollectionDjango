from django.db import models
from django.contrib.auth import models as AuthModels

class Image(models.Model):
    user = models.ForeignKey(AuthModels.User, on_delete=models.CASCADE, verbose_name = "Użytkownik")
    title = models.CharField(max_length=128, verbose_name = "Tytuł")
    description = models.TextField(verbose_name = "Opis")
    image = models.ImageField(upload_to = "img/", null=True, verbose_name = "Obraz")
    canComment = models.BooleanField(verbose_name = "Czy można komentować?")

    def get_absolute_url(self):
        return '/'

    def __str__(self):
        return f'Obraz: {self.title}'

    class Meta:
        verbose_name = "Obraz"
        verbose_name_plural = "Obrazy"

class Comment(models.Model):
    user = models.ForeignKey(AuthModels.User, on_delete=models.CASCADE, verbose_name = "Użytkownik")
    image = models.ForeignKey(Image, on_delete=models.CASCADE, verbose_name = "Obraz")
    content = models.TextField(verbose_name = "Zawartość")

    def __str__(self):
        return 'Komentarz'

    class Meta:
        verbose_name = "Komentarz"
        verbose_name_plural = "Komentarze"