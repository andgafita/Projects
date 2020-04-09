from django import forms
from .models import News


#class NewsForm(forms.ModelForm):
#    def __init__(self, *args, **kwargs):
 #       super(NewsForm, self).__init__(*args, **kwargs)

 #   class Meta:
  #      model = News


class NewsForm(forms.ModelForm):
    title = forms.CharField(max_length=2000, required=True)
    body = forms.CharField(widget=forms.Textarea, required=True)


    class Meta:
        model = News
        #exclude = ()
        fields = ('title', 'body')
        #fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form-control'})

