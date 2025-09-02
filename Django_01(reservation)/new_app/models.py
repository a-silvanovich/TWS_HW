from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db import models
from django import forms

class Table(models.Model):
    number = models.IntegerField(unique=True, null=False, blank=False)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    seats = models.IntegerField(null=False, blank=False)

    class Meta:
        db_table = 'table'
        verbose_name = 'Table'
        verbose_name_plural = 'Tables'
        ordering = ['number']

class Reservation(models.Model):
    table = models.ForeignKey(Table, on_delete=models.RESTRICT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    hour_start = models.IntegerField()
    hour_end = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reservation'
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'
        ordering = ['date']

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date', 'hour_start', 'hour_end']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'hour_start': forms.NumberInput(attrs={'min': '8', 'max': '18'}),
            'hour_end': forms.NumberInput(attrs={'min': '8', 'max': '18'}),
        }

    def __init__(self, *args, table=None, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.table = table
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        hour_start = cleaned_data.get('hour_start')
        hour_end = cleaned_data.get('hour_end')
        date = cleaned_data.get('date')
        # Проверка, что не выбрана дата раньше, чем сегодня
        if date and date < date.today():
            raise forms.ValidationError("Дата бронирования не может быть раньше сегодняшнего дня.")
        # Проверка, что у пользователя нет других бронирований на эту дату
        if self.user and date:
            existing_reservations = Reservation.objects.filter(
                user=self.user,
                date=date
            ).exclude(id=self.instance.id if self.instance and self.instance.id else None)
            if existing_reservations.exists():
                raise forms.ValidationError("У вас уже есть бронирование на эту дату.")
        # Проверка диапазона часов
        if hour_start is not None and (hour_start < 8 or hour_start > 18):
            raise forms.ValidationError("Час начала должен быть от 8 до 18.")
        if hour_end is not None and (hour_end < 8 or hour_end > 18):
            raise forms.ValidationError("Час окончания должен быть от 8 до 18.")
        # Проверка, что hour_end > hour_start
        if hour_start is not None and hour_end is not None and hour_end <= hour_start:
            raise forms.ValidationError("Час окончания должен быть позже часа начала.")
        # Проверка пересечения бронирований
        if self.table and date and hour_start is not None and hour_end is not None:
            overlapping = Reservation.objects.filter(
                table=self.table,
                date=date,
                hour_start__lt=hour_end,
                hour_end__gt=hour_start
            ).exclude(id=self.instance.id if self.instance else None).exists()
            if overlapping:
                raise forms.ValidationError("Стол занят в указанное время.")
        return cleaned_data

class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput(), required=True)

    class Meta:
        model = User
        fields = ["username", "password"]
        widgets = {
            "password": forms.PasswordInput(),
        }

    def clean_password(self):
        password = self.cleaned_data.get("password")
        validate_password(password)
        return password

    def clean(self):
        """Валидация всей формы, автоматически вызывается."""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password and password2 and password != password2:
            self.add_error("password2", "Пароли не совпадают")

        return cleaned_data

# class TableFilterForm(forms.Form):
#     seats = forms.IntegerField(
#         required=False,
#         label='Количество мест',
#         widget=forms.NumberInput(attrs={'min': 1, 'placeholder': 'Введите количество мест'}),
#     )

# class TableFilterForm(forms.Form):
#     seats = forms.ChoiceField(
#         choices=[('', 'Все')] + [(i, i) for i in Table.objects.values_list('seats', flat=True).distinct()],
#         required=False,
#         label='Количество мест',
#     )

class TableFilterForm(forms.Form):
    seats = forms.ChoiceField(
        required=False,
        label='Количество мест',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Динамически получаем уникальные значения seats
        seats_choices = [(str(seats), str(seats)) for seats in sorted(set(Table.objects.values_list('seats', flat=True)))]
        self.fields['seats'].choices = [('', 'Все')] + seats_choices