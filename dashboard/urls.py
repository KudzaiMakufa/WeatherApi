from django.urls import path
from dashboard import views
app_name = 'dashboard'
urlpatterns = [ 
    path('create', views.dashboard_index ,name="index"),
    path('libraries', views.dashboard_libraries ,name="libraries"),
    path('lib_scan/<int:lib_id>', views.library_scan , name="lib_scan"),
    path('process_data', views.process_data , name="process_data"),
    path('map_data', views.map_data , name="map_data"),
    path('reduce_data/<str:file_id>', views.reduce_data , name="reduce_data"),
    path('read_contents/<str:file_name>', views.read_contents , name="read_contents"),
    path('view_data/<int:lib_id>', views.view_data , name="view_data"),
    path('delete_librabry/<int:librabry_id>', views.delete_librabry , name="delete_librabry"),
    
  
    
   

    
 
]