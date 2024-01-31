from django import forms


class AddRide(forms.Form):
    from_place = forms.CharField(max_length=30, min_length=2)
    to_place = forms.CharField(max_length=30, min_length=2)
    ride_datetime = forms.SplitDateTimeField()
    seats_count = forms.IntegerField(min_value=1)
    price = forms.IntegerField(min_value=0)


class SearchRide(forms.Form):
    template_name = 'main/search_form_snippet.html'

    from_place = forms.CharField(max_length=30, min_length=2, widget=forms.TextInput(attrs={'placeholder': 'pipka'}))
    to_place = forms.CharField(max_length=30, min_length=2)
    ride_date = forms.DateField()
    person_count = forms.IntegerField(min_value=1)
