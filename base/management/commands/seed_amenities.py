from django.core.management.base import BaseCommand
from base.models import Amenity
import random

class Command(BaseCommand):
    help = 'Seed Hotel room amenities with 100 realistic unique amenity names'

    def handle(self, *args, **kwargs):
        names = [
            "Free WiFi", "Air Conditioning", "Heating", "Flat-screen TV", "Cable/Satellite TV",
            "Room Service", "Mini-bar", "Coffee Maker", "Electric Kettle", "Tea/Coffee Supplies",
            "Complimentary Bottled Water", "Refrigerator", "Microwave", "In-room Safe", "Telephone",
            "Desk & Chair", "Hair Dryer", "Iron & Ironing Board", "Alarm Clock", "Wardrobe/Closet",
            "Blackout Curtains", "Soundproofing", "Bathrobes", "Slippers", "Premium Toiletries",
            "Towels", "Linens", "Bathtub", "Shower", "Toilet Paper", "Tissue Box",
            "Make-up Mirror", "Vanity Table", "Laundry Bag", "Free Parking", "Valet Parking",
            "Wake-up Service", "Daily Housekeeping", "Turn-down Service", "Smoke Detector",
            "Fire Extinguisher", "Carbon Monoxide Detector", "Balcony/Terrace", "City View",
            "Mountain View", "Pool View", "Desk Lamp", "Reading Lights", "USB Charging Ports",
            "Power Adapter", "Interconnecting Rooms", "Hypoallergenic Bedding", "Crib on Request",
            "Extra Pillows/Foam", "Pillow Menu", "In-room Dining Menu", "Mini Bar Snacks",
            "Snack Basket", "Ice Bucket & Tongs", "Turndown Cookies", "Snack Vending Machine Access",
            "Room Service App", "Mobile Key Entry", "In-room Tablet", "Streaming Services (Netflix etc.)",
            "Bluetooth Speaker", "USB Ports", "International TV Channels", "Flat-screen TV Streaming",
            "Yoga Mat (On Request)", "Fitness Equipment (In Room)", "In-room Safe",
            "Hair Styling Tools", "Universal Adapter", "Blackout Drapes", "LED Lighting Control",
            "Thermostat Control", "Air Purifier", "Humidifier", "Shower Cap", "Sewing Kit",
            "Umbrella (On Request)", "First Aid Kit", "Medication Kit (On Request)", "Pet Bed (Pet-friendly)",
            "Pet Bowls", "Baby Bathtub (On Request)", "On-demand Water Heater",
            "Mini Fridge", "In-room Pantry", "Microwave Oven", "Kitchenette", "Dishwasher (Extended Stay)",
            "Fireplace (Suite Only)", "Sofa Bed", "Extra Bed (On Request)", "Feather Duvet",
            "Sound System", "Video Game Console (On Request)", "VR Experience (Premium Rooms)",
            "In-room Spa Menu", "Massage Bed (Suite)", "In-room Safe"
        ]

        count = 0
        for name in names:
            obj, created = Amenity.objects.get_or_create(name=name)
            if created:
                count += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Created {count} unique amenities."))
