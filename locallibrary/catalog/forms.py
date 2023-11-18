from .models import CustomUser
from .models import Category
from django import forms
from .models import DesignRequest


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['fio', 'email', 'username', 'password', 'confirm_password', 'agreement']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают.')


class DesignRequestForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None)

    class Meta:
        model = DesignRequest
        fields = ['title', 'description', 'category', 'photo']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
