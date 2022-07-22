from django.db import models


class Posts(models.Model):
    title = models.CharField(max_length=256)
    image = models.URLField()
    content = models.TextField(max_length=1024)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Posts"
