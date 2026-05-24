from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Person
from .forms import PersonForm


# Получение данных из БД (Главная страница)
def index(request):
    form = PersonForm()
    # Сортируем по id в обратном порядке (-id), чтобы новые записи сразу появлялись сверху
    people = Person.objects.all().order_by('-id')
    return render(request, 'index.html', {'form': form, 'people': people})


# Сохранение данных в БД через AJAX (Только POST-запросы)
@require_POST
def create(request):
    form = PersonForm(request.POST)
    if form.is_valid():
        person = form.save()
        return JsonResponse({
            'success': True,
            'person': {'id': person.id, 'name': person.name, 'age': person.age}
        })

    # Возвращаем ошибки формы в формате словаря {'имя_поля': ['сообщение_об_ошибке']}
    return JsonResponse({'success': False, 'errors': form.errors.get_json_data()}, status=400)


# Изменение данных в БД через AJAX (GET — получить данные для модалки, POST — сохранить)
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
        # Возвращаем ошибки для модального окна редактирования
        return JsonResponse({'success': False, 'errors': form.errors.get_json_data()}, status=400)

    return JsonResponse({
        'id': person.id,
        'name': person.name,
        'age': person.age
    })


# Удаление данных из БД через AJAX (Только POST-запросы для безопасности)
@require_POST
def delete(request, id):
    person = get_object_or_404(Person, id=id)
    person.delete()
    return JsonResponse({'success': True, 'id': id})

def finance(request, id):
    # Находим конкретного сотрудника по id или отдаем 404, если его нет
    person = get_object_or_404(Person, id=id)
    return render(request, 'finance.html', {'person': person})