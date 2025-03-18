from django.core.management.base import BaseCommand
from apps.employees.models import Position

class Command(BaseCommand):
    help = 'Atualiza os nomes das posições que começam com "Gerente" para "Funcionário"'

    def handle(self, *args, **kwargs):
        # Filtra as posições que começam com "Gerente"
        positions_to_update = Position.objects.filter(position__startswith='Gerente')

        # Contador para mostrar quantos registros foram atualizados
        updated_count = 0

        for position in positions_to_update:
            # Substitui "Gerente" por "Funcionário de"
            old_name = position.position
            position.position = position.position.replace('Gerente', 'Funcionário', 1)
            position.save()
            updated_count += 1
            self.stdout.write(f'Atualizado: "{old_name}" ➔ "{position.position}"')

        # Mostra o resultado na saída padrão
        self.stdout.write(self.style.SUCCESS(f'{updated_count} posições atualizadas com sucesso!'))
