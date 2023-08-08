from django.db import models


# Create your models here.
class ContentCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="name")
    key = models.CharField(max_length=100, verbose_name="category_key")

    class Meta:
        db_table = "tb_content_category"

    def __str__(self):
        return self.name


class Content(models.Model):
    category = models.ForeignKey(ContentCategory, on_delete=models.PROTECT, related_name="category",
                                 verbose_name="category_id")
    title = models.CharField(max_length=100, verbose_name="Ad_title")
    url = models.URLField(max_length=300, verbose_name="content_url")
    image = models.ImageField(blank=True, null=True, verbose_name="image")
    text = models.TextField(blank=True, null=True, verbose_name="content")
    sequence = models.IntegerField(verbose_name="sequence")
    status = models.BooleanField(default=True, verbose_name="isShow")

    class Meta:
        db_table = "tb_content"

    def __str__(self):
        return self.category.name + " " + self.title
