from django.urls import path, include

from rest_framework.routers import DefaultRouter

from recipe import views


"""
Which app this urls.py belongs to.
This way reverse() function will find this urls
when using reverse(recipe:XXX)
"""
app_name = 'recipe'


"""
Router -> Register/Associate URLs for a viewset.
For making easier for urlpatterns and path,
just including the router and therefore, all the urls registered on the router.
127.0.0.1:8000/api/recipe/{ViewSet}
"""
router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)
router.register('recipes', views.RecipeViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
