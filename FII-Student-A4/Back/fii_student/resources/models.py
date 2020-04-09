from django.db import models


class Resources(models.Model):
    resources_id = models.AutoField(primary_key=True, verbose_name='ID')
    title = models.CharField(max_length=128)
    timestamp = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    url = models.TextField(null=True)
    content = models.TextField(null=True)
    type = models.TextField()

    class Meta:
        db_table = 'resources'

    def __str__(self):
        return {
            'title': self.title,
            'url': self.url,
            'content': self.content,
            'type': self.type
        }