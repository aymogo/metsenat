from rest_framework import generics
from sponsors import models
from sponsors import serializers


class SponsorListView(generics.ListAPIView):
    queryset = models.Sponsor.objects.all()
    serializer_class = serializers.SponsorListSerializer


class StudentListView(generics.ListAPIView):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentListSerializer


class DonationListView(generics.ListAPIView):
    queryset = models.Donation.objects.all()
    serializer_class = serializers.DonationListSerializer
