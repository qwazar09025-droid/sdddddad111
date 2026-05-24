from django import forms
from .models import Person


INPUT_CLASS = (
    "w-full px-3.5 py-2 text-sm "
    "bg-slate-50 dark:bg-slate-800/60 "
    "border border-slate-200 dark:border-white/10 "
    "rounded-lg "
    "focus:outline-hidden focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 "
    "transition-all"
)


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'age']
        labels = {
            'name': 'Имя',
            'age': 'Возраст',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Например, Иван',
                'required': True,
                'autocomplete': 'off',
            }),
            'age': forms.NumberInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Возраст',
                'min': '0',
                'required': True,
            }),
        }

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is None:
            return age
        if age < 0:
            raise forms.ValidationError('Возраст не может быть отрицательным.')
        if age >= 80:
            raise forms.ValidationError('Столько не ЖИВУТ!')
        return age
