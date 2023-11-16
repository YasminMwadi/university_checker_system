from django.urls import path
from university_checker_app import views

app_name = 'university_checker'
urlpatterns = [
    path('registration/', views.registration_view, name='registration'),
    path('forgot_password/', views.forgot_password_view, name='forgot_password'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('new_project/', views.project_view, name='new_project'),
    path('overview/<str:university>/', views.overview_view, name='overview'),
    path('comparison/<str:university>/', views.comparison_view, name='comparison'),
    path('ranking/<str:university>/', views.ranking_view, name='ranking'),
    path('profile/', views.profile_view, name='profile'),
    path('change_password/', views.change_password_view, name='change_password'),
    path('user_management/', views.user_management_view, name='user_management'),
    path('upload/', views.upload_excel, name='upload_excel'),
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),

]
 