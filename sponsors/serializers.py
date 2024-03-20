from rest_framework import serializers
from sponsors import models


class SponsorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sponsor
        fields = (
            "id",
            "fullname",
            "phone_number",
            "company_name",
            "sponsor_quantity",
            "spent_quantity",
            "status",
            "created_at",
        )


class StudentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = (
            "id",
            "fullname",
            "university_name",
            "study_type",
            "paid_quantity",
            "contract_quantity",
        )


class DonationListSerializer(serializers.ModelSerializer):
    sponsor = SponsorListSerializer(many=False, read_only=True)
    student = StudentListSerializer(many=False, read_only=True)
    class Meta:
        model = models.Donation
        fields = (
            "id",
            "student",
            "sponsor",
            "paid_quantity",
            "created_at",
        )
