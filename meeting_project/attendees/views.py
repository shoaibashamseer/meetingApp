import os

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Attendee
from .forms import AttendeeForm
import qrcode
import uuid
from django.conf import settings
from django.http import JsonResponse

def home(request):
    return render(request, 'attendees/home.html')
def generate_qr_code(request):
    '''    unique_id = str(uuid.uuid4())
    return render(request, 'attendees/qr_code.html', {'unique_id': unique_id})
    img = qrcode.make(unique_id)
    img.save(f"static/qr_codes/{unique_id}.png")'''

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