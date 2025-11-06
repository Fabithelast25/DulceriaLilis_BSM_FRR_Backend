from django.db import migrations, models


class Migration(migrations.Migration):

    # 👇 apúntalo a tu última migración real
    dependencies = [
        ('Panel_Usuarios', '0001_initial'),
    ]

    operations = [
        # Campos base que suelen faltar en tu tabla 'usuario'
        migrations.AddField(
            model_name='usuario',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='usuario',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='usuario',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        # Nota: los M2M (groups / user_permissions) normalmente ya quedaron definidos
        # en 0001_initial si tu modelo ya heredaba de AbstractUser. Si luego te faltan
        # las tablas intermedias, las agregamos en otra migración.
    ]
