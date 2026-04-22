import sys
import os
import json
from datetime import datetime
from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# --- Configuration & Setup ---

if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY='django-insecure-key-high-security-workspace',
        ROOT_URLCONF=__name__,
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'db.sqlite3',
            }
        },
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
        }],
        MIDDLEWARE=[
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ],
    )

# --- Models ---

class ToolOutput(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tool_name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

# --- Views ---

def index(request):
    if request.user.is_authenticated:
        return HttpResponse(HTML_TEMPLATE)
    return HttpResponse(AUTH_TEMPLATE)

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'User already exists'}, status=400)
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return JsonResponse({'status': 'registered'})

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if user:
            login(request, user)
            return JsonResponse({'status': 'logged_in'})
        return JsonResponse({'error': 'Invalid credentials'}, status=401)

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def get_user_outputs(request):
    outputs = list(ToolOutput.objects.filter(user=request.user).values(
        'id', 'tool_name', 'title', 'content', 'is_published', 'created_at'
    ))
    return JsonResponse({'outputs': outputs})

@csrf_exempt
@login_required
def save_output(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        output = ToolOutput.objects.create(
            user=request.user,
            tool_name=data.get('tool_name'),
            title=data.get('title'),
            content=data.get('content')
        )
        return JsonResponse({'id': output.id, 'status': 'saved'})

@csrf_exempt
@login_required
def toggle_publish(request, output_id):
    output = ToolOutput.objects.get(id=output_id, user=request.user)
    output.is_published = not output.is_published
    output.save()
    return JsonResponse({'status': 'updated', 'is_published': output.is_published})

def public_archive(request, output_id):
    """Static HTML Archive view."""
    try:
        output = ToolOutput.objects.get(id=output_id, is_published=True)
        html = f"""
        <html><head><title>{output.title}</title><style>body{{font-family:sans-serif;padding:2rem;max-width:800px;margin:auto;}}</style></head>
        <body><h1>{output.title}</h1><p>Tool: {output.tool_name}</p><hr/><pre>{output.content}</pre></body></html>
        """
        return HttpResponse(html)
    except ToolOutput.DoesNotExist:
        return HttpResponse("Not Found or Not Published", status=404)

@login_required
def download_file(request, output_id, format_type):
    output = ToolOutput.objects.get(id=output_id, user=request.user)
    filename = f"{output.title.replace(' ', '_')}"
    
    if format_type == 'md':
        content = f"# {output.title}\n\n{output.content}"
        response = HttpResponse(content, content_type='text/markdown')
        response['Content-Disposition'] = f'attachment; filename="{filename}.md"'
    elif format_type == 'rtf':
        # Basic RTF encapsulation
        rtf_content = r"{\rtf1\ansi\deff0 {\fonttbl {\f0 Arial;}} \f0\fs24 " + output.title + r"\line\line " + output.content.replace('\n', r'\line ') + r"}"
        response = HttpResponse(rtf_content, content_type='application/rtf')
        response['Content-Disposition'] = f'attachment; filename="{filename}.rtf"'
    else:
        return HttpResponse("Invalid Format", status=400)
    return response

# --- URL Routing ---

urlpatterns = [
    path('', index),
    path('auth/register/', register_view),
    path('auth/login/', login_view),
    path('auth/logout/', logout_view),
    path('api/outputs/', get_user_outputs),
    path('api/save/', save_output),
    path('api/publish/<int:output_id>/', toggle_publish),
    path('api/download/<int:output_id>/<str:format_type>/', download_file),
    path('archive/<int:output_id>/', public_archive),
]

# --- Templates ---

AUTH_TEMPLATE = """
<!DOCTYPE html><html><head><title>Secure Login</title><script src="https://cdn.tailwindcss.com"></script></head>
<body class="bg-slate-900 flex items-center justify-center min-h-screen">
    <div class="bg-white p-8 rounded-2xl shadow-2xl w-full max-w-md">
        <h1 class="text-2xl font-bold mb-6 text-center text-slate-800">Workspace Secure Access</h1>
        <div class="space-y-4">
            <input id="user" type="text" placeholder="Username" class="w-full px-4 py-3 border rounded-xl outline-none focus:ring-2 focus:ring-blue-500">
            <input id="pass" type="password" placeholder="Password" class="w-full px-4 py-3 border rounded-xl outline-none focus:ring-2 focus:ring-blue-500">
            <button onclick="handleAuth('login')" class="w-full bg-blue-600 text-white py-3 rounded-xl font-bold hover:bg-blue-700">Login</button>
            <button onclick="handleAuth('register')" class="w-full bg-slate-100 text-slate-700 py-3 rounded-xl font-bold hover:bg-slate-200">Register</button>
        </div>
    </div>
    <script>
        async function handleAuth(type) {
            const username = document.getElementById('user').value;
            const password = document.getElementById('pass').value;
            const res = await fetch(`/auth/${type}/`, {
                method: 'POST', body: JSON.stringify({username, password})
            });
            if(res.ok) window.location.reload();
            else alert("Authentication failed");
        }
    </script>
</body></html>
"""

HTML_TEMPLATE = """
<!DOCTYPE html><html><head><title>Tool Suite</title><script src="https://cdn.tailwindcss.com"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"></head>
<body class="bg-slate-50 min-h-screen">
    <header class="bg-white border-b p-4 shadow-sm flex justify-between items-center">
        <h1 class="font-bold text-xl text-blue-600"><i class="fas fa-toolbox mr-2"></i>Tool Suite</h1>
        <div class="flex items-center space-x-4">
            <span class="text-sm text-slate-500">Logged in as <b>{{ request.user.username }}</b></span>
            <a href="/auth/logout/" class="text-red-500 hover:underline text-sm font-bold">Logout</a>
        </div>
    </header>

    <main class="max-w-6xl mx-auto p-6 grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Tools List -->
        <div class="lg:col-span-1 space-y-4">
            <h2 class="font-bold text-slate-800 flex items-center"><i class="fas fa-list-ul mr-2"></i>Tool Bank</h2>
            <div class="bg-white rounded-xl border p-2 space-y-1">
                <button onclick="selectTool('md')" class="w-full text-left p-3 hover:bg-blue-50 rounded-lg flex items-center"><i class="fab fa-markdown w-8 text-blue-500"></i>Markdown Editor</button>
                <button onclick="selectTool('code')" class="w-full text-left p-3 hover:bg-blue-50 rounded-lg flex items-center"><i class="fas fa-code w-8 text-emerald-500"></i>Code Formatter</button>
                <button onclick="selectTool('inspect')" class="w-full text-left p-3 hover:bg-blue-50 rounded-lg flex items-center"><i class="fas fa-search w-8 text-amber-500"></i>JSON Inspector</button>
            </div>
            
            <h2 class="font-bold text-slate-800 pt-4 flex items-center"><i class="fas fa-archive mr-2"></i>Saved Works</h2>
            <div id="outputs-list" class="space-y-3 max-h-96 overflow-y-auto pr-2"></div>
        </div>

        <!-- Editor Area -->
        <div class="lg:col-span-2 space-y-6">
            <div class="bg-white rounded-2xl shadow-sm border p-6">
                <div class="flex justify-between items-center mb-4">
                    <h3 id="current-tool-title" class="font-bold text-lg">Select a tool</h3>
                    <input id="work-title" type="text" placeholder="Entry Title" class="px-3 py-1 border-b focus:border-blue-500 outline-none text-right">
                </div>
                <textarea id="editor" class="w-full h-80 p-4 bg-slate-50 rounded-xl border focus:ring-2 focus:ring-blue-500 outline-none font-mono text-sm" placeholder="Tool output or content goes here..."></textarea>
                <div class="flex justify-end mt-4">
                    <button onclick="saveWork()" class="bg-blue-600 text-white px-6 py-2 rounded-xl font-bold hover:bg-blue-700 flex items-center">
                        <i class="fas fa-cloud-upload-alt mr-2"></i>Save to Cloud
                    </button>
                </div>
            </div>
        </div>
    </main>

    <script>
        let currentTool = 'md';
        
        function selectTool(t) {
            currentTool = t;
            const titles = { 'md': 'Markdown Editor', 'code': 'Code Formatter', 'inspect': 'JSON Inspector' };
            document.getElementById('current-tool-title').innerText = titles[t];
            document.getElementById('editor').value = '';
        }

        async function fetchHistory() {
            const res = await fetch('/api/outputs/');
            const data = await res.json();
            const list = document.getElementById('outputs-list');
            list.innerHTML = '';
            data.outputs.reverse().forEach(o => {
                const card = document.createElement('div');
                card.className = 'bg-white p-4 rounded-xl border shadow-sm space-y-2';
                card.innerHTML = `
                    <div class="flex justify-between font-bold text-sm">
                        <span>${o.title || 'Untitled'}</span>
                        <span class="text-xs text-slate-400">${o.tool_name}</span>
                    </div>
                    <div class="flex items-center space-x-2">
                        <button onclick="togglePublish(${o.id})" class="text-xs px-2 py-1 rounded bg-slate-100 ${o.is_published ? 'text-blue-600 font-bold' : ''}">
                            <i class="fas fa-globe mr-1"></i>${o.is_published ? 'Published' : 'Private'}
                        </button>
                        ${o.is_published ? `<a href="/archive/${o.id}/" target="_blank" class="text-xs text-blue-500 underline"><i class="fas fa-external-link-alt"></i></a>` : ''}
                    </div>
                    <div class="flex space-x-2 border-t pt-2 mt-2">
                        <a href="/api/download/${o.id}/md" class="text-xs text-slate-500 hover:text-blue-500"><i class="fas fa-file-download mr-1"></i>.MD</a>
                        <a href="/api/download/${o.id}/rtf" class="text-xs text-slate-500 hover:text-blue-500"><i class="fas fa-file-word mr-1"></i>.RTF</a>
                    </div>
                `;
                list.appendChild(card);
            });
        }

        async function saveWork() {
            const title = document.getElementById('work-title').value || 'New Entry';
            const content = document.getElementById('editor').value;
            await fetch('/api/save/', {
                method: 'POST', body: JSON.stringify({tool_name: currentTool, title, content})
            });
            fetchHistory();
        }

        async function togglePublish(id) {
            await fetch(`/api/publish/${id}/`, { method: 'POST' });
            fetchHistory();
        }

        fetchHistory();
    </script>
</body></html>
"""

# --- Execution ---

if __name__ == "__main__":
    from django.core.management import call_command
    call_command('migrate', verbosity=0)
    execute_from_command_line(sys.argv)