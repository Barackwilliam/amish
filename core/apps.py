from django.apps import AppConfig
from django.db.models.signals import pre_save


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "Website"

    def ready(self):
        from django.apps import apps

        from .imaging import optimize_on_save

        for label in ("core", "divisions", "company"):
            for model in apps.get_app_config(label).get_models():
                pre_save.connect(
                    optimize_on_save, sender=model,
                    dispatch_uid=f"optimize_{label}_{model.__name__}",
                )
