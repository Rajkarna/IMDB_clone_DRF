from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
# from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import BasicAuthentication
from .permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from .throttling import ReviewCreateThrottle, ReviewListThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .pagination import WatchlistPagination, WatchListLOPagination, WatchListCPagination
from watchlist_app.api.serializers import WatchListSerializer,StreamPlatformSerializer, ReviewSerializer
from watchlist_app.models import WatchList, StreamPlatform, Review

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewCreateThrottle]
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)
        
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)
        if review_queryset.exists():
            raise ValidationError("you already reviewed this movie")
        
        if watchlist.num_rating == 0:
            watchlist.Avg_rating = serializer.validated_data['rating']
        else:
            watchlist.Avg_rating =  (watchlist.Avg_rating + serializer.validated_data['rating'])/2
        
        watchlist.num_rating += 1
        watchlist.save()
        
        serializer.save(watchlist = watchlist, review_user = review_user)
        
class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle]

    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist = pk)
        
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    # throttle_classes = [ScopedRateThrottle]
    # throttle_scope = 'review-detail'


# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs) 

# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    # filter_backends = [filters.OrderingFilter]    
    # ordering_fields   = ['Avg_rating']
    # pagination_class = WatchListCPagination
   

class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self,request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many = True)
        return Response(serializer.data)
    
    
    def post(self,request):
        serializer = WatchListSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)



class WatchDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self,request,pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error: Not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)
    
    def put(self,request,pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def delete(self,request,pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status = status.HTTP_404_NOT_FOUND)
            
            
            
            

class StreamPlatformListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self,request):
        streams = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(streams, many = True)
        return Response(serializer.data)       
        
        
    def post(self,request):
        serializer = StreamPlatformSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
            
    


class StreamDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self,request,pk):
        try:
            stream = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error : stream not found'}, status = status.HTTP_404_NOT_FOUND)
        
        serializer = StreamPlatformSerializer(stream)
        return Response(serializer.data)
        
    def put(self,request,pk):
        stream = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(stream, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
    def delete(self,request,pk):
        stream = StreamPlatform.objects.get(pk=pk)
        stream.delete()
        return Response(status = status.HTTP_404_NOT_FOUND)















# @api_view(['GET', 'POST'])
# def movies_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many = True)
#         return Response(serializer.data)
    
#     if request.method == 'POST':
#         serializer = MovieSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)


# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_detail(request, pk):
#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({'error: Movie not found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
    
#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie, data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
    
#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_404_NOT_FOUND)