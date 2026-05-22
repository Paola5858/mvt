import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
import django
django.setup()
from api_telemetria.models import MedicaoVeiculo
from django.db.models import Count

print('count', MedicaoVeiculo.objects.count())
print('tipo counts:', list(MedicaoVeiculo.objects.values('medicao__tipo').annotate(c=Count('id')).order_by('-c')))
for tipo in MedicaoVeiculo.objects.values_list('medicao__tipo', flat=True).distinct():
    qs = MedicaoVeiculo.objects.filter(medicao__tipo=tipo).order_by('-valor')[:5]
    print('tipo', tipo)
    for item in qs:
        print(' ', item.id, item.data, item.valor)
