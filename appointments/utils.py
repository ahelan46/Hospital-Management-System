from datetime import datetime, timedelta
from .models import TimeSlot

def generate_slots(doctor, date, start_time, end_time, slot_minutes=15):

    current = datetime.combine(date, start_time)
    end = datetime.combine(date, end_time)

    slots = []

    while current < end:

        slot_end = current + timedelta(minutes=slot_minutes)

        slots.append(
            TimeSlot(
                doctor=doctor,
                date=date,
                start_time=current.time(),
                end_time=slot_end.time()
            )
        )

        current = slot_end

    TimeSlot.objects.bulk_create(slots)
