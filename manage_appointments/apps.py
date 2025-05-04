from django.apps import AppConfig


class ManageAppointmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'manage_appointments'

    def ready(self):
        import manage_appointments.signals
