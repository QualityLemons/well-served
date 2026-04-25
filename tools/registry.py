from importlib import import_module


TOOL_CATALOG = {
    'triz': {
        'class': 'tools.implementations.TrizTool',
        'form_class': 'tools.forms.TrizForm',
        'title': 'TRIZ',
        'icon': 'trash-can',
        'category': 'Facilitation',
        'what': (
            'Clear space for innovation by challenging sacred cows safely. '
            'Invert your objective to expose what is actually holding progress back.'
        ),
        'how': (
            'Three steps, each 10 minutes, using 1-2-4-All within your group: '
            '(1) List all you could do to guarantee the worst result. '
            '(2) Identify what you are currently doing that resembles that list. '
            '(3) Decide on first steps to stop each counterproductive activity.'
        ),
        'why': (
            'Make it possible to speak the unspeakable and get skeletons out of '
            'the closet. Build trust by acting together to remove barriers and '
            'lay the ground for creative destruction in a seriously fun way.'
        ),
        'example_input': {
            'worst_result_list': (
                'Never share information across teams. '
                'Reward individual performance only. '
                'Hold endless meetings with no decisions.'
            ),
            'current_resemblances': (
                'We do silo our knowledge in separate drives. '
                'Our bonus structure is entirely individual.'
            ),
            'stop_first_steps': (
                'We will stop sending reports only to our own team. '
                'I will stop attending status meetings with no agenda.'
            ),
        },
        'display_fields': [
            'worst_result_list',
            'current_resemblances',
            'stop_first_steps',
            'word_count',
        ],
        'timer_seconds': 2100,
    },
    'appreciative-interviews': {
        'class': 'tools.implementations.AppreciativeInterviewsTool',
        'form_class': 'tools.forms.AppreciativeInterviewsForm',
        'title': 'Appreciative Interviews',
        'icon': 'comments',
        'category': 'Facilitation',
        'what': (
            'Generate the conditions essential for success by surfacing hidden '
            'success stories. Positive momentum springs from uncovering what '
            'works and why.'
        ),
        'how': (
            'In pairs, take turns interviewing each other about a proud success '
            'story and what made it possible (15–20 min). In groups of four, '
            'retell your partner\'s story and listen for patterns (15 min). '
            'Collect insights for the whole group, then discuss opportunities '
            'to invest more in those conditions (10–15 min + 10 min).'
        ),
        'why': (
            'Groups are energised sharing success stories rather than problems. '
            'Spontaneous momentum and insights for positive change are liberated '
            'as "hidden" stories are revealed and root causes of success identified.'
        ),
        'example_input': {
            'success_story': 'A time our team pulled together under pressure and delivered something we were proud of…',
            'success_conditions': 'Clear purpose, trust between members, and space to experiment.',
            'partner_story': 'My partner described a project where leadership stepped back and let the team lead…',
            'group_patterns': 'Psychological safety, shared ownership, and consistent communication appeared across stories.',
            'opportunities': 'We could invest more in regular reflection time and cross-team storytelling.',
        },
        'display_fields': [
            'success_story',
            'success_conditions',
            'partner_story',
            'group_patterns',
            'opportunities',
            'word_count',
        ],
        'timer_seconds': 3600,
    },
    'wicked-questions': {
        'class': 'tools.implementations.WickedQuestionsTool',
        'form_class': 'tools.forms.WickedQuestionsForm',
        'title': 'Wicked Questions',
        'icon': 'bolt',
        'category': 'Facilitation',
        'what': (
            'Articulate the paradoxical challenges a group must confront to succeed. '
            'Surface opposing-yet-complementary strategies that must be pursued simultaneously.'
        ),
        'how': (
            'Individually generate pairs of opposites using the format '
            '"How is it that we are ____ and we are ____ simultaneously?" (5 min). '
            'Small groups select their most impactful question (5 min). '
            'The whole group picks out the most powerful and refines them (10 min).'
        ),
        'why': (
            'Spark innovative action while diminishing "yes, but…" and "either-or" thinking. '
            'Bring to light paradoxical-yet-complementary forces that influence behaviours, '
            'especially during change efforts.'
        ),
        'example_input': {
            'individual_questions': (
                'How is it that we are deeply committed to our staff and we are '
                'constantly asking them to do more with less, simultaneously?'
            ),
            'group_question': (
                'How is it that we are focused on long-term strategy and we are '
                'reacting to short-term pressures, simultaneously?'
            ),
            'whole_group_refinement': (
                'The group sharpened this to: "How is it that we prize innovation '
                'and we reward compliance, simultaneously?"'
            ),
        },
        'display_fields': [
            'individual_questions',
            'group_question',
            'whole_group_refinement',
            'word_count',
        ],
        'timer_seconds': 1500,
    },
    'nine-whys': {
        'class': 'tools.implementations.NineWhysTool',
        'form_class': 'tools.forms.NineWhysForm',
        'title': 'Nine Whys',
        'icon': 'circle-question',
        'category': 'Facilitation',
        'what': (
            'Rapidly clarify for individuals and a group what is essentially '
            'important in their work by asking "Why?" up to nine times.'
        ),
        'how': (
            'In pairs, one partner interviews the other for 5 minutes — '
            'starting with activities, then asking "Why is that important?" '
            'repeatedly. Switch roles. Then share insights in a foursome, '
            'and finally reflect as a whole group.'
        ),
        'why': (
            'When a group discovers an unambiguous shared purpose, more freedom '
            'and responsibility are unleashed. You lay the foundation for '
            'spreading innovations with fidelity.'
        ),
        'example_input': {
            'activities': 'I facilitate workshops, write reports, coordinate teams…',
            'why_chain': 'Because it helps people align… because alignment reduces waste… because…',
            'fundamental_purpose': 'To make sure no one is left behind.',
            'foursome_insights': 'We all arrived at themes of connection and meaning.',
            'group_reflection': 'Our shared purpose should shape how we prioritise the agenda.',
        },
        'display_fields': [
            'activities',
            'why_chain',
            'fundamental_purpose',
            'foursome_insights',
            'group_reflection',
            'word_count',
        ],
        'timer_seconds': 1200,
    },
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
        'phases': [
            {'label': 'Phase 1 — Self-reflection', 'seconds': 60},
            {'label': 'Phase 2 — Pair ideas', 'seconds': 120},
            {'label': 'Phase 3 — Foursome ideas', 'seconds': 240},
            {'label': 'Phase 4 — Standout idea', 'seconds': 300},
        ],
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
