from django.urls import path
from recommend.views import recommendation,recommend_by_id
urlpatterns = [
    path("recommend/",recommendation),
    path("<int:id>/",recommend_by_id),
]

