import os

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Attendee,StallVisit,Stall
from django.contrib.auth import authenticate, login
from .forms import AttendeeForm,StallKeeperLoginForm
from django.contrib.auth.decorators import login_required
import qrcode
import uuid
from django.conf import settings
from django.http import JsonResponse

def home(request):
    return render(request, 'attendees/index.html')

def generate_qr_code(request):
    unique_id = str(uuid.uuid4())
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(unique_id)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Ensure the directory exists
    qr_code_dir = os.path.join(settings.STATIC_ROOT, 'qr_codes')
    os.makedirs(qr_code_dir, exist_ok=True)

    # Save the QR code image
    img_path = os.path.join(qr_code_dir, f"{unique_id}.png")
    img.save(img_path)


    #attendee = Attendee(unique_id=unique_id, qr_code=img_path)
    #attendee.save()

    return render(request, 'attendees/qr_code.html',
                  {'unique_id': unique_id, 'img_path': f'/static/qr_codes/{unique_id}.png'})
    '''return JsonResponse({'unique_id': unique_id,
                         'img_url': request.build_absolute_uri(settings.MEDIA_URL + 'qr_codes/' + f"{unique_id}.png")})'''


def scan_qr(request):
    # Handle QR code scanning logic to retrieve unique_id
    # Example: Get unique_id from the QR code scanning process

    unique_id = "your_unique_id_from_qr_scan"
    # Redirect to the attendee_form view with the unique_id
    return redirect('attendee_form', unique_id=unique_id)


def attendee_form(request, unique_id):
    attendee = Attendee.objects.filter(unique_id=unique_id).first()
    if attendee:
        return render(request, 'attendees/already_submitted.html')

    if request.method == 'POST':
        form = AttendeeForm(request.POST)
        if form.is_valid():
            attendee = form.save(commit=False)
            attendee.unique_id = unique_id
            attendee.save()
            return redirect('form_success')
    else:
        form = AttendeeForm()

    return render(request, 'attendees/form.html', {'form': form})

def check_in(request, unique_id):
    try:
        attendee = get_object_or_404(Attendee, unique_id=unique_id)
        if attendee.arrived:
            return redirect('already_arrived')
        attendee.arrived = True
        attendee.save()
        return redirect('arrival_success')

    except Attendee.DoesNotExist:
        return render(request, 'attendees/check_in_failed.html', {'message': 'Attendee not found'})


def form_success(request):
    return render(request, 'attendees/form_success.html')
def arrival_success(request):
    return render(request, 'attendees/arrival_success.html')

def already_arrived(request):
    return render(request, 'attendees/already_arrived.html')

def already_submitted(request):
    return render(request, 'attendees/already_submitted.html')

@login_required
def stall_keeper_login(request):
    if request.method == 'POST':
        form = StallKeeperLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('stall_dashboard')
    else:
        form = StallKeeperLoginForm()
    return render(request, 'attendees/stall_keeper_login.html', {'form': form})

@login_required
def stall_dashboard(request):
    return render(request, 'attendees/stall_dashboard.html')

@login_required
def scan_attendee(request, unique_id):
    try:
        attendee = Attendee.objects.get(unique_id=unique_id)
        stall = Stall.objects.get(keeper=request.user)
        StallVisit.objects.create(attendee=attendee, stall=stall)
        return render(request, 'attendees/scan_success.html', {'attendee': attendee, 'stall': stall})
    except Attendee.DoesNotExist:
        return render(request, 'attendees/scan_failed.html', {'message': 'Attendee not found'})
    except Stall.DoesNotExist:
        return render(request, 'attendees/scan_failed.html', {'message': 'Stall not found'})

