from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Board, Card, Task
#from django.views.generic import TemplateView
from .forms import BoardForm, CardForm, MyRegistrationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login


def board_list(request):
    """
    Note:
        This function returns a list of all boards ordered by a date of creation.
        The later was created the board, the higher place it will take in the list.

    Args:
        request: Request.

    Returns:
        List of boards.

    """
    boards = Board.objects.order_by('-created_date')
    return render(request, 'rtt_app/board_list.html', {'boards': boards})


def board_detail(request, pk):
    """
    Note:
        This function returns the content of the board.
        The content includes cards with (or without) tasks.

    Args:
        request: Request.
        pk: Primary key.

    Returns:
        Content of the board.

    """
    board = get_object_or_404(Board, pk=pk)
    cards = Card.objects.order_by('created_date')
    return render(request, 'rtt_app/board_detail.html', {'board': board, 'cards': cards})


@login_required
def board_new(request):
    """
    Note:
        This function returns a new board and redirects user to it's page if the form is filled correctly.
        Otherwise, the user will remain on the page with the form.

    Args:
        request: Request.

    Returns:
        New board.

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
    Note:
        This function redirects the user to the page where he can edit the title of the board.
        And saves the changes.

    Args:
        request: Request.
        pk: Primary key.

    Returns:
        Edited board.

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
    Note:
        This function confirms the changes.

    Args:
        request: Request.
        pk: Primary key.

    Returns:
        Page of the board.

    """
    board = get_object_or_404(Board, pk=pk)
    board.publish()
    return redirect('rtt_app.views.board_detail', pk=pk)


@login_required
def board_remove(request, pk):
    """
    Note:
        This function deletes the board and returns the updated list of boards.

    Args:
        request: Request.
        pk: Primary key.

    Returns:
        List of boards.

    """
    board = get_object_or_404(Board, pk=pk)
    board.delete()
    return redirect('rtt_app.views.board_list')


@login_required
def card_create(request, pk):
    """
    Note:
        This function returns a new card.

    Args:
        request: Request.
        pk: Primary key.

    Returns:
        New card.

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
    Note:
        This function deletes a card.

    Args:
        request: Request.
        pk: Primary key.
        card_id: id of the card.

    Returns:
        Page of the board with an updated list of cards.

    """
    card = get_object_or_404(Card, pk=card_id)
    card.delete()
    return redirect('rtt_app.views.board_detail', pk=pk)


def registration(request):
    """
    Note:
        This function creates a new user.

    Args:
        request: Request.

    Returns:
        Registration form.

    """
    if request.method == "POST":
        user_form = MyRegistrationForm(request.POST)  # , instance=task)
        if user_form.is_valid():

            # UserProfile.objects.create_user(username=form.cleaned_data.get('username'),
            # password=form.cleaned_data.get('password'))
            new_email = user_form.clean_email()
            user_object = User.objects.create_user(
                                     password=user_form.cleaned_data.get('password1'),
                                     first_name=user_form.cleaned_data.get('first_name'),
                                     last_name=user_form.cleaned_data.get('last_name'),
                                     email=new_email,
                                     username=new_email.split('@')[0]
                                     )

            user = authenticate(username=user_form.cleaned_data.get('email').split('@')[0],
                                password=user_form.cleaned_data.get('password1')
                                )
            if user is not None:  # add check if exist
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                error_msg = "Try one more time, please"
                return render(request, 'registration/registration.html', {'form': user_form, 'error_msg': error_msg})
    else:
        user_form = MyRegistrationForm()
    return render(request, 'registration/registration.html', {'form': user_form})
