import os
from django.shortcuts import render, redirect, get_object_or_404
<<<<<<< HEAD
from .models import Attendee,StallVisit,Profile,Person
from django.contrib.auth import authenticate, login
from .forms import AttendeeForm,PersonForm,AttendeeVerificationForm, PersonVerificationForm,UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
=======
from .models import Attendee,StallVisit,Stall
from django.contrib.auth import authenticate, login
from .forms import AttendeeForm,StallKeeperLoginForm
from django.contrib.auth.decorators import login_required
>>>>>>> 85a187678478d2f08d8ecfc2ee6880f581ccf9bb
import qrcode
import uuid
from django.urls import reverse
from django.conf import settings
from django.contrib import messages


def home(request):
    return render(request, 'attendees/index.html')
<<<<<<< HEAD

def generate_qr_code(request):
    qr_codes = []

    for i in range(1):
        unique_id = str(uuid.uuid4())
        form_url =  request.build_absolute_uri(reverse('attendee_form', args=[unique_id]))
=======

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
>>>>>>> 85a187678478d2f08d8ecfc2ee6880f581ccf9bb

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        #qr.add_data(unique_id)
        qr.add_data(form_url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")


        qr_code_dir = os.path.join(settings.STATIC_ROOT, 'qr_codes')
        os.makedirs(qr_code_dir, exist_ok=True)

        # Save the QR code image
        img_path = os.path.join(qr_code_dir, f"{unique_id}.png")
        img.save(img_path)


        qr_codes.append({'unique_id': unique_id, 'img_path': f'/static/qr_codes/{unique_id}.png'})


    return render(request, 'attendees/qr_code.html', {'qr_codes': qr_codes})


def scan_qr(request):
    # Handle QR code scanning logic to retrieve unique_id
    # Example: Get unique_id from the QR code scanning process

    unique_id = "your_unique_id_from_qr_scan"
    # Redirect to the attendee_form view with the unique_id
    return redirect('attendee_form', unique_id=unique_id)


def attendee_form(request, unique_id):

   # attendee = Attendee.objects.filter(unique_id=unique_id).first()
    attendee = Attendee.objects.filter(unique_id__startswith=unique_id[:5]).first()


    if attendee:
        return render(request, 'attendees/already_submitted.html',{'attendee':attendee})

    num_persons = 0
    person_forms = [PersonForm(prefix=f'person_{i}') for i in range(num_persons)]

    if request.method == 'POST':
        attendee_form = AttendeeForm(request.POST)
        num_persons = int(request.POST.get('num_persons', 0))
        person_forms = [PersonForm(request.POST, prefix=f'person_{i}') for i in range(num_persons)]

        if attendee_form.is_valid() and all(pf.is_valid() for pf in person_forms):
            print("Attendee form and person forms are valid")
            attendee = attendee_form.save(commit=False)
            attendee.unique_id = unique_id
            attendee.num_persons = num_persons
            attendee.save()

            for i in range(num_persons):
                person_form = person_forms[i]
                person = person_form.save(commit=False)
                person.attendee = attendee
                person.save()

            return redirect('form_success')
        else:
            print("Form validation failed")
            for pf in person_forms:
                if not pf.is_valid():
                    print(f"Person form {pf.prefix} errors: {pf.errors}")

    else:
        attendee_form = AttendeeForm()
        person_forms = [PersonForm(prefix='person_0')]

    return render(request, 'attendees/form.html', {'attendee_form': attendee_form,'person_forms': person_forms,'unique_id': unique_id})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'attendees/register.html', {'form': form})

def custom_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                try:
                    profile = user.profile

                except Profile.DoesNotExist:
                    messages.error(request, "You are not registered. Please register first.")
                    return render(request, 'attendees/login.html', {'form': form})


                if user.profile.role in ['stall_keeper', 'watchman']:
                    login(request, user)
                    return redirect('scan_qr_code')
                else:
                    messages.error(request, "You are not registered as a watchman or stall keeper. Please register first.")
                    return redirect('register')
            else:
                messages.error(request, "Invalid username or password.")

    else:
        form = AuthenticationForm()
    return render(request, 'attendees/login.html', {'form': form})


