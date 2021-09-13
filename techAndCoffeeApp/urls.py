from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.loginPage),
    path('register', views.register),
    path('login', views.login),
    path('homePage', views.homePage),
    path('logout', views.logout),
    path('homePage/newPost',views.new),
    path('homePage/image_upload', views.imageview, name = 'image_upload'),
    path('success', views.success,name = 'success'),
    path('homePage/viewPosts',views.displayImages),
    path('homePage/viewPosts/createcomment',views.createComment),
    path('homePage/viewPosts/<int:comment_id>/edit',views.editComment),
    path('homePage/viewPosts/<int:comment_id>/update',views.updateComment),
    path('homePage/<int:user_id>/profilePage',views.profileView),


]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
