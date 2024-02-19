from django.core.validators import ValidationError
from django import forms


RADIO_CHOICES = (
    ("Value One", "Value One Display"),
    ("Value Two", "Text For Value Two"),
    ("Value Three", "Value Three's Display Text")
)

BOOK_CHOICES = (
    (
        "Non-Fiction", (
           ("1", "Deep Learning with Keras"),
           ("2", "Web Development with Django")
        )
    ),
    (
        "Fiction", (
           ("3", "Brave New World"),
           ("4", "The Great Gatsby")
        )
    )
)

def validate_email_domain(value):
    if value.split("@")[-1].lower() != "example.com":
        raise ValidationError("The email address must be on the domain example.com.")


class ExampleForm(forms.Form):
    text_input = forms.CharField(max_length=3)
    password_input = forms.CharField(min_length=8, widget=forms.PasswordInput)
    checkbox_on = forms.BooleanField()
    radio_input = forms.ChoiceField(choices=RADIO_CHOICES, widget=forms.RadioSelect)
    favorite_book = forms.ChoiceField(choices=BOOK_CHOICES)
    books_you_own = forms.MultipleChoiceField(required=False, choices=BOOK_CHOICES)
    text_area = forms.CharField(widget=forms.Textarea)
    integer_input = forms.IntegerField(min_value=1, max_value=10)
    float_input = forms.FloatField()
    decimal_input = forms.DecimalField(max_digits=5, decimal_places=3)
    email_input = forms.EmailInput()
    date_input = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    hidden_input = forms.CharField(widget=forms.HiddenInput, initial="Hidden Value")

class OrderForm(forms.Form):
    magazine_count = forms.IntegerField(min_value=0, max_value=80,
                                        widget=forms.NumberInput(attrs={"placeholder": "Number of Magazines"}))
    book_count = forms.IntegerField(min_value=0, max_value=50,
                                    widget=forms.NumberInput(attrs={"placeholder": "Number of Books"}))
    send_confirmation = forms.BooleanField(required=False)
    email = forms.EmailField(required=False, validators=[validate_email_domain],
                             widget=forms.EmailInput(attrs={"placeholder": "Your company email address"}))

    def clean_email(self):
        return self.cleaned_data["email"].lower()

    def clean(self):
        clean_data = super().clean()
        if clean_data["send_confirmation"] and not clean_data.get("email"):
           self.add_error("email", "Please enter an email address to receive the confirmation message.")
        elif clean_data.get("email") and not clean_data["send_confirmation"]:
           self.add_error("send_confirmation", "Please check this if you want to receive a confirmation email.")

        item_total = clean_data.get("magazine_count", 0) + clean_data.get("book_count", 0)
        if item_total > 100:
            self.add_error(None, "The total number of items must be 100 or less.")


class NewsletterSignupForm(forms.Form):
    signup = forms.BooleanField(label="Sign up to newsletter?", required=False)
    email = forms.EmailField(help_text="Enter your email address to subscribe", required=False)

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data["signup"] and not cleaned_data.get("email"):
            self.add_error("email", "Your email address is required if signing up for the newsletter.")