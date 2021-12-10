from django.urls import path
from dashboard import views
app_name = 'dashboard'
urlpatterns = [ 
    path('create', views.dashboard_index ,name="index"),
    path('libraries', views.dashboard_libraries ,name="libraries"),
    path('lib_scan/<int:lib_id>', views.library_scan , name="lib_scan"),
    path('process_data', views.process_data , name="process_data"),
    path('view_data/<int:lib_id>', views.view_data , name="view_data"),
    path('delete_librabry/<int:librabry_id>', views.delete_librabry , name="delete_librabry"),
  
    
   

    
 
]