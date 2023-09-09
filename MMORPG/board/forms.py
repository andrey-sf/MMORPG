from django import forms
from .models import Ad, Response
from tinymce.widgets import TinyMCE


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['category', 'title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
            }),
            'description': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }
        labels = {
            'category': 'Категория',
            'title': 'Заголовок',
            'description': 'Описание',
        }


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['responseText']
        widgets = {
            'responseText': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'responseText': 'Текст отклика',
        }


class ResponseFormFilter(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['responseText', 'responseAd', 'is_accepted']

    def __init__(self, *args, **kwargs):
        super(ResponseForm, self).__init__(*args, **kwargs)
        self.fields['responseAd'].label = 'Выберите объявление'
        self.fields['is_accepted'].label = 'Принят отклик?'
        self.fields['responseText'].label = 'Текст отклика'
