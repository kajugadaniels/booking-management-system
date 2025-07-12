from car.models import *
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Seed the database with 100 realistic car features'

    def handle(self, *args, **kwargs):
        features = [
            "Air Conditioning", "Leather Seats", "Bluetooth", "Backup Camera", "Cruise Control",
            "Sunroof", "Navigation System", "Keyless Entry", "Push Button Start", "Heated Seats",
            "Apple CarPlay", "Android Auto", "Blind Spot Monitoring", "Lane Departure Warning",
            "Adaptive Cruise Control", "Premium Sound System", "Alloy Wheels", "Fog Lights",
            "Remote Start", "Third Row Seating", "Tinted Windows", "Power Seats", "Memory Seats",
            "Dual-Zone Climate Control", "Rear Air Conditioning", "Parking Sensors", "Heads-Up Display",
            "Wireless Charging", "Ambient Lighting", "Rain-Sensing Wipers", "Automatic High Beams",
            "4WD/AWD", "Traction Control", "ABS", "Power Windows", "Power Mirrors", "Foldable Mirrors",
            "Leather-Wrapped Steering Wheel", "Voice Recognition", "Traffic Sign Recognition",
            "Collision Warning", "Rear Cross-Traffic Alert", "Split-Folding Rear Seats", "USB Ports",
            "Auxiliary Input", "HD Radio", "Satellite Radio", "Digital Instrument Cluster",
            "Power Liftgate", "Hands-Free Liftgate", "Roof Rails", "Tow Hitch", "Panoramic Roof",
            "Adjustable Pedals", "Surround View Camera", "Ventilated Seats", "Sport Mode", "Eco Mode",
            "Cup Holders", "Cargo Net", "Underfloor Storage", "Heated Steering Wheel", "Rear Spoiler",
            "Run Flat Tires", "LED Headlights", "Xenon Headlights", "Daytime Running Lights",
            "Automatic Emergency Braking", "Pre-Collision System", "Electronic Stability Control",
            "Driver Drowsiness Monitor", "Side Airbags", "Front Airbags", "Rear Airbags",
            "Knee Airbags", "ISOFIX Child Seat Anchors", "Tire Pressure Monitoring System",
            "Remote Trunk Release", "Rear Seat Reminder", "Adjustable Steering Column", "Armrest",
            "Manual Sunshade", "Digital Compass", "Cargo Cover", "Wireless Headphones", "Power Outlet",
            "Auto-Dimming Rearview Mirror", "Trip Computer", "Multi-Function Display",
            "Anti-Theft Alarm", "Immobilizer", "Brake Assist", "Hill Start Assist", "Hill Descent Control",
            "Drive Mode Selector", "Engine Start/Stop", "Front Fog Lamps", "Rear Fog Lamps", "Paddle Shifters"
        ]

        created = 0
        for name in features:
            obj, was_created = Feature.objects.get_or_create(name=name)
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(
            f"✅ Successfully added {created} car features."
        ))
