from car.models import *
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Seed the database with 20 popular car brands'

    def handle(self, *args, **kwargs):
        brands = [
            "Toyota", "Honda", "Ford", "Chevrolet", "BMW",
            "Mercedes-Benz", "Audi", "Volkswagen", "Hyundai", "Nissan",
            "Kia", "Subaru", "Jeep", "Tesla", "Lexus",
            "Mazda", "Volvo", "Porsche", "Jaguar", "Land Rover"
        ]

        created = 0
        for name in brands:
            obj, was_created = CarBrand.objects.get_or_create(name=name)
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Successfully created {created} car brands."))
