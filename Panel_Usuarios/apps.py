from django.apps import AppConfig


class PanelUsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Panel_Usuarios'
    
    def ready(self):
        import Panel_Usuarios.signals
