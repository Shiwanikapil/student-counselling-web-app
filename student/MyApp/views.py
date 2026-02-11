from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from datetime import datetime
from MyApp.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User  
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login  # ✅ Rename import to avoid conflict
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from .models import StudentCounselling
import os

#from .forms import Information

# Home page
def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        desc = request.POST.get('desc')
        contact = Contact(name=name, email=email, desc=desc, date=datetime.today())
        contact.save()
        messages.success(request, "Your message has been sent!")
    return render(request, 'contact.html')


# Student login
def login_view(request):
    if request.method == "POST":
        username= request.POST.get("username")
        password = request.POST.get("password")

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)  # ✅ Correct login function
            messages.success(request, "You have logged in successfully!")
            return redirect("dashboard")  # ✅ URL name match kare
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login.html')

@login_required
def dashboard(request):
    if request.method == 'POST':
        # form data fetch
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        highschool_name = request.POST.get('highschool_name')
        intermediate_name = request.POST.get('intermediate_name')
        father_name = request.POST.get('father_name')
        mother_name = request.POST.get('mother_name')
        dob = request.POST.get('dob')

        hs_hindi = int(request.POST.get('hs_hindi') or 0)
        hs_english = int(request.POST.get('hs_english') or 0)
        hs_social_science = int(request.POST.get('hs_social_science') or 0)
        hs_science = int(request.POST.get('hs_science') or 0)
        hs_math = int(request.POST.get('hs_math') or 0)

        inter_hindi = int(request.POST.get('inter_hindi') or 0)
        inter_english = int(request.POST.get('inter_english') or 0)
        inter_physics = int(request.POST.get('inter_physics') or 0)
        inter_chemistry = int(request.POST.get('inter_chemistry') or 0)
        inter_math = int(request.POST.get('inter_math') or 0)

        pref1 = request.POST.get('pref1')
        pref2 = request.POST.get('pref2')

        StudentCounselling.objects.create(
            name=name,
            email=email,
            phone=phone,
            address=address,
            highschool_name=highschool_name,
            intermediate_name=intermediate_name,
            father_name=father_name,
            mother_name=mother_name,
            dob=dob,
            hs_hindi=hs_hindi,
            hs_english=hs_english,
            hs_social_science=hs_social_science,
            hs_science=hs_science,
            hs_math=hs_math,
            inter_hindi=inter_hindi,
            inter_english=inter_english,
            inter_physics=inter_physics,
            inter_chemistry=inter_chemistry,
            inter_math=inter_math,
            pref1=pref1,
            pref2=pref2,
            status="Pending", 
            payment_status="Not Paid"  # default payment status 
        )

        messages.success(request, 'Thanks for submission of your counselling form!')
        return redirect('pending')
    #return redirect('dashboard.html') 
    return render(request, 'dashboard.html')
    #return redirect('dashboard')
@login_required
def pending(request):
    student = StudentCounselling.objects.filter(email=request.user.email).last()
    return render(request, 'pending.html', {'student': student})
@login_required
def make_payment(request, student_id):
    student = get_object_or_404(StudentCounselling, id=student_id)
    student.payment_status = "Paid"

    # ===== Generate Admission Letter PDF =====
    from reportlab.pdfgen import canvas
    from django.core.files import File
    import tempfile

    # Temporary file create karo
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(temp.name)

    # Letter content
    c.setFont("Helvetica-Bold", 22)
    c.drawString(150, 800, "ADMISSION LETTER")

    c.setFont("Helvetica", 12)
    c.drawString(100, 760, f"Date: {datetime.today().strftime('%d-%m-%Y')}")
    c.drawString(100, 730, f"Dear {student.name},")
    c.drawString(100, 710, "Congratulations! We are pleased to inform you that you are selected ")
    c.drawString(100, 695, "that your application for admission has been approved for computer scienceWhere")
    c.drawString(100, 675, f"Course Preference 1: {student.pref1}")
    c.drawString(100, 660, f"Course Preference 2: {student.pref2}")
    c.drawString(100, 630, "Please keep this letter for your records.")
    c.drawString(100, 610, "We look forward to seeing you soon!")

    c.drawString(100, 570, "Sincerely,")
    c.drawString(100, 555, "Admissions Office")

    # Save PDF
    c.showPage()
    c.save()

    # Save PDF to model field
    student.admission_letter.save(f"admission_letter_{student.id}.pdf", File(open(temp.name, "rb")))
    temp.close()

    # Save student data
    student.save()

    messages.success(request, "Payment successful! Your admission letter is ready for download.")
    return redirect('pending')

@login_required
def download_letter(request, student_id):
    student = get_object_or_404(StudentCounselling, id=student_id)
    if student.admission_letter:
        file_path = student.admission_letter.path
        file_name = f"admission_letter_{student.id}.pdf"
        return FileResponse(open(file_path, 'rb'), as_attachment=True,filename=file_name,content_type='application/pdf')
    else:
        messages.error(request, "Admission letter not available yet.")
        return redirect('pending')



def signup(request):
    return render(request, 'signup.html') 
