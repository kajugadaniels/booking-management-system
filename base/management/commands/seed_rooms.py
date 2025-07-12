import random
from faker import Faker
from base.models import *
from django.core.management.base import BaseCommand

fake = Faker()

# Realistic room types from industry sources
ROOM_TYPES = [
    "Single Room", "Double Room", "Twin Room", "Triple Room", "Quad Room",
    "Queen Room", "King Room", "Standard Room", "Deluxe Room", "Superior Room",
    "Executive Room", "Junior Suite", "Suite", "Penthouse Suite", "Family Room",
    "Accessible Room", "Studio", "Connecting Rooms", "Presidential Suite", "Executive Suite"
]

class Command(BaseCommand):
    help = 'Seed HotelRoom records with realistic details per hotel, including amenities'

    def handle(self, *args, **kwargs):
        hotels = list(range(1, 47))  # hotel IDs from 1 to 46
        amenity_ids = list(Amenity.objects.values_list('id', flat=True))
        total_rooms = 0

        for hotel_id in hotels:
            num_rooms = random.randint(10, 23)
            # Determine hotel star-level for price tier (fetch from Hotel model)
            from base.models import Hotel
            hotel = Hotel.objects.get(id=hotel_id)
            min_price = 30 + (hotel.stars - 3) * 20
            max_price = 80 + (hotel.stars - 3) * 40

            for _ in range(num_rooms):
                room_type = random.choice(ROOM_TYPES)
                room_name = f"{room_type} {fake.word().capitalize()}"
                occupancy = \
                    1 if "Single" in room_type else \
                    2 if room_type in ["Double Room", "Queen Room", "King Room", "Standard Room", "Deluxe Room"] else \
                    3 if "Triple" in room_type else \
                    4 if "Quad Room" in room_type else random.randint(1, 4)

                room = HotelRoom.objects.create(
                    hotel_id=hotel_id,
                    name=room_name,
                    room_type=room_type,
                    description=fake.paragraph(nb_sentences=4),
                    bed_type=random.choice(["King Bed", "Queen Bed", "Twin Beds", "Double Bed"]),
                    occupancy=occupancy,
                    size=f"{random.randint(20, 60)} sqm",
                    price_per_night=round(random.uniform(min_price, max_price), 2),
                    refundable=random.choice([True, False]),
                    breakfast_included=random.choice([True, False]),
                    air_conditioning=True if hotel.stars >= 4 else False,
                    balcony=random.choice([True, False]),
                    is_available=True,
                )

                # assign 20–50 amenities
                chosen = random.sample(amenity_ids, k=random.randint(20, 50))
                for amenity_id in chosen:
                    RoomAmenity.objects.create(room=room, amenity_id=amenity_id)

                total_rooms += 1

        self.stdout.write(self.style.SUCCESS(
            f"✅ Created {total_rooms} rooms and amenities for {len(hotels)} hotels."
        ))
