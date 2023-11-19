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

    def clean_photo(self):
        image = self.cleaned_data.get('photo')

        # Проверка наличия изображения
        if not image:
            raise forms.ValidationError("Необходимо загрузить изображение.")

        # Проверка формата изображения
        allowed_formats = ['jpg', 'jpeg', 'png', 'bmp']
        image_format = image.name.split('.')[-1].lower()
        if image_format not in allowed_formats:
            raise forms.ValidationError(
                "Формат изображения не поддерживается. Поддерживаемые форматы: jpg, jpeg, png, bmp.")

        # Проверка размера изображения
        max_size = 2 * 1024 * 1024  # 2 Мб
        if image.size > max_size:
            raise forms.ValidationError("Максимальный размер изображения - 2 Мб.")

        return image

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo'].required = True


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
