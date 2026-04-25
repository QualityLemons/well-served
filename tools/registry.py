from importlib import import_module


TOOL_CATALOG = {
    'impromptu-networking': {
        'class': 'tools.implementations.ImpromptNetworkingTool',
        'form_class': 'tools.forms.ImpromptNetworkingForm',
        'title': 'Impromptu Networking',
        'icon': 'handshake',
        'category': 'Facilitation',
        'what': (
            'Tap a deep well of curiosity and talent by helping the group '
            'focus on problems they want to solve. Loose yet powerful '
            'connections are formed in 20 minutes.'
        ),
        'how': (
            'Three rounds of pair conversations (4–5 min each). Before you '
            'begin, write down your challenge and what you hope to get and '
            'give. Find a new partner for each round.'
        ),
        'why': (
            'Initiate participation immediately. Attract deeper engagement '
            'around challenges, invite stories to deepen as they are repeated, '
            'and affirm that little things can make a big difference.'
        ),
        'example_input': {
            'challenge': 'A challenge I bring is…',
            'give_and_get': 'I hope to get… and give…',
            'round_one': 'In Round 1 I heard…',
            'round_two': 'In Round 2 I noticed…',
            'round_three': 'In Round 3 the pattern I saw was…',
        },
        'display_fields': [
            'challenge',
            'give_and_get',
            'round_one',
            'round_two',
            'round_three',
            'word_count',
        ],
        'timer_seconds': 1200,
    },
    '1-2-4-all': {
        'class': 'tools.implementations.OneTwoFourAllTool',
        'form_class': 'tools.forms.OneTwoFourAllForm',
        'title': '1-2-4-All',
        'icon': 'people-group',
        'category': 'Facilitation',
        'what': (
            'Engage everyone simultaneously in generating questions, ideas, '
            'and suggestions — regardless of group size.'
        ),
        'how': (
            'Work through four timed phases: 1 min of silent self-reflection, '
            '2 min in pairs, 4 min in foursomes, then 5 min sharing one '
            'standout idea with the whole group.'
        ),
        'why': (
            'Ideas and solutions are sifted rapidly. Participants own the '
            'ideas, so follow-up and implementation is simplified — no '
            'buy-in strategies needed.'
        ),
        'example_input': {
            'self_reflection': 'One opportunity I see is…',
            'pair_ideas': 'Together we noticed…',
            'foursome_ideas': 'Our group built on the idea that…',
            'standout_idea': 'The idea that stood out most was…',
        },
        'display_fields': [
            'self_reflection',
            'pair_ideas',
            'foursome_ideas',
            'standout_idea',
            'word_count',
        ],
        'timer_seconds': 720,
    },
    'i-am-and-i-like': {
        'class': 'tools.implementations.IAmAndILikeTool',
        'form_class': 'tools.forms.IAmAndILikeForm',
        'title': 'I am and I like',
        'icon': 'smile',
        'category': 'Low-Risk Warm-ups',
        'what': (
            'The group stands or sits in a circle, facing inwards.'
        ),
        'how': (
            'Going around the circle everyone says their first name, '
            'together with something they like or do not like or both.'
        ),
        'why': 'Keep working on breaking the ice.',
        'example_input': {
            'i_like': 'walking in the rain',
            'i_do_not_like': 'cold coffee',
        },
        'display_fields': ['statement', 'i_like', 'i_do_not_like', 'word_count'],
        'timer_seconds': 60,
    },
    'idea-generation': {
        'class': 'tools.implementations.IdeaGenerationTool',
        'form_class': 'tools.forms.IdeaGenerationForm',
        'title': 'Idea Generation',
        'icon': 'lightbulb',
        'category': 'Facilitation',
        'how_to': (
            'Spend a minute writing down your individual reflection before '
            'sharing it with the group.'
        ),
        'example_input': {
            'initial_thought': 'A challenge I keep noticing is...',
        },
        'display_fields': ['initial_thought', 'word_count'],
        'timer_seconds': 60,
    },
    'five-structural-elements': {
        'class': 'tools.implementations.FiveStructuralElementsTool',
        'form_class': 'tools.forms.FiveStructuralElementsForm',
        'title': 'Five Structural Elements',
        'icon': 'brickpile',
        'category': 'Facilitation',
        'how_to': (
            'Rapidly share challenges and expectations, build new connections. '
            'Get into pairs.'
        ),
        'example_input': {
            'pair_one_challenge': 'A challenge I bring is...',
            'pair_one_hope': 'I hope to get... and give...',
            'pair_two_challenge': 'A challenge I bring is...',
            'pair_two_hope': 'I hope to get... and give...',
        },
        'display_fields': [
            'pair_one_challenge', 'pair_one_hope',
            'pair_two_challenge', 'pair_two_hope',
            'word_count',
        ],
        'timer_seconds': 1200,
    },
}


def _resolve_class(dotted_path):
    module_path, _, class_name = dotted_path.rpartition('.')
    return getattr(import_module(module_path), class_name)


def get_tool_instance(slug, input_data=None):
    """Fetch and initialize a tool by its slug."""
    info = TOOL_CATALOG.get(slug)
    if not info:
        return None
    tool_class = _resolve_class(info['class'])
    return tool_class(user_input=input_data)


def get_tool_form_class(slug):
    """Return the Django form class associated with a tool, or None."""
    info = TOOL_CATALOG.get(slug)
    if not info or 'form_class' not in info:
        return None
    return _resolve_class(info['form_class'])
