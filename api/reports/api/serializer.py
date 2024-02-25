from rest_framework import serializers
from reports.models import *

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['name', 'criminality_index', 'travel_safety_report', 'health_report', 'vaccines', 'diseases']
