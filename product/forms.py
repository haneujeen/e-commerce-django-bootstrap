from .models import Review
from django import forms

class ReviewForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(ReviewForm, self).__init__(*args, **kwargs)
    self.fields['content'].label = 'Review '
    self.fields['content'].widget.attrs = {'rows': 5}
    self.fields['content'].widget.attrs['placeholder'] = '리뷰를 남겨주세요.'

  class Meta:
      model = Review
      fields = ('content',)

class ChildCommentForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(ReviewForm, self).__init__(*args, **kwargs)
    self.fields['content'].label = 'Review '
    self.fields['content'].widget.attrs = {'rows': 5}
    self.fields['content'].widget.attrs['placeholder'] = '리뷰를 남겨주세요.'

  class Meta:
      model = Review
      fields = ('content',)