@login_required
def check_in(request, unique_id):
    try:
        #attendee = get_object_or_404(Attendee, unique_id=unique_id)
        attendee = Attendee.objects.filter(unique_id__startswith=unique_id[:5]).first()
        persons = Person.objects.filter(attendee=attendee)

        if attendee.arrived:
            return redirect('watchman_dashboard',unique_id=attendee.unique_id)

        if request.method == 'POST':
            attendee_form = AttendeeVerificationForm(request.POST, instance=attendee)
            person_forms = [PersonVerificationForm(request.POST, instance=person, prefix=str(person.id)) for person in persons]

            if attendee_form.is_valid() and all(pf.is_valid() for pf in person_forms):

                attendee_form.instance.name_verified = request.POST.get('name_verified') == 'on'
                attendee_form.instance.place_verified = request.POST.get('place_verified') == 'on'
                attendee_form.instance.job_verified = request.POST.get('job_verified') == 'on'
                attendee_form.instance.gender_verified = request.POST.get('gender_verified') == 'on'
                attendee_form.instance.phone_verified = request.POST.get('phone_verified') == 'on'
                attendee_form.instance.email_verified = request.POST.get('email_verified') == 'on'
                attendee_form.instance.arrived = True
                attendee.save()
                attendee_form.save()

                for pf in person_forms:
                    pf.save()

                return redirect('watchman_dashboard',unique_id=attendee.unique_id)
        else:
            attendee_form = AttendeeVerificationForm(instance=attendee)
            person_forms = [PersonVerificationForm(instance=person, prefix=str(person.id)) for person in persons]

        return render(request, 'attendees/check_in.html', {
            'attendee_form': attendee_form,
            'person_forms': person_forms,
            'attendee': attendee,

        })
    except  Attendee.DoesNotExist:
        return render(request, 'attendees/check_in_failed.html', {'message': 'Attendee not found'})


def form_success(request):
    return render(request, 'attendees/form_success.html')

def arrival_success(request):
    return render(request, 'attendees/arrival_success.html')

def already_arrived(request):
    return render(request, 'attendees/already_arrived.html')

def already_submitted(request):
    return render(request, 'attendees/already_submitted.html')

<<<<<<< HEAD

@login_required
def scan_qr_code(request):
    return render(request, 'attendees/scan_qr_code.html')


@login_required
def watchman_dashboard(request,unique_id):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'watchman':
        return redirect('login')

    #attendee = get_object_or_404(Attendee, unique_id=unique_id)
    attendee = Attendee.objects.filter(unique_id__startswith=unique_id[:5]).first()
    persons = Person.objects.filter(attendee=attendee)


    return render(request, 'attendees/watchman_dashboard.html', {
        'attendee': attendee,
        'persons': persons,
    })
=======
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
>>>>>>> 85a187678478d2f08d8ecfc2ee6880f581ccf9bb

@login_required
def scan_attendee(request, unique_id):
    try:
<<<<<<< HEAD
        #attendee = Attendee.objects.get(unique_id=unique_id)
        attendee = Attendee.objects.filter(unique_id__startswith=unique_id[:5]).first()
        user_profile = request.user.profile

        if user_profile.role == 'stall_keeper':
            existing_visit = StallVisit.objects.filter(attendee=attendee, stall=request.user).first()

            if not existing_visit:
                StallVisit.objects.create(attendee=attendee, stall=request.user)
            #return redirect('scan_qr_code')
            return redirect('stall_dashboard')

        elif user_profile.role == 'watchman':
            return redirect('check_in', unique_id=unique_id)

    except Attendee.DoesNotExist:
        return render(request, 'attendees/scan_failed.html', {'message': 'Attendee not found'})
    except StallVisit.DoesNotExist:
        print("Error creating StallVisit")
        return render(request, 'attendees/scan_failed.html', {'message': 'Stall not found'})

@login_required
def stall_dashboard(request):

    try:
        visits = StallVisit.objects.filter(stall=request.user)
        return render(request, 'attendees/stall_dashboard.html', {'visits': visits})

    except StallVisit.DoesNotExist:
        return render(request, 'attendees/stall_dashboard.html', {'error': 'Stall not found for this user.'})

=======
        attendee = Attendee.objects.get(unique_id=unique_id)
        stall = Stall.objects.get(keeper=request.user)
        StallVisit.objects.create(attendee=attendee, stall=stall)
        return render(request, 'attendees/scan_success.html', {'attendee': attendee, 'stall': stall})
    except Attendee.DoesNotExist:
        return render(request, 'attendees/scan_failed.html', {'message': 'Attendee not found'})
    except Stall.DoesNotExist:
        return render(request, 'attendees/scan_failed.html', {'message': 'Stall not found'})

>>>>>>> 85a187678478d2f08d8ecfc2ee6880f581ccf9bb
