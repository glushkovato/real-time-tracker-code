from django import forms
from .models import Board, Card


class BoardForm(forms.ModelForm):
    """
    Note:
        A form for creating a board.

    """
    class Meta:
        model = Board
        fields = ('title',)


class CardForm(forms.ModelForm):
    """
    Note:
        A form for creating a card.

    """
    class Meta:
        model = Card
        fields = ('title',)


