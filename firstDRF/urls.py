from .views import ArticleViewSet
from rest_framework.routers import DefaultRouter
from datetime import timedelta
from django.urls import path
from . import views
from rest_framework.authtoken import views as tview
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
app_name = 'drf_home'
urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('s/', views.hello_word, name='home'),
    path('', views.HelloWord.as_view(), name='hello'),
    path('crypto/', views.GetCryptoPrice.as_view(), name='crypto'),
    path('articles/', views.ShowArticles.as_view(), name='articles'),
    path('detail/<int:pk>', views.ArticleDetailView.as_view(), name='detail'),
    path('articles/add/', views.AddArticleView.as_view(), name='add_Article'),
    path('articles/update/<int:pk>', views.ArticleUpdateView.as_view(), name='update_Article'),
    path('logins', tview.obtain_auth_token, name='obtain_auth_token'),
    path('articles/comments/<int:pk>', views.GetArticleCommentView.as_view(), name='article_comment'),
    path('users/', views.UserDetailView.as_view(), name='Users'),
]
router = DefaultRouter()
router.register(r'articles/viewsets', ArticleViewSet, basename='viewsets')
urlpatterns += router.urls