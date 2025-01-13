from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import users.signals
        from account import hooks
        from users.hooks import custom_send_email_confirmation  # Импорт кастомного метода
        hooks.send_email_confirmation = custom_send_email_confirmation