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
        queryset = Country.objects.filter(name__icontains=country_name) if country_name else Country.objects.all()

        # Serialize the queryset
        serializer = CountrySerializer(queryset, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = CountrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
