from account.decorators import login_required
from django.http import JsonResponse
import account.forms
import account.views
from django.shortcuts import render
from .forms import SettingsForm, SignupForm
from home.models import Tickets


@login_required
def Profile(request):
    tickets = Tickets.objects.filter(user=request.user)
    return render(request, 'profile.html', {'tickets': tickets})

def EmailForm(request):
    return render(request, 'account/email_confirmation_sent.html')

class LoginView(account.views.LoginView):
    form_class = account.forms.LoginEmailForm

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            errors = {
                "non_field_errors": form.non_field_errors().as_text(),
                "field_errors": {
                    field: [str(err) for err in form.errors[field]]
                    for field in form.errors
                }
            }
            return JsonResponse({"success": False, "errors": errors}, status=400)
        return super().form_invalid(form)

class SignupView(account.views.SignupView):

    form_class = SignupForm

    def generate_username(self, form):
        username = form.cleaned_data["email"]
        return username

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            errors = {
                "non_field_errors": form.non_field_errors().as_text(),
                "field_errors": {
                    field: [str(err) for err in form.errors[field]]
                    for field in form.errors
                }
            }
            return JsonResponse({"success": False, "errors": errors}, status=400)
        else:
            return super().form_invalid(form)


    def after_signup(self, form):
        # Вызов метода save формы
        form.save(self.created_user)  # Передаем только что созданного пользователя
        super(SignupView, self).after_signup(form)

class SettingsView(account.views.SettingsView):
    form_class = SettingsForm

    def get_form_kwargs(self):
        # Получаем стандартные аргументы для формы
        kwargs = super().get_form_kwargs()
        # Передаём текущего пользователя
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Обновляем стандартные поля
        user = self.request.user
        user.email = form.cleaned_data["email"]
        user.timezone = form.cleaned_data.get("timezone", "")
        if hasattr(user, "language"):
            user.language = form.cleaned_data.get("language", "")

        # Обновляем дополнительные поля
        user.first_name = form.cleaned_data.get("first_name", "")
        user.last_name = form.cleaned_data.get("last_name", "")
        user.save()
        return super().form_valid(form)