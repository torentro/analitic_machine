from django import forms
from .models import *
from sympy import *
import numpy as np



class DifferentiationForm(forms.Form):
    function = forms.CharField(max_length=100)
    order = forms.IntegerField()

    function.widget.attrs.update({'class': 'form-control'})
    order.widget.attrs.update({'class': 'form-control'})

    def clean_function(self):
        new_function = self.cleaned_data['function'].lower()

        return new_function



    def differentiat(self):
        differentiation = str(self.cleaned_data['function'])
        x = symbols('x')
        differentiation = diff(differentiation, x, self.cleaned_data['order'])
        return differentiation

    def dots_func(self):
        func = lambdify(symbols('x'), self.differentiat(), 'math')
        l = np.arange(-10, 10, 0.1)
        list_dots = [['x','y']]
        for i in l:
            list_dots.append([i,func(i)])

        return list_dots


    def save(self):
        new_differentiation = (
        Differentiation.objects.create(
        function=self.cleaned_data['function'],
        differentiation = self.differentiat(),
        order = self.cleaned_data['order'],
        user = 'user1')
        )

class ExstrapolationForm(forms.Form):
    dots = forms.CharField(max_length=100)
    x = forms.FloatField()

    dots.widget.attrs.update({'class': 'form-control'})
    x.widget.attrs.update({'class': 'form-control'})


    def clean_dots(self):
        new_dots = self.cleaned_data['dots'].lower()
        return new_dots

    def clean_x(self):
        new_x = self.cleaned_data['x']
        return new_x



    def extrapolatiat(self):
        dots = str(self.cleaned_data['dots'])
        x = self.cleaned_data['x']
        newdots = list(zip(*[list(map(float, i.split(','))) for i in dots.replace(' ','')[1:-1].split('),(')]))
        xi = newdots[0]
        yi = newdots[1]
        return lagrange_polynom(xi, yi)(x)

    def dots_func(self):
        dots = str(self.cleaned_data['dots'])
        x = self.cleaned_data['x']
        l = list(zip(*[list(map(float, i.split(','))) for i in dots.replace(' ','')[1:-1].split('),(')]))
        xi = l[0]
        yi = l[1]
        func = lagrange_polynom(xi, yi)
        dots = np.arange(x-10, x+10, 0.1)
        list_dots = [['x','y']]
        for i in dots:
            list_dots.append([i,func(i)])

        return list_dots


    def save(self):
        new_extrapolation = (
        Exstrapolation.objects.create(
        dots=self.cleaned_data['dots'],
        extrapolation = self.extrapolatiat(),
        x = self.cleaned_data['x'],
        user = 'user1')
        )




def lagrange_coeff(xi):
    denoms = []
    for index in range(len(xi)):
        denomination = 1
        for i in range(len(xi)):
            if i == index: continue
            denomination *= xi[index] - xi[i]
        denoms.append(denomination)

    def inner_lagrange_coeff(x):
        coeff = []
        for d in range(len(denoms)):
            numerator = 1
            for i  in range(len(xi)):
                if i == d: continue
                numerator *= x - xi[i]
            coeff.append( numerator / denoms[d] )
        return coeff
    return inner_lagrange_coeff

def lagrange_polynom(xi, yi):
    lc = lagrange_coeff(xi)
    def inner_lagrange_polynom(a):
        summ = 0
        for i in range(len(xi)):
            summ += yi[i] * lc(a)[i]
        return summ
    return inner_lagrange_polynom
