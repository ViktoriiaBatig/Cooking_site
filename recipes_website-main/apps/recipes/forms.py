from django import forms
from .models import Recipe
from django.utils.translation import gettext_lazy as _


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'image', 'video']
        labels = {
            'title': _('Назва'),
            'description': _('Опис'),
            'image': _('Фото'),
            'video': _('Відео'),
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Введите назву')}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': _('Введите опис')}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'video': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def is_file_field(self, field_name):
        field = self.fields[field_name]
        return isinstance(field.widget, forms.FileInput)