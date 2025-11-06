from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('Panel_Usuarios', '0007_fix_legacy_nombres_apellidos'),  # ajusta al último número que tengas
    ]
    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE `usuario` MODIFY COLUMN `ultimo_acceso` datetime(6) NULL;",
            reverse_sql="ALTER TABLE `usuario` MODIFY COLUMN `ultimo_acceso` datetime(6) NOT NULL;",
        ),
    ]
