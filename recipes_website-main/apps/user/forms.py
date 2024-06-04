from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from apps.user.models import User


class ProfileChangeForm(forms.ModelForm):
    instagram_url = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'placeholder': 'https://www.instagram.com/yourusername'}))
    telegram_url = forms.URLField(required=False,
                                  widget=forms.URLInput(attrs={'placeholder': 'https://t.me/yourusername'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'bio', 'profile_picture', 'instagram_url', 'telegram_url')
        widgets = {
            'username': forms.TextInput(attrs={'id': 'id_username'}),
            'email': forms.EmailInput(attrs={'id': 'id_email'}),
            'bio': forms.Textarea(attrs={'id': 'id_description'}),
            'profile_picture': forms.FileInput(attrs={'id': 'id_avatar', 'onchange': 'previewFile()'}),
        }

    def clean_instagram_url(self):
        instagram_url = self.cleaned_data.get('instagram_url', '')
        if instagram_url and not instagram_url.startswith('https://www.instagram.com/'):
            raise ValidationError("Посилання на Інстаграм повинно починатися з https://www.instagram.com/")
        return instagram_url

    def clean_telegram_username(self):
        telegram_url = self.cleaned_data.get('telegram_url', '')
        if telegram_url and not telegram_url.startswith('https://t.me/'):
            raise ValidationError("Посилання на Телеграм повинно починатися з https://t.me/")
        return telegram_url


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('username', 'email', 'password1', 'password2')

    def clean_email_or_username(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Дана електронна пошта вже використовується")
        elif User.objects.filter(username=username).exists():
            raise forms.ValidationError("Даний логін вже зайнятий")
        return email, username
