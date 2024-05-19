from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("name", "profile_image")

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.profile_image.name = f"{instance.profile_image.name.split('.')[0]}.png"
        if commit:
            instance.save()
        return instance


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields
