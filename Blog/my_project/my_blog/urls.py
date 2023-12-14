from django.urls import path
from django.contrib.auth import views as auth_view
from . import views


urlpatterns = [
    path("",views.LandingPageView.as_view(),name="landing_page"),
    path("posts",views.AllPostView.as_view(),name="posts_page"),
    path("posts/<slug:slug>",views.DetailPostView.as_view(),name="detail_posts_page"),
    path("contact/",views.Contactview,name="contact_page"),
    path("signup/",views.SignUpView.as_view(),name="sign_up"),
    path("login/",auth_view.LoginView.as_view(template_name="my_blog/login.html"),name="login"),
    path("logout/",auth_view.LogoutView.as_view(template_name="my_blog/logout.html"),name="logout"),
    path("createpost/",views.PostCreateView.as_view(),name="post_create_page"),
    path("posts/<slug:slug>/update",views.PostUpdateView.as_view(),name="update_post_page"),
    path("posts/<slug:slug>/delete",views.PostDeleteView.as_view(),name="delete_post_page"),
]