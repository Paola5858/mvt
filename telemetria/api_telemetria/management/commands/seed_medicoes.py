"""
Script para gerar dados de medição realistas para testes.
Uso: python manage.py seed_medicoes --days=30 --records-per-day=100
"""
import random
from datetime import datetime, timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from api_telemetria.models import MedicaoVeiculo, Veiculo, Medicao


class Command(BaseCommand):
    help = 'Gera dados de medição realistas para testes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Número de dias para gerar dados (padrão: 30)',
        )
        parser.add_argument(
            '--records-per-day',
            type=int,
            default=50,
            help='Número de registros por dia (padrão: 50)',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Limpar dados existentes antes de gerar',
        )

    def handle(self, *args, **options):
        days = options['days']
        records_per_day = options['records_per_day']
        clear = options['clear']

        # Limpar dados existentes se solicitado
        if clear:
            count = MedicaoVeiculo.objects.count()
            MedicaoVeiculo.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'Deletados {count} registros existentes'))

        # Verificar se há veículos e medições
        veiculos = list(Veiculo.objects.all())
        medicoes = list(Medicao.objects.all())

        if not veiculos:
            self.stdout.write(self.style.ERROR('Nenhum veículo cadastrado. Crie veículos primeiro.'))
            return

        if not medicoes:
            self.stdout.write(self.style.ERROR('Nenhuma medição cadastrada. Crie medições primeiro.'))
            return

        self.stdout.write(f'Gerando {days} dias x {records_per_day} registros/dia = {days * records_per_day} total')
        self.stdout.write(f'Veículos: {len(veiculos)} | Medições: {len(medicoes)}')

        # Gerar dados
        registros = []
        data_inicio = timezone.now() - timedelta(days=days)

        for dia in range(days):
            data_dia = data_inicio + timedelta(days=dia)

            for _ in range(records_per_day):
                veiculo = random.choice(veiculos)
                medicao = random.choice(medicoes)

                # Gerar valores realistas por tipo de medição
                if medicao.tipo == 'combustivel':
                    valor = Decimal(str(round(random.uniform(10, 60), 2)))  # 10-60 litros
                elif medicao.tipo == 'odometro':
                    valor = Decimal(str(round(random.uniform(50000, 150000), 2)))  # 50k-150k km
                elif medicao.tipo == 'horimetro':
                    valor = Decimal(str(round(random.uniform(1000, 5000), 2)))  # 1k-5k horas
                else:
                    valor = Decimal(str(round(random.uniform(0, 100), 2)))

                # Variar a hora do dia
                hora = random.randint(0, 23)
                minuto = random.randint(0, 59)
                segundo = random.randint(0, 59)
                data_completa = data_dia.replace(hour=hora, minute=minuto, second=segundo)

                registros.append(
                    MedicaoVeiculo(
                        veiculo=veiculo,
                        medicao=medicao,
                        data=data_completa,
                        valor=valor,
                    )
                )

        # Inserir em lotes para melhor performance
        batch_size = 1000
        for i in range(0, len(registros), batch_size):
            batch = registros[i : i + batch_size]
            MedicaoVeiculo.objects.bulk_create(batch)
            self.stdout.write(f'  ... {i + len(batch)} registros inseridos')

        self.stdout.write(
            self.style.SUCCESS(f'\n✅ {len(registros)} registros criados com sucesso!')
        )
        self.stdout.write(f'Período: {data_inicio.date()} até {(data_inicio + timedelta(days=days)).date()}')
