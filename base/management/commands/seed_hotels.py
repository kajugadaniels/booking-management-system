from django.core.management.base import BaseCommand
from base.models import Hotel
from faker import Faker
import random

fake = Faker()

# Realistic hotel base entries for Rwanda
RWANDA_HOTELS = [
    {"name": "Kigali Marriott Hotel", "province": "Kigali City", "district": "Nyarugenge", "sector": "Nyarugenge"},
    {"name": "Hotel des Mille Collines", "province": "Kigali City", "district": "Nyarugenge", "sector": "Nyarugenge"},
    {"name": "Ubumwe Grande Hotel", "province": "Kigali City", "district": "Gasabo", "sector": "Remera"},
    {"name": "Lake Kivu Serena Hotel", "province": "Western", "district": "Rubavu", "sector": "Gisenyi"},
    {"name": "Tiloreza Volcanoes Ecolodge", "province": "Northern", "district": "Musanze", "sector": "Nyange"},
    {"name": "Da Vinci Gorilla Lodge", "province": "Northern", "district": "Musanze", "sector": "Kinigi"},
    {"name": "Nyungwe House by One&Only", "province": "Western", "district": "Nyamasheke", "sector": "Bushekeri"},
    {"name": "Galaxy Hotel", "province": "Kigali City", "district": "Gasabo", "sector": "Kacyiru"},
    {"name": "Lemigo Hotel", "province": "Kigali City", "district": "Gasabo", "sector": "Kimihurura"},
    {"name": "Mantis Kivu Marina Bay Hotel", "province": "Western", "district": "Rusizi", "sector": "Kamembe"},
    {"name": "Heaven Boutique Hotel", "province": "Kigali City", "district": "Nyarugenge", "sector": "Kiyovu"},
    {"name": "Five to Five Hotel", "province": "Kigali City", "district": "Gasabo", "sector": "Remera"},
    {"name": "The Retreat", "province": "Kigali City", "district": "Nyarugenge", "sector": "Kiyovu"},
    {"name": "Urban by CityBlue", "province": "Kigali City", "district": "Gasabo", "sector": "Kacyiru"},
    {"name": "Hotel Chez Lando", "province": "Kigali City", "district": "Gasabo", "sector": "Remera"},
    {"name": "Kivu Peace View Hotel", "province": "Western", "district": "Rubavu", "sector": "Gisenyi"},
    {"name": "Gorilla Volcanoes Hotel", "province": "Northern", "district": "Musanze", "sector": "Kinigi"},
    {"name": "Golden Monkey Hotel", "province": "Northern", "district": "Musanze", "sector": "Kinigi"},
    {"name": "Inzozi Lodge", "province": "Southern", "district": "Huye", "sector": "Ngoma"},
    {"name": "Rebero Eco Lodge", "province": "Southern", "district": "Huye", "sector": "Tumba"},
    {"name": "Hakuna Matata Lodge", "province": "Eastern", "district": "Kayonza", "sector": "Rukara"},
    {"name": "Eastland Hotel", "province": "Eastern", "district": "Ngoma", "sector": "Kibungo"},
    {"name": "Moriah Hill Resort", "province": "Western", "district": "Karongi", "sector": "Bwishyura"},
    {"name": "Bethany Hotel", "province": "Western", "district": "Karongi", "sector": "Bwishyura"},
    {"name": "Silent Hill Hotel", "province": "Northern", "district": "Burera", "sector": "Rugarama"},
    {"name": "Kivu Lodge", "province": "Western", "district": "Nyamasheke", "sector": "Bushenge"},
    {"name": "Amahoro Guest House", "province": "Northern", "district": "Musanze", "sector": "Cyuve"},
    {"name": "Discover Rwanda Hostel", "province": "Kigali City", "district": "Gasabo", "sector": "Kacyiru"},
    {"name": "Hill View Hotel", "province": "Eastern", "district": "Rwamagana", "sector": "Kigabiro"},
    {"name": "Stipp Hotel", "province": "Western", "district": "Rubavu", "sector": "Gisenyi"},
    {"name": "Golf Hills Residence", "province": "Kigali City", "district": "Gasabo", "sector": "Nyarutarama"},
]

class Command(BaseCommand):
    help = 'Seed hotels with realistic data for Rwanda'

    def handle(self, *args, **kwargs):
        total_to_create = 40
        created = 0

        while created < total_to_create:
            source = random.choice(RWANDA_HOTELS)

            Hotel.objects.create(
                name = f"{source['name']} {fake.city_suffix().capitalize()} {random.randint(100,999)}",
                description=fake.paragraph(nb_sentences=6),
                stars=random.randint(3, 5),
                address=fake.street_address(),
                map_url=fake.url(),

                country="Rwanda",
                province=source["province"],
                district=source["district"],
                sector=source["sector"],
                cell=fake.word().capitalize() + " Cell",
                village=fake.word().capitalize() + " Village",

                phone_number=fake.phone_number(),
                email=fake.company_email(),
                website=fake.url(),

                is_active=True
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Successfully created {created} hotel records."))
