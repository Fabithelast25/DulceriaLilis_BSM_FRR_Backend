from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('Panel_Usuarios', '0005_alter_usuario_managers'),  # <-- ajusta si tu último es otro
    ]
    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE `usuario` MODIFY COLUMN `area_id` BIGINT NULL;",
            reverse_sql="ALTER TABLE `usuario` MODIFY COLUMN `area_id` BIGINT NOT NULL;",
        ),
        migrations.RunSQL(
            sql="ALTER TABLE `usuario` MODIFY COLUMN `rol_id`  BIGINT NULL;",
            reverse_sql="ALTER TABLE `usuario` MODIFY COLUMN `rol_id`  BIGINT NOT NULL;",
        ),
    ]
