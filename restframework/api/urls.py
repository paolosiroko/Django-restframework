from django.urls import path,include
from .views import ArticleApiView,ArticleDetail,GenericApiView,ArticleViewSet,GenericArticleViewSet,ArticleModelViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('article', ArticleViewSet, basename='article')
# GENERIC VIEW SET
router.register('articleg', GenericArticleViewSet, basename='articleg')
# MODEL VIEW SET is the simplest
router.register('articlem', ArticleModelViewSet, basename='articlem')


urlpatterns = [
    path('viewset/',include(router.urls)),
    path('viewset/<int:pk>/',include(router.urls)),

    path('',ArticleApiView.as_view(), ),
    path('detail/<int:pk>/',ArticleDetail.as_view(), ),
    path('generic/<int:id>/',GenericApiView.as_view(), ),


]


# FUNCTION BASED VIEWS URLS

# urlpatterns = [
#     path('',views.article_list ),
#     path('detail/<int:pk>/',views.article_detail),
# ]