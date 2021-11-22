from django.urls import path
from dashboard import views
app_name = 'dashboard'
urlpatterns = [ 
    path('create', views.dashboard_index ,name="index"),
    path('libraries', views.dashboard_libraries ,name="libraries"),
    path('lib_scan/<int:lib_id>', views.library_scan , name="lib_scan"),
    path('process_data/<int:lib_id>', views.process_data , name="process_data"),
    path('delete_librabry/<int:librabry_id>', views.delete_librabry , name="delete_librabry"),
    path('cve_scan', views.cve_scan , name="cve_scan"),
    
    path('send_notification', views.send_notification , name="send_notification"),
    path('generate_otp', views.generate_otp , name="generate_otp"),
    path('alert_recovery', views.alert_recovery , name="alert_recovery"),
    
    
    


    
 
]