from django.contrib import admin
from MyApp.models import Contact 
from .models import StudentCounselling

# Register your models here.
@admin.register(StudentCounselling)
class StudentCounsellingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'total_highschool_marks', 'total_intermediate_marks', 'pref1', 'pref2', 'submitted_at','status', 'payment_status' )
    list_filter = ('pref1', 'pref2', 'submitted_at','status', 'payment_status')
    search_fields = ('name', 'email', 'phone', 'father_name', 'mother_name')
    readonly_fields = ('total_highschool_marks', 'total_intermediate_marks', 'submitted_at')
    list_editable = ('status', 'payment_status')  # Directly editable from list view 

    def save_model(self, request, obj, form, change):
        # Agar status Approved ho gaya aur letter pehle se nahi hai
        if obj.status == 'Approved' and not obj.admission_letter:
            from django.core.files.base import ContentFile
            from io import BytesIO
            from reportlab.pdfgen import canvas

            buffer = BytesIO()
            p = canvas.Canvas(buffer)
            p.drawString(100, 750, f"Admission Letter for {obj.name}")
            p.drawString(100, 730, f"Congratulations! You have been approved for admission.")
            p.drawString(100, 710, f"Branch Preference 1: {obj.pref1}")
            p.drawString(100, 690, f"Branch Preference 2: {obj.pref2}")
            p.showPage()
            p.save()

            buffer.seek(0)
            obj.admission_letter.save(f"{obj.name}_letter.pdf", ContentFile(buffer.read()), save=False)
        
        super().save_model(request, obj, form, change) 


    def total_highschool_marks(self, obj):
        return obj.total_highschool_marks()
    total_highschool_marks.short_description = 'Total HS Marks'

    def total_intermediate_marks(self, obj):
        return obj.total_intermediate_marks()
    total_intermediate_marks.short_description = 'Total Intermediate Marks'


admin.site.register(Contact)