from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Board(models.Model):
    """
    Note:
        User can make multiple boards.

    Attributes:
        author: Name of the user who created the board.
        title: Title of the board.
        created_date: Date of creation.
        published_date: (unused).

    """
    author = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    text = models.TextField(null=True)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        """
        Note:
            The publish method saves the board.

        """
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        """
        Note:
            The __str__ method returns the title of the board.

        """
        return self.title


class Card(models.Model):
    """
    Note:
        Each card refers to a specific board.
        One card can not belong to two boards at the same time.
        Each board can contain multiple cards.

    Attributes:
        board: ForeignKey(id of the board).
        title: Title of the card.
        text: Extra text field (unused).
        created_date: Date of creation.

    """
    board = models.ForeignKey(Board, related_name='cards')
    title = models.CharField(max_length=50)
    text = models.TextField(blank=False)
    created_date = models.DateTimeField(default=timezone.now)

    def publish(self):
        """
        Note:
            The publish method saves the card.

        """
        self.save()

    def __str__(self):
        """
        Note:
            The __str__ method returns the title of the card.

        """
        return self.title


class Task(models.Model):
    """
    Note:
        Each task refers to a specific card.
        One task can not belong to two cards at the same time.
        Each card can contain multiple tasks.

    Attributes:
        card: ForeignKey(id of the card).
        title: Title of the task.
        deadline: By this time the task should be done.

    """
    card = models.ForeignKey(Card, related_name='tasks')
    title = models.CharField(max_length=200)
    # text = models.TextField()
    # created_date = models.DateTimeField(default=timezone.now)
    deadline = models.DateField(blank=True, null=True)

    def publish(self):
        """
        Note:
            The publish method saves the task.

        """
        self.save()

    def __str__(self):
        """
        Note:
            The __str__ method returns the title of the task.

        """
        return self.title
