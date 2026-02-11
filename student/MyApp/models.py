from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=120)
    desc = models.TextField()
    date = models.DateField()


class StudentCounselling(models.Model): 
    # Personal Details
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('Not Paid', 'Not Paid'),
        ('Paid', 'Paid'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default='Pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES,default='Not Paid')
    admission_letter = models.FileField(upload_to='admission_letters/', null=True, blank=True)

    name = models.CharField(max_length=100) 
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    highschool_name = models.CharField(max_length=100)
    intermediate_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    dob = models.DateField()

    # High School Marks
    hs_hindi = models.PositiveIntegerField()
    hs_english = models.PositiveIntegerField()
    hs_social_science = models.PositiveIntegerField()
    hs_science = models.PositiveIntegerField()
    hs_math = models.PositiveIntegerField()

    # Intermediate Marks
    inter_hindi = models.PositiveIntegerField()
    inter_english = models.PositiveIntegerField()
    inter_physics = models.PositiveIntegerField()
    inter_chemistry = models.PositiveIntegerField()
    inter_math = models.PositiveIntegerField()

    # Branch Preferences
    pref1 = models.CharField(max_length=50)
    pref2 = models.CharField(max_length=50)

    submitted_at = models.DateTimeField(auto_now_add=True)

    def total_highschool_marks(self):
        return self.hs_hindi + self.hs_english + self.hs_social_science + self.hs_science + self.hs_math

    def total_intermediate_marks(self):
        return self.inter_hindi + self.inter_english + self.inter_physics + self.inter_chemistry + self.inter_math

    def __str__(self):
        return self.name


