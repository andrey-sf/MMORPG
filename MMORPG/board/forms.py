from django import forms
from .models import Ad, Response


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
            'description': forms.Textarea(attrs={
                'class': 'form-control',
            }),
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


class ResponseAcceptForm(forms.Form):
    response_id = forms.IntegerField(widget=forms.HiddenInput())
