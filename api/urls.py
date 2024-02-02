from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("test/<int:pk>/", views.test),
    path("signup/", views.signup),
    path("delete/<int:pk>/", views.delete_items),
    path("users/", views.show_users),
    path("login/", views.login),
    path("token/", views.token),
    path("events/", views.events),
    path("events/<int:pk>/", views.get_event),
    path("events/<int:pk>/join/", views.join_event),
    path("events/<int:pk>/leave/", views.leave_event),
    path("events/<int:pk>/start/", views.start_event),
    path("events/<int:pk>/submitmatch/", views.submit_match_result),
    path("games/", views.get_games),
    path("playerstats/", views.get_playerstats)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

