from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('Panel_Usuarios', '0003_alter_usuario_date_joined_alter_usuario_is_active_and_more'),  # ← cambia por tu última migración real
    ]
    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE `usuario` MODIFY COLUMN `area_id` BIGINT NULL;",
            reverse_sql="ALTER TABLE `usuario` MODIFY COLUMN `area_id` BIGINT NOT NULL;",
        ),
    ]
