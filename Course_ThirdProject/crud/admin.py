from django.contrib import admin
from .models import Person, Finance


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'age')
    search_fields = ('name',)


@admin.register(Finance)
class FinanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'person', 'date', 'amount')
    list_filter = ('date',)
    search_fields = ('person__name',)
