from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Board, Card, Task
#from django.views.generic import TemplateView
from .forms import BoardForm, CardForm
from django.contrib.auth.models import User


def board_list(request):

    """
    :param: request
    :return: list of boards

    This function returns a list of all boards ordered by a date of creation.
    The later was created the board, the higher place it will take in the list.

    """

    boards = Board.objects.order_by('-created_date')
    return render(request, 'rtt_app/board_list.html', {'boards': boards})


def board_detail(request, pk):

    """
    :param request:
    :param pk:
    :return: content of the board

    This function returns the content of the board.
    The content includes cards with (or without) tasks.

    """

    board = get_object_or_404(Board, pk=pk)
    cards = Card.objects.order_by('created_date')
    return render(request, 'rtt_app/board_detail.html', {'board': board, 'cards': cards})


@login_required
def board_new(request):

    """
    :param request:
    :return: new board

    This function returns a new board and redirects user to it's page if the form is filled correctly.
    Otherwise, the user will remain on the page with the form.

    """

    if request.method == "POST":
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.author = request.user
            board.published_date = timezone.now()
            board.save()
            return redirect('rtt_app.views.board_detail', pk=board.pk)
    else:
        form = BoardForm()
    return render(request, 'rtt_app/board_edit.html', {'form': form})


@login_required
def board_edit(request, pk):

    """
    :param request:
    :param pk:
    :return: edited board

    This function redirects the user to the page where he can edit the title of the board.
    And saves the changes.

    """

    board = get_object_or_404(Board, pk=pk)

    if request.method == "POST":
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            board = form.save(commit=False)
            board.author = request.user
            board.published_date = timezone.now()
            board.save()
            return redirect('rtt_app.views.board_detail', pk=board.pk)
    else:
        form = BoardForm(instance=board)
    return render(request, 'rtt_app/board_edit.html', {'form': form})

# @login_required
# def post_draft_list(request):
#     posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
#     return render(request, 'rtt_app/post_draft_list.html', {'posts': posts})


@login_required
def board_publish(request, pk):

    """
    :param request:
    :param pk:
    :return: page of the board

    This function confirms the changes.

    """

    board = get_object_or_404(Board, pk=pk)
    board.publish()
    return redirect('rtt_app.views.board_detail', pk=pk)


@login_required
def board_remove(request, pk):

    """
    :param request:
    :param pk:
    :return: list of boards

    This function deletes the board and returns the updated list of boards.

    """

    board = get_object_or_404(Board, pk=pk)
    board.delete()
    return redirect('rtt_app.views.board_list')


@login_required
def card_create(request, pk):

    """
    :param request:
    :param pk:
    :return: new card

    This function returns a new card.

    """

    board = get_object_or_404(Board, pk=pk)
    if request.method == "POST":
        form = CardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.board = board
            card.save()
            return redirect('rtt_app.views.board_detail', pk=pk)
    else:
        form = CardForm()
    return render(request, 'rtt_app/card_create.html', {'form': form})


# def card_list(request):
#     cards = Card.objects.order_by('-created_date')
#     return render(request, 'rtt_app/board_detail.html', {'cards': cards})


@login_required
def card_remove(request, pk, card_id):

    """
    :param request:
    :param pk:
    :param card_id:
    :return: page of the board

    This function deletes a card.
    Returns a page of the board with an updated list of cards.

    """

    card = get_object_or_404(Card, pk=card_id)
    card.delete()
    return redirect('rtt_app.views.board_detail', pk=pk)
