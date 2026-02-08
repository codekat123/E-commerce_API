from django import forms 


class SetPasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholders": "new passwords"}),
        min_length=8,
        label="new password"
    )