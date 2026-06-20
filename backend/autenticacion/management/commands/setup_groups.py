from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Configura los grupos de usuarios necesarios para el sistema de joyería'

    def handle(self, *args, **options):
        self.stdout.write('🔧 Configurando grupos de usuarios...')
        
        # Crear grupo 'Clientes'
        clientes_group, created = Group.objects.get_or_create(name='Clientes')
        if created:
            self.stdout.write(
                self.style.SUCCESS('✅ Grupo "Clientes" creado exitosamente')
            )
        else:
            self.stdout.write(
                self.style.WARNING('ℹ️ Grupo "Clientes" ya existe')
            )
        
        # Crear grupo 'Empleados' (para futuros flujos)
        empleados_group, created = Group.objects.get_or_create(name='Empleados')
        if created:
            self.stdout.write(
                self.style.SUCCESS('✅ Grupo "Empleados" creado exitosamente')
            )
        else:
            self.stdout.write(
                self.style.WARNING('ℹ️ Grupo "Empleados" ya existe')
            )
        
        # Crear grupo 'Administradores' (para futuros flujos)
        admin_group, created = Group.objects.get_or_create(name='Administradores')
        if created:
            self.stdout.write(
                self.style.SUCCESS('✅ Grupo "Administradores" creado exitosamente')
            )
        else:
            self.stdout.write(
                self.style.WARNING('ℹ️ Grupo "Administradores" ya existe')
            )
        
        self.stdout.write(
            self.style.SUCCESS('🎉 Configuración de grupos completada')
        ) 