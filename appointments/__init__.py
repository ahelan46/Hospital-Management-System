def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    if 'doctor' in self.data:
        try:
            doctor_id = int(self.data.get('doctor'))
            self.fields['slot'].queryset = TimeSlot.objects.filter(
                doctor_id=doctor_id,
                is_booked=False
            )
        except (ValueError, TypeError):
            pass
    else:
        self.fields['slot'].queryset = TimeSlot.objects.none()
