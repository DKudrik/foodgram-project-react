from django.urls import path

from . import views


urlpatterns = [
    path('',
         views.index,
         name='index'),
    path('recipe/new/',
         views.new_recipe,
         name='new_recipe'),
    path('recipe/<int:recipe_id>/',
         views.recipe_view,
         name='recipe'),
    path('recipe/<int:recipe_id>/edit/',
         views.recipe_edit,
         name='recipe_edit'),
    path('recipe/<int:recipe_id>/delete/',
         views.recipe_delete,
         name='recipe_delete'),
    path('ingredients/',
         views.search_ingredients,
         name='search_ingredients'),
    path('subscriptions/',
         views.add_subscription,
         name='add_subscription'),
    path('subscriptions/<int:author_id>',
         views.remove_subscription,
         name='remove_subscription'),
    path('subscriptions/ <int:author_id>',
         views.remove_subscription,
         name='remove_subscription'),
    path('<str:username>/followings/',
         views.profile_following,
         name='profile_following'),
    path('favorites/',
         views.add_favorite,
         name='add_favorite'),
    path('favorites/<int:recipe_id>/',
         views.remove_favorite,
         name='remove_favorite'),
    path('<str:username>/profile_favorites/',
         views.profile_favorites,
         name='profile_favorites'),
    path('purchases/',
         views.add_purchase,
         name='add_purchase'),
    path('purchases/<int:recipe_id>/',
         views.remove_purchase,
         name='remove_purchase'),
    path('<str:username>/profile_purchases/',
         views.profile_purchases,
         name='profile_purchases'),
    path('not_api/purchases/<int:recipe_id>/',
         views.remove_purchase_list,
         name='remove_purchase_list'),
    path('purchases_download/',
         views.purchases_download,
         name='purchases_download'),
    path('not_auth_purchases/',
         views.not_auth_purchases,
         name='not_auth_purchases'),
    path('<str:username>/',
         views.profile,
         name='profile'),
]
