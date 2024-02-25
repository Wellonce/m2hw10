from django.urls import path

from apps.gap.views import RoomListView, RoomDetailView, LikeOpinionView, OpinionDetailView, Loginview, UserRegisterView, UserLogout

app_name = 'gap'
urlpatterns = [
    path('rooms/', RoomListView.as_view(), name='rooms'),
    path('room/<pk>', RoomDetailView.as_view(), name='room'),
    path('like/<pk>', LikeOpinionView.as_view(), name='opinion-like'),
    path('opinion/<pk>', OpinionDetailView.as_view(), name='opdetail-like'),
    path('login/', Loginview.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register-page'),
    path('logout/', UserLogout.as_view(), name='logout'),

]
