from django.core.management.base import BaseCommand, CommandError
from time import sleep
from apps.products.services import ProductService

class Command(BaseCommand):
    
    def handle(self, **options):
        while True:
            service = ProductService()
            print('Starting sync...')
            response = service.sync_iapp()
            print(response)
            print('Sync finished!')
            sleep(3600)