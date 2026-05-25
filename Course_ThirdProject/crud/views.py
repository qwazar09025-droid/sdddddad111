from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Person, Finance
from .forms import PersonForm, FinanceForm


# ============================ PERSON ============================

def index(request):
    form = PersonForm()
    people = Person.objects.all().order_by('-id')
    return render(request, 'index.html', {'form': form, 'people': people})


@require_POST
def create(request):
    form = PersonForm(request.POST)
    if form.is_valid():
        person = form.save()
        return JsonResponse({
            'success': True,
            'person': {'id': person.id, 'name': person.name, 'age': person.age}
        })
    return JsonResponse({'success': False, 'errors': form.errors.get_json_data()}, status=400)


def edit(request, id):
    person = get_object_or_404(Person, id=id)

    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True,
                'person': {'id': person.id, 'name': person.name, 'age': person.age}
            })
        return JsonResponse({'success': False, 'errors': form.errors.get_json_data()}, status=400)

    return JsonResponse({
        'id': person.id,
        'name': person.name,
        'age': person.age,
    })


@require_POST
def delete(request, id):
    person = get_object_or_404(Person, id=id)
    person.delete()
    return JsonResponse({'success': True, 'id': id})


# ============================ FINANCE ============================

def _finance_payload(item):
    return {
        'id': item.id,
        'person_id': item.person_id,
        'date': item.date.isoformat(),
        'amount': str(item.amount),
    }


def finance(request, id):
    person = get_object_or_404(Person, id=id)
    finances = person.finances.all()
    form = FinanceForm()
    return render(request, 'finance.html', {
        'person': person,
        'finances': finances,
        'form': form,
    })


@require_POST
def finance_create(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    form = FinanceForm(request.POST)
    if form.is_valid():
        item = form.save(commit=False)
        item.person = person
        item.save()
        return JsonResponse({'success': True, 'finance': _finance_payload(item)})
    return JsonResponse({'success': False, 'errors': form.errors.get_json_data()}, status=400)


def finance_edit(request, fid):
    item = get_object_or_404(Finance, id=fid)

    if request.method == 'POST':
        form = FinanceForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'finance': _finance_payload(item)})
        return JsonResponse({'success': False, 'errors': form.errors.get_json_data()}, status=400)

    return JsonResponse(_finance_payload(item))


@require_POST
def finance_delete(request, fid):
    item = get_object_or_404(Finance, id=fid)
    item.delete()
    return JsonResponse({'success': True, 'id': fid})
