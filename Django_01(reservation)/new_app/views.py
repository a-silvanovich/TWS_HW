from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from new_app.models import Table, RegisterForm, ReservationForm, Reservation, TableFilterForm


def tables_list(request):
    form = TableFilterForm(request.GET or None)
    tables = Table.objects.all()
    if form.is_valid() and form.cleaned_data['seats'] is not None:
        tables = tables.filter(seats=int(form.cleaned_data['seats'])) if form.cleaned_data['seats'].isdigit() else tables
    return render(request, 'tables.html', {'tables': tables, 'form': form})

def base(request):
    return redirect('tables')

def register(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # email = form.cleaned_data['email']
            User.objects.create_user(username=username, email=None, password=password)
            return redirect(reverse("login"))

    return render(request, 'registration/register.html', {"form": form})

@login_required
def reserve_table(request, number):
    form = ReservationForm()
    table = get_object_or_404(Table, number=number)
    if request.method == 'POST':
        form = ReservationForm(request.POST, table=table, user=request.user)
        if form.is_valid():
            date = form.cleaned_data['date']
            hour_start = form.cleaned_data['hour_start']
            hour_end = form.cleaned_data['hour_end']
            Reservation.objects.create(table=table, user=request.user, date=date, hour_start=hour_start, hour_end=hour_end)
            messages.success(request, f'Стол №{table.number} успешно забронирован!')
            return redirect(reverse("profile"))
    return render(request, 'reservation.html', {'table': table, 'form': form})

@login_required
def profile_view(request):
    reservations = Reservation.objects.filter(user=request.user).select_related('table')
    return render(request, 'profile.html', {'user': request.user, 'reservations': reservations})

@login_required
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == 'POST':
        reservation.delete()
        messages.success(request, 'Бронирование успешно удалено.')
        return redirect('profile')
    return redirect('profile')