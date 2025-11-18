from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('Panel_Usuarios', '0006_make_area_nullable'),  # ajusta al último número en tu app
    ]
    operations = [
        migrations.RunSQL(
            sql="""
                -- Si existen las columnas, forzar NOT NULL con DEFAULT ''
                ALTER TABLE `usuario`
                MODIFY COLUMN `nombres`   varchar(150) NOT NULL DEFAULT '';
            """,
            reverse_sql="""
                ALTER TABLE `usuario`
                MODIFY COLUMN `nombres`   varchar(150) NOT NULL;
            """,
        ),
        migrations.RunSQL(
            sql="""
                ALTER TABLE `usuario`
                MODIFY COLUMN `apellidos` varchar(150) NOT NULL DEFAULT '';
            """,
            reverse_sql="""
                ALTER TABLE `usuario`
                MODIFY COLUMN `apellidos` varchar(150) NOT NULL;
            """,
        ),
    ]
