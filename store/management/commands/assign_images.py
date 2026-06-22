from django.core.management.base import BaseCommand
from store.models import Product

class Command(BaseCommand):
    help = 'Assign media product images based on slug (media/products/<slug>.svg)'

    def handle(self, *args, **options):
        count = 0
        for p in Product.objects.all():
            filename = f'products/{p.slug}.svg'
            p.image.name = filename
            p.save()
            self.stdout.write(self.style.SUCCESS(f'Assigned {filename} to {p}'))
            count += 1
        self.stdout.write(self.style.SUCCESS(f'Updated {count} products'))
