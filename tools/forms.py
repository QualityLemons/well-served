from django import forms


class IdeaGenerationForm(forms.Form):
    initial_thought = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Your individual reflection (1 min)...'}),
        label="Phase 1: Self-Reflection"
    )


class FiveStructuralElementsForm(forms.Form):
    pair_one_challenge = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What big challenge do you bring to this gathering?',
            'rows': 3,
        }),
        label="Pair Member One — Challenge",
    )
    pair_one_hope = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What do you hope to get from and give this group?',
            'rows': 3,
        }),
        label="Pair Member One — Hope",
    )
    pair_two_challenge = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What big challenge do you bring to this gathering?',
            'rows': 3,
        }),
        label="Pair Member Two — Challenge",
    )
    pair_two_hope = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What do you hope to get from and give this group?',
            'rows': 3,
        }),
        label="Pair Member Two — Hope",
    )
