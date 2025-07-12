from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random
from car.models import Car, CarType, CarFeature, Feature, CarBrand

fake = Faker()

BRAND_MODELS = {
    "Toyota": ["Corolla", "Camry", "RAV4", "Highlander", "Yaris"],
    "BMW": ["3 Series", "5 Series", "X3", "X5", "7 Series"],
    "Mercedes-Benz": ["C-Class", "E-Class", "GLA", "GLC", "S-Class"],
    "Ford": ["Focus", "Fiesta", "Escape", "Explorer", "F-150"],
    "Honda": ["Civic", "Accord", "CR-V", "Pilot", "Fit"],
    "Nissan": ["Altima", "Sentra", "Rogue", "Pathfinder", "Leaf"],
    "Hyundai": ["Elantra", "Tucson", "Santa Fe", "Sonata", "Kona"],
    "Kia": ["Sportage", "Sorento", "Optima", "Rio", "Seltos"],
    "Volkswagen": ["Golf", "Jetta", "Passat", "Tiguan", "Polo"],
    "Chevrolet": ["Malibu", "Equinox", "Cruze", "Tahoe", "Camaro"],
    "Mazda": ["Mazda3", "Mazda6", "CX-5", "CX-9", "MX-5"],
    "Jeep": ["Wrangler", "Cherokee", "Grand Cherokee", "Compass"],
    "Lexus": ["RX", "ES", "NX", "LS", "UX"],
    "Subaru": ["Impreza", "Outback", "Forester", "Crosstrek", "Legacy"],
    "Tesla": ["Model 3", "Model S", "Model X", "Model Y"],
    "Peugeot": ["208", "308", "3008", "508", "5008"],
    "Renault": ["Clio", "Captur", "Megane", "Kadjar", "Talisman"],
    "Audi": ["A3", "A4", "Q3", "Q5", "A6"],
    "Mitsubishi": ["Lancer", "Outlander", "ASX", "Pajero", "Mirage"],
    "Volvo": ["XC40", "XC60", "S60", "S90", "V60"]
}

class Command(BaseCommand):
    help = "Seed cars for each CarBrand with features"

    def handle(self, *args, **kwargs):
        car_type_ids = list(CarType.objects.values_list('id', flat=True))
        feature_ids = list(Feature.objects.values_list('id', flat=True))
        created = 0

        for brand in CarBrand.objects.all():
            model_list = BRAND_MODELS.get(brand.name, [fake.word().capitalize()])
            num_cars = random.randint(3, 8)

            for _ in range(num_cars):
                model_name = random.choice(model_list)
                car = Car.objects.create(
                    name=f"{brand.name} {model_name}",
                    car_type_id=random.choice(car_type_ids),
                    car_brand=brand,
                    condition=random.choice(['new', 'used']),
                    fuel_type=random.choice(['petrol', 'diesel', 'electric', 'hybrid']),
                    doors=random.choice([2, 3, 4, 5]),
                    year=random.randint(2012, 2023),
                    transmission=random.choice(['manual', 'automatic']),
                    color=random.choice(['black', 'white', 'gray', 'red', 'blue', 'silver', 'green']),
                    body=fake.word().capitalize() + " Body",
                    engine_capacity=round(random.uniform(1.2, 4.5), 1),
                    mileage=random.randint(10000, 150000),
                    price_per_day=round(random.uniform(30, 100), 2),
                    description=fake.paragraph(nb_sentences=5),
                    is_available=True,
                    created_at=timezone.now()
                )

                selected_features = random.sample(feature_ids, random.randint(30, 70))
                for fid in selected_features:
                    CarFeature.objects.create(car=car, feature_id=fid)

                created += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully created {created} car records."))

