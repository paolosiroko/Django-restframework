from django.shortcuts import render
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

# Authentication
from rest_framework.authentication import SessionAuthentication,TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework import mixins
from rest_framework import generics

from .models import Article
from .serializers import ArticleSerializer

from rest_framework import viewsets
from django.shortcuts import get_object_or_404


# MODEL VIEW SETS is the simplest

class ArticleModelViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()


# GENERIC VIEW SETS

class GenericArticleViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                            mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()


# VIEW SETS

class ArticleViewSet(viewsets.ViewSet):
    def list(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Article.objects.all()
        article = get_object_or_404(queryset, pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def update(self, request , pk=None):
        article = Article.objects.get(pk=pk)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        article = Article.objects.get(pk=pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# GENERIC VIEWS AND MIXINS

class GenericApiView(generics.GenericAPIView, mixins.ListModelMixin,mixins.CreateModelMixin,
                     mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    lookup_field = 'id'
    # Authentication
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):

        if id:
            return self.retrieve(request)
        else:
            return self.list(request)
        return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)


# CLASS BASED VIEWS

class ArticleApiView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# FUNCTION BASED VIEWS

# @api_view(['GET', 'POST'])
# def article_list(request):
#
#     if request.method == 'GET':
#         articles = Article.objects.all()
#         serializer = ArticleSerializer(articles, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = ArticleSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def article_detail(request, pk):
#     """
#       Retrieve, update or delete a code snippet.
#       """
#
#     try:
#         article = Article.objects.get(pk=pk)
#     except Article.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = ArticleSerializer(article)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = ArticleSerializer(article, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         article.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)




  # """
  # working without api view
  #   Retrieve, update or delete a code snippet.
  #   """

# @csrf_exempt
# def article_list(request):
#     if request.method == 'GET':
#         articles = Article.objects.all()
#         serializer = ArticleSerializer(articles, many=True)
#         return JsonResponse(serializer.data, safe=False)
#
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = ArticleSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#         if serializer.is_valid():
#             serializer.save()
#         return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)
#
#
# @csrf_exempt
# def article_detail(request, pk):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         article = Article.objects.get(pk=pk)
#     except Article.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == 'GET':
#         serializer = ArticleSerializer(article)
#         return JsonResponse(serializer.data)
#
#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = ArticleSerializer(article, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)
#
#     elif request.method == 'DELETE':
#         article.delete()
#         return HttpResponse(status=204)
#
