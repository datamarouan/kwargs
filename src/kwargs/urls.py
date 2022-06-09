from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from utilisateur import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('page.urls')),
    path('blog/', include('blog.urls')),
    path('glossaire/', include('glossaire.urls')),
    path('cde/', include('rudi.urls')),
    path('projet/', include('projet.urls')),
    path('catalogue/', include('catalogue.urls')),
    path("maturite/", include('maturite.urls'))
]

url_users = [
    path('login/', user_views.LoginView.as_view(template_name="utilisateur/login.html"), name="login"),
    path('logout/', user_views.LogoutView.as_view(template_name="utilisateur/logout.html"), name="logout"),
    path('password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name="utilisateur/password/password_reset.html"
            ),
        name="password_reset"),
    path('password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name="utilisateur/password/password_reset_done.html"
            ),
        name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name="utilisateur/password/password_reset_confirm.html"
            ),
        name="password_reset_confirm"),
    path('password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name="utilisateur/password/password_reset_complete.html"
            ),
        name="password_reset_complete"),
    path('profile/', user_views.profile, name="profile"),
    path('register/', user_views.register, name="register"),
    path('groupes/', user_views.GroupsList.as_view(), name="groups-list"),
    path('groupe/<int:pk>/', user_views.GroupsDetailView.as_view(), name="group-details"),
    path('groupe/ajouter/', user_views.GroupsCreateView.as_view(), name="new-group"),
    path('groupe/<int:pk>/edition/', user_views.GroupsUpdateView.as_view(), name="group-modif"),
    path('groupe/<int:pk>/effacer/', user_views.GroupsDeleteView.as_view(), name="group-delete"),
    path('users/', user_views.UsersList.as_view(), name="users-list"),
]

urlpatterns += url_users

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'kwargs Industria Administration'  # default: "Django Administration"
admin.site.index_title = 'Objets éditables'  # default: "Site administration"
admin.site.site_title = 'kwargs site admin'       # default: "Django site admin"
