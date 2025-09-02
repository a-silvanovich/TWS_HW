from django.contrib import admin
from new_app.models import Table, Reservation


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['number', 'image', 'seats']
    list_editable = ('image', 'seats',)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['table', 'user', 'date', 'hour_start', 'hour_end', 'created_at']