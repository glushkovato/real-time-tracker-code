from django import forms
from .models import Board, Card
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


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


class MyRegistrationForm(forms.ModelForm):
    """
    Note:
        A form for creating a new user.

    Attributes:
        email: User's email.
        first_name: User's name.
        last_name: User's surname.
        error_messages: These messages emerge if two password fields do not match, or the email address is not unique.
        password1: User's password.
        password2: The same password as password1 for verification.

    """
    email = forms.CharField(max_length=30, label='Your email')
    first_name = forms.CharField(max_length=30, label='Name')
    last_name = forms.CharField(max_length=30, label='Surname')

    error_messages = {
        'password_mismatch': "The two password fields do not match.",
        'email_mismatch': "Email address is not unique.",
    }

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)
    #help_text="Enter the same password as above, for verification."

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_password2(self):
        """
        Note:
            This function checks if both password fields are completed and both passwords match.

        Returns:
            User's password.

        Raises:
            ValidationError: If password1 is not equal to password2.

        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def clean_email(self):
        """
        Note:
            This function checks if the given email already exists in database.

        Returns:
            User's email.

        Raises:
            ValidationError: If email is not unique.

        """
        email = self.cleaned_data.get('email')
        username = email.split('@')[0]
        if email and User.objects.filter(email=email).exists():
            raise ValidationError(
                self.error_messages['email_mismatch'],
                code='email_mismatch')
        return email

    def save(self, commit=True):
        """
        Note:
            This function saves user's info in database.
            Info includes password and email.

        Returns:
            User.

        """
        user = super(MyRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
