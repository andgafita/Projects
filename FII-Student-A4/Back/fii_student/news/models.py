from django.db import models


class News(models.Model):
    MATERII = 'MATERII'
    PROFESORI = 'PROFESORI'
    SECRETARIAT = 'SECRETARIAT'
    CATEGORY_CHOICES = (
        (MATERII, 'MATERII'),
        (PROFESORI, 'PROFESORI'),
        (SECRETARIAT, 'SECRETARIAT')
    )

    news_id = models.AutoField(primary_key=True, verbose_name='ID')
    title = models.CharField(max_length=255)
    author_name = models.CharField(max_length=255)
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES)
    body = models.TextField(blank=True, null=True)
    inserted_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    published_time = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    expire_time = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    source = models.CharField(max_length=255)

    class Meta:
        db_table = 'news'

    def __str__(self):
        return '{}'.format(self.title)
