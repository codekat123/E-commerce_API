from django.shortcuts import render , redirect
from ...utils import get_user_from_token
from django.core.exceptions import ValidationError
from django.contrib import messages
from ...forms import SetPasswordForm

def staff_set_password_view(request,uuid,token):

    try:
        user = get_user_from_token(uuid,token)
    except ValidationError as e:
        messages.error(request,str(e))

    if request.method == "POST":
        if form.is_valid():
            form = SetPasswordForm(request.POST)
            user.set_password(form.cleaned_data['password'])
            user.is_active = True
            user.save()
            messages.success(request,'password set successfully your account is active')
            return render(request,"auth/staff_set_password.html",{'form':form})
        
        else:
            form = SetPasswordForm()

    return render(
        request,
        "auth/staff_set_password.html",
        {"form": form}
    )