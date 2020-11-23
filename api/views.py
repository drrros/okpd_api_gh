from rest_framework import generics, status
from rest_framework.response import Response

from .models import Record
from .process_request import process_request
from .serializers import RecordSerializer


class ListRecord(generics.ListCreateAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer

    def create(self, request, *args, **kwargs):
        result = process_request(request.data.get('okpd'))
        if 'error' in result['status'].lower():
            return Response(result, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        serializer = RecordSerializer(Record.objects.get(okpd=request.data.get('okpd')))
        if result['status'] == 'Created':
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class DetailRecord(generics.RetrieveAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
