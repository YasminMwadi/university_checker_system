from django.urls import path
from university_checker_app import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'university_checker'
urlpatterns = [
    path('registration/', views.registration_view, name='registration'),
    path('forgot_password/', views.forgot_password_view, name='forgot_password'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('new_project/', views.project_view, name='new_project'),
    path('overview/<str:university>/', views.overview_view, name='overview'),
    path('comparison/<str:university>/', views.comparison_view, name='comparison'),
    path('ranking/<str:university>/',  views.RankingListView.as_view(), name='ranking'),
    path('profile/', views.profile_view, name='profile'),
    path('change_password/', views.change_password_view, name='change_password'),
    path('user_management/', views.user_management_view, name='user_management'),
    path('upload/', views.upload_excel, name='upload_excel'),
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),
    path('overview_report/<str:university>/', views.Overview_generatePdf.as_view(),  name='overview_report'),
    path('comparison_report/<str:university>/<str:selected_university>/', views.Comparison_generatePdf.as_view(), name='comparison_report'),  
    path('remove_profile_pic/', views.remove_profile_pic, name='remove_profile_pic'),
    path('delete_account/', views.delete_account, name='delete_account'),
     path('download_manual/', views.download_manual, name='download_manual'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)