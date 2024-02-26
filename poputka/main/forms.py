from django import forms


class SearchRide(forms.Form):
    from_place = forms.CharField(max_length=30, min_length=2)
    to_place = forms.CharField(max_length=30, min_length=2)
    ride_date = forms.DateField()
    person_count = forms.IntegerField(min_value=1)
