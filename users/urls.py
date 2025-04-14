from django.urls import path
from . import views as user
urlpatterns = [
    path('create_user/', user.create_user, name='creat_user'),
    path('all_users/', user.all_user, name='all_users'),
    path('update/<int:user_id>/', user.update_user, name='update_user'),
    path('delate/<int:user_id>/', user.delete_user, name='delete_user'),

]
