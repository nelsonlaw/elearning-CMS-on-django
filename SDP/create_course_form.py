from django import forms
from SDP.models import Category


class CourseInfoForm(forms.Form):
    title = forms.CharField(label='Course Title', max_length=127)
    description = forms.CharField(label='Course description', max_length=2000, widget=forms.Textarea)
    category = Category.objects.all()
    category = forms.ModelChoiceField(category)


class ModuleInfoForm(forms.Form):
    title = forms.CharField(label='Module Title', max_length=127)


class TextComponentInfoForm(forms.Form):
    title = forms.CharField(label='Component Title', max_length=127)
    content = forms.CharField(label='Content', max_length=2000, widget=forms.Textarea)


class ImageComponentInfoForm(forms.Form):
    title = forms.CharField(label='Component Title', max_length=127)
    content = forms.ImageField(label='Content')


class FileComponentInfoForm(forms.Form):
    title = forms.CharField(label='Component Title', max_length=127)
    content = forms.FileField(label='Content', allow_empty_file=True)


class VideoComponentInfoForm(forms.Form):
    title = forms.CharField(label='Component Title', max_length=127)
    content = forms.URLField(label='Youtube link')


class QuizComponentInfoForm(forms.Form):
    title = forms.CharField(label='Component Title', max_length=127)
    question = forms.CharField(label='Question', max_length=4096, widget=forms.Textarea)
    answer = forms.CharField(label='Answer', max_length=4096, widget=forms.Textarea)
