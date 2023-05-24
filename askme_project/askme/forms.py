from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Profile, Post, Answer


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}),
                               label="Your Username", max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
                               label="Password", max_length=50)

    def clean_password(self):
        data = self.cleaned_data['password']
        if len(data) < 8:
            raise ValidationError("Password must contain at least 8 characters.")
        return data

    def clean_username(self):
        data = self.cleaned_data['username']
        if len(data) < 3:
            raise ValidationError("Username must contain at least 3 characters.")
        return data


class RegistrationForm(forms.ModelForm):
    password_check = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
                                     label="Repeat password", max_length=50)
    avatar = forms.ImageField(label="Upload an avatar!", required=False)
    bio = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Write about yourself',  'rows': '3'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': "AskMe"}),
            'email': forms.EmailInput(attrs={'placeholder': "askme@mail.com"}),
            'password': forms.PasswordInput(attrs={'placeholder': 'yourmom'}),
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),

        }
        labels = {
            'username': "Username",
            'email': "Email",
            'first_name': "First Name",
            'last_name': "Last Name",
            'password': "Password",
            'bio': "Write whatever you want about yourself"
        }

    def clean_bio(self):
        data = self.data['bio']
        if len(data) > 500:
            raise ValidationError("Bio must be up to 500 characters.")
        return data

    def clean_password(self):
        data = self.data['password']
        if len(data) < 8:
            raise ValidationError("Password must contain at least 8 characters.")
        return data

    def clean_username(self):
        data = self.data['username']
        if len(data) < 4:
            raise ValidationError("Username must contain at least 4 characters.")
        return data

    def clean(self):
        password1 = self.cleaned_data['password']
        password2 = self.cleaned_data['password_check']

        if password1 != password2:
            raise ValidationError("Passwords do not match!")

        username_match = User.objects.filter(username=self.cleaned_data["username"])
        if self.instance:
            username_match = username_match.exclude(pk=self.instance.pk)

        if username_match.exists():
            raise ValidationError(f"User with username {self.cleaned_data['username']} already exists")

        return self.cleaned_data

    def save(self):
        avatar_ = self.cleaned_data['avatar']
        self.cleaned_data.pop('avatar')
        self.cleaned_data.pop('password_check')
        bio_ = self.cleaned_data['bio']
        self.cleaned_data.pop('bio')
        user = User.objects.create_user(**self.cleaned_data)
        user.save()
        profile = Profile.objects.create(user=user, avatar=avatar_, bio=bio_)
        profile.save()
        return user


class AskForm(forms.ModelForm):
    tags = forms.CharField()

    class Meta:
        model = Post
        fields = ['title', 'text', 'tags']

        widgets = {
            'title': forms.TextInput(),
            'text': forms.Textarea(attrs={'placeholder': "Detailed description"}),
            'tags': forms.TextInput(attrs={'placeholder': "Tags"})
        }

        labels = {
            'title': "Question header",
            'text': "Add a description to your question and write it in details.",
            'tags': "Add some tags!",
        }

    def clean_tags(self):
        data = self.data['tags']
        if len(data) > 30:
            raise ValidationError("Tags field length must be less than 30 characters")
        return data

    def clean_title(self):
        data = self.data['title']
        if len(data) > 100:
            raise ValidationError("Title length must be less than 100 characters")
        return data

    def clean_text(self):
        data = self.data['text']
        if len(data) > 5000:
            raise ValidationError("Question body must be less than 5000 characters")
        return data


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']

        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control mb-3', 'placeholder': 'Answer...', 'rows': '3'})
        }
        labels = {
            'text': 'Write your answer here!'
        }

    def clean_text(self):
        data = self.data['text']
        if len(data) > 5000:
            raise ValidationError("Answer body must be less than 5000 characters")
        return data


class EditForm(forms.ModelForm):
    avatar = forms.ImageField(label="Upload an avatar!", required=False)
    bio = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Write about yourself',  'rows': '3'}))

    original_username = None

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': "AskMe"}),
            'email': forms.EmailInput(attrs={'placeholder': "askme@mail.com"}),
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),

        }
        labels = {
            'username': "Username",
            'email': "Email",
            'first_name': "First Name",
            'last_name': "Last Name",
        }

    def clean_bio(self):
        data = self.data['bio']
        if len(data) > 500:
            raise ValidationError("Bio must be up to 500 characters.")
        return data

    def clean_username(self):
        data = self.data['username']
        if len(data) < 4:
            raise ValidationError("Username must contain at least 4 characters.")
        return data

    def clean(self):
        try:
            username_match = User.objects.filter(username=self.cleaned_data["username"])
        except Exception:
            pass
        else:
            if self.instance:
                username_match = username_match.exclude(pk=self.instance.pk)

            if username_match.exists():
                raise ValidationError(f"Username {self.cleaned_data['username']} already taken")

        return self.cleaned_data

    def save(self):
        user = super().save()
        profile = user.profile_related
        if self.cleaned_data['avatar']:
            profile.avatar = self.cleaned_data['avatar']
        profile.bio = self.cleaned_data['bio']
        profile.save()
        return user
