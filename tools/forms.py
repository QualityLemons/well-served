from django import forms


class IdeaGenerationForm(forms.Form):
    initial_thought = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Your individual reflection (1 min)...'}),
        label="Phase 1: Self-Reflection"
    )


class IAmAndILikeForm(forms.Form):
    i_like = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'I like…',
            'rows': 2,
        }),
        label="I like…",
        required=False,
    )
    i_do_not_like = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'I do not like…',
            'rows': 2,
        }),
        label="I do not like…",
        required=False,
    )


class ImpromptNetworkingForm(forms.Form):
    challenge = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What big challenge do you bring to this gathering?',
            'rows': 3,
        }),
        label='Your challenge',
    )
    give_and_get = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What do you hope to get from and give this group or community?',
            'rows': 3,
        }),
        label='What you hope to get and give',
    )
    round_one = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What did you hear, share, or notice in Round 1?',
            'rows': 3,
        }),
        label='Round 1 notes (4–5 min)',
    )
    round_two = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What did you hear, share, or notice in Round 2?',
            'rows': 3,
        }),
        label='Round 2 notes (4–5 min)',
    )
    round_three = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What did you hear, share, or notice in Round 3?',
            'rows': 3,
        }),
        label='Round 3 notes (4–5 min)',
    )


class OneTwoFourAllForm(forms.Form):
    self_reflection = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What opportunities do YOU see for making progress on this challenge?',
            'rows': 3,
        }),
        label='Phase 1 — Self-reflection (1 min)',
    )
    pair_ideas = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Ideas generated with your pair partner…',
            'rows': 3,
        }),
        label='Phase 2 — Pair ideas (2 min)',
    )
    foursome_ideas = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Ideas and themes that emerged in your group of four…',
            'rows': 3,
        }),
        label='Phase 3 — Foursome ideas (4 min)',
    )
    standout_idea = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What is one idea that stood out in your conversation?',
            'rows': 2,
        }),
        label='Phase 4 — Standout idea for whole group (5 min)',
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
