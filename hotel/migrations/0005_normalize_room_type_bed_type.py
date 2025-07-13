from django.db import migrations

ROOM_TYPE_MAP = {
    "Single Room": "single",
    "Double Room": "double",
    "Twin Room": "twin",
    "Triple Room": "triple",
    "Quad Room": "quad",
    "Queen Room": "queen",
    "King Room": "king",
    "Standard Room": "standard",
    "Deluxe Room": "deluxe",
    "Superior Room": "superior",
    "Executive Room": "executive",
    "Junior Suite": "junior_suite",
    "Suite": "suite",
    "Penthouse Suite": "penthouse",
    "Family Room": "family",
    "Accessible Room": "accessible",
    "Studio": "studio",
    "Connecting Rooms": "connecting",
    "Presidential Suite": "presidential",
    "Executive Suite": "executive_suite",
}

BED_TYPE_MAP = {
    "King Bed": "king",
    "Queen Bed": "queen",
    "Twin Beds": "twin",
    "Double Bed": "double",
}

def forwards(apps, schema_editor):
    HotelRoom = apps.get_model("hotel", "HotelRoom")

    for room in HotelRoom.objects.all():
        room_type_cleaned = ROOM_TYPE_MAP.get(room.room_type.strip())
        bed_type_cleaned = BED_TYPE_MAP.get(room.bed_type.strip())

        if room_type_cleaned:
            room.room_type = room_type_cleaned
        if bed_type_cleaned:
            room.bed_type = bed_type_cleaned

        room.save()

def backwards(apps, schema_editor):
    pass  # Optional: you can add reverse mapping if needed

class Migration(migrations.Migration):

    dependencies = [
        ("hotel", "0004_alter_hotelroom_bed_type_alter_hotelroom_room_type"),  # replace with the real previous migration
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
