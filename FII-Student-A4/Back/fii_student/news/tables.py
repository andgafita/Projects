import django_tables2
from .models import News
from django.utils.html import format_html


class NewsTable(django_tables2.Table):
    def __init__(self, *args, **kwargs):
        super(NewsTable, self).__init__(*args, **kwargs)

    @staticmethod
    def render_timestamp(record):
        if record.timestamp:
            return record.timestamp.strftime('%Y/%m/%d %H:%M:%S')
        return "—"

    class Meta:
        model = News
        # attrs = {"style": "font-size: 0.8rem; width:100%; margin:auto;"}
