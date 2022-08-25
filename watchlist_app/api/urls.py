from django.urls import path
# from watchlist_app.api.views import movies_list, movie_detail
from watchlist_app.api.views import (ReviewList,ReviewDetail, ReviewCreate,
                                     WatchListAV, WatchDetailAV, WatchListGV,
                                     StreamPlatformListAV, StreamDetailAV)

urlpatterns = [
    path('list/', WatchListAV.as_view(), name='movies-list'),
    path('list2/', WatchListGV.as_view(), name='movies-list-duplicate'),
    path('<int:pk>/', WatchDetailAV.as_view(), name='movie-detail'),
    path('stream/', StreamPlatformListAV.as_view(), name='stream-platform-list'),
    path('stream/<int:pk>/', StreamDetailAV.as_view(), name='stream-platform-detail'),
    
    # path('review/', ReviewList.as_view(), name='review-list'),
    # path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
    
    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/reviews/',ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail')

    
]
