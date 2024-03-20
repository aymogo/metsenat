from django.db import models
from django.core.exceptions import ValidationError


class Sponsor(models.Model):
    STATUS_CHOICES = (
        ("yangi", "Yangi"),
        ("bekor", "Bekor"),
        ("moderatsiyada", "Moderatsiyada"),
        ("tasdiqlangan", "Tasdiqlangan"),
    )
    fullname = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=128)
    company_name = models.CharField(max_length=256)
    sponsor_quantity = models.IntegerField()
    spent_quantity = models.IntegerField(default=0)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fullname


class Student(models.Model):
    STUDY_TYPE = (
        ("bakalavr", "Bakalavr"),
        ("magistr", "Magistr"),
    )
    fullname = models.CharField(max_length=128)
    university_name = models.CharField(max_length=128)
    study_type = models.CharField(max_length=16, choices=STUDY_TYPE)
    paid_quantity = models.IntegerField(default=0)
    contract_quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.fullname


class Donation(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="sponsors"
    )
    sponsor = models.ForeignKey(
        Sponsor, on_delete=models.CASCADE, related_name="students"
    )
    paid_quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        student_left = (
            self.student.contract_quantity - self.student.paid_quantity
        )
        sponsor_left = (
            self.sponsor.sponsor_quantity - self.sponsor.spent_quantity
        )
        donation_max_amount = min(student_left, sponsor_left)
        if student_left == 0:
            raise ValidationError(
                f"You cannot donate this for this student\n\
                  This student recieved required amount."
            )
        elif sponsor_left == 0:
            raise ValidationError(
                f"Your balance is empty, please top up your balance."
            )
        elif self.paid_quantity > donation_max_amount:
            raise ValidationError(
                f"You cannot donate this amount\n\
                  You can only pay maximum {donation_max_amount}"
            )

    def save(self, *args, **kwargs):
        self.sponsor.sponsor_quantity -= self.paid_quantity
        self.sponsor.spent_quantity += self.paid_quantity
        self.sponsor.save()

        self.student.paid_quantity += self.paid_quantity
        self.student.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.fullname} got {self.paid_quantity} from {self.sponsor.fullname}"
