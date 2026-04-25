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


class TrizForm(forms.Form):
    worst_result_list = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'List everything you could do to guarantee the worst result '
                'imaginable for your top strategy or objective…'
            ),
            'rows': 5,
        }),
        label='Step 1 — How to guarantee the worst result (10 min)',
    )
    current_resemblances = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'Go through your list above item by item. '
                'What are you currently doing that in any way resembles those items? '
                'Be brutally honest…'
            ),
            'rows': 5,
        }),
        label='Step 2 — What we are currently doing that resembles that list (10 min)',
    )
    stop_first_steps = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'For each item above, what first steps will help you stop it? '
                'Frame as "I will stop…" or "We will stop…"'
            ),
            'rows': 4,
        }),
        label='Step 3 — First steps to stop counterproductive activities (10 min)',
    )


class AppreciativeInterviewsForm(forms.Form):
    success_story = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'Tell a story about a time when you worked on a challenge with others '
                'and you are proud of what you accomplished…'
            ),
            'rows': 5,
        }),
        label='Your success story (pairs, 15–20 min)',
    )
    success_conditions = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What made the success possible? What conditions or assets were at play?',
            'rows': 3,
        }),
        label='What made the success possible?',
    )
    partner_story = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'Retell your partner\'s story. '
                'What patterns in conditions or assets supporting success did you notice?'
            ),
            'rows': 4,
        }),
        label='Your partner\'s story and patterns noticed (groups of 4, 15 min)',
    )
    group_patterns = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Conditions and assets for success collected by the whole group…',
            'rows': 4,
        }),
        label='Whole-group patterns and conditions (10–15 min)',
    )
    opportunities = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'How are we investing in the assets and conditions that foster success? '
                'What opportunities do you see to do more?'
            ),
            'rows': 3,
        }),
        label='Opportunities to invest more (10 min)',
    )


class WickedQuestionsForm(forms.Form):
    individual_questions = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'Use the format: "How is it that we are ____ and we are ____ simultaneously?"\n'
                'Write one or more pairs of opposites that are at play in your work…'
            ),
            'rows': 5,
        }),
        label='Your Wicked Questions (individual, 5 min)',
    )
    group_question = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'The most impactful Wicked Question your small group selected…',
            'rows': 3,
        }),
        label='Small group\'s selected Wicked Question (5 min)',
    )
    whole_group_refinement = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'The most powerful questions and any further refinements from the whole group…',
            'rows': 4,
        }),
        label='Whole-group refinement (10 min)',
    )


class NineWhysForm(forms.Form):
    activities = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What do you do when working on this challenge? List your activities…',
            'rows': 3,
        }),
        label='Your activities',
    )
    why_chain = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': (
                'Record your answers as your partner asked "Why is that important to you?" '
                'up to nine times…'
            ),
            'rows': 5,
        }),
        label='Your why-chain (pairs interview, 10 min)',
    )
    fundamental_purpose = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'The deepest "why" you reached — the fundamental purpose of this work…',
            'rows': 2,
        }),
        label='Your fundamental purpose',
    )
    foursome_insights = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'What did your foursome share? What insights or patterns emerged?',
            'rows': 3,
        }),
        label='Foursome insights (5 min)',
    )
    group_reflection = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'How do our purposes influence the next steps we take?',
            'rows': 3,
        }),
        label='Whole-group reflection (5 min)',
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
