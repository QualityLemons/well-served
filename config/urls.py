from django.contrib import admin
from django.http import HttpResponse
from django.urls import path


def home(request):
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Well-Served</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
                   max-width: 720px; margin: 4rem auto; padding: 0 1.5rem; color: #222; }
            h1 { color: #2a4d69; }
            code { background: #f4f4f4; padding: 0.15rem 0.4rem; border-radius: 4px; }
            .card { background: #f8fafc; border: 1px solid #e2e8f0;
                    padding: 1.25rem 1.5rem; border-radius: 8px; margin-top: 1.5rem; }
        </style>
    </head>
    <body>
        <h1>Well-Served</h1>
        <p>Milestone Project 3 &mdash; Level 5 Diploma in Web Software Engineering.</p>
        <p>The Django development server is running.</p>
        <div class="card">
            <strong>Available routes</strong>
            <ul>
                <li><a href="/admin/">/admin/</a> &mdash; Django admin site</li>
            </ul>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)


urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
]
