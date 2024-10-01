from celery import shared_task
from contracts.models import Contract


@shared_task
def update_contract_status():
    for contract in Contract.objects.all():
        contract.save()
