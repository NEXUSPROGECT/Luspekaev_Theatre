import account.forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django import forms

class SignupForm(account.forms.SignupForm):

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        del self.fields["username"]
        if "code" in self.fields:
            del self.fields["code"]

    first_name = forms.CharField(
        max_length=30,
        label="Ваше Имя",
        required=True,
        widget=forms.TextInput(attrs={})
    )
    last_name = forms.CharField(
        max_length=30,
        label="Ваша Фамилия",
        required=True,
        widget=forms.TextInput(attrs={})
    )


    def save(self, user=None):
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name = self.cleaned_data.get("last_name", "")
        user.save()
        return user


class SettingsForm(account.forms.SettingsForm):
    first_name = forms.CharField(
        label=_("Имя"),
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": _("Ваше имя")}),
    )
    last_name = forms.CharField(
        label=_("Фамилия"),
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": _("Фамилия")}),
    )



    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  # Извлекаем пользователя, если он передан
        super().__init__(*args, **kwargs)

        # Устанавливаем начальные значения для полей
        if user:
            self.fields["first_name"].initial = user.first_name
            self.fields["last_name"].initial = user.last_name