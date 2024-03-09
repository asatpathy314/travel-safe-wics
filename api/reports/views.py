from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Country
from reports.api.serializer import CountrySerializer
from rest_framework import status

class CountryView(APIView):
    def get(self, request):
        # Get the country name from the query parameters
        country_name = request.query_params.get('name', None)

        # If country_name is provided, filter the queryset; otherwise, return all countries
        queryset = Country.objects.filter(name__icontains=country_name) if country_name else None

        # Serialize the queryset
        serializer = CountrySerializer(queryset, many=True)

        return Response(serializer.data)