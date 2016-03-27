from django import forms
from .models import Board, Card, Task


class BoardForm(forms.ModelForm):

    class Meta:
        model = Board
        fields = ('title',)


class CardForm(forms.ModelForm):

    class Meta:
        model = Card
        fields = ('title',)


