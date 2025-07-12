from car.models import *
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Seed the database with 30 realistic CarType entries'

    def handle(self, *args, **kwargs):
        types = [
            "Sedan", "Hatchback", "Station Wagon", "Coupe", "Convertible",
            "Sports Car", "Muscle Car", "SUV", "Crossover", "Minivan",
            "Van", "Pickup Truck", "Electric", "Hybrid", "Diesel",
            "Luxury Sedan", "Compact SUV", "Full-size SUV", "Off-Road SUV",
            "Sports Utility Truck", "Roadster", "Microcar", "City Car",
            "Kei Car", "Subcompact Car", "Mid-size Car", "Grand Tourer",
            "Limousine", "Supercar", "Targa"
        ]

        created = 0
        for name in types:
            obj, was_created = CarType.objects.get_or_create(name=name)
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(
            f"✅ Successfully added {created} unique CarType entries."
        ))
