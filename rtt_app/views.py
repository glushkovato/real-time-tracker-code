from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Board, Card, Task # Поскольку views.py и models.py находятся в одной директории, мы можем использовать точку . и имя файла (без расширения .py)
#from django.views.generic import TemplateView
from .forms import BoardForm, CardForm

# Create your views here.


def board_list(request):
    boards = Board.objects.order_by('-created_date')
    return render(request, 'rtt_app/board_list.html', {'boards': boards})


def board_detail(request, pk):
    board = get_object_or_404(Board, pk=pk)
    cards = Card.objects.order_by('created_date')
    return render(request, 'rtt_app/board_detail.html', {'board': board, 'cards': cards})


@login_required
def board_new(request):
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
    board = get_object_or_404(Board, pk=pk)
    board.publish()
    return redirect('rtt_app.views.board_detail', pk=pk)


@login_required
def board_remove(request, pk):
    board = get_object_or_404(Board, pk=pk)
    board.delete()
    return redirect('rtt_app.views.board_list')


@login_required
def card_create(request, pk):
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
    card = get_object_or_404(Card, pk=card_id)
    card.delete()
    return redirect('rtt_app.views.board_detail', pk=pk)


#class IndexView(TemplateView):
    #template_name = 'index.html'
