from rest_framework import viewsets,
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, ArticleSerializer, CommentSerializer
from django.contrib.auth.models import User
from .models import Article
import requests
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import BlocklistPermission, IsUserOrReadOnly

URL = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"


@api_view(['GET', 'POST'])
def hello_word(request):
    return Response({'message': 'hello, world!'})


product = [
    {'name': 'amir',
     'last name': None
     },
    {
        'product_name': 'laptop',
        'price': 49
    }
]


class HelloWord(APIView):
    def get(self, request):
        name = request.GET.get('name')
        last = request.GET.get('last')

        return Response({'message': f'hello {name} {last}'})

    def post(self, request):
        name = request.GET.get('name')
        last = request.GET.get('last')
        data = request.data
        return Response(f'hello, {data.get("name")} {data.get("last")}')


class GetCryptoPrice(APIView):
    def get(self, request):
        coin = request.GET.get('coin').upper()
        responce = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={coin}")
        data = responce.json()
        result = {
            "symbol": data.get('symbol'),
            "price": data.get('price')
        }
        print(coin)
        return Response(data=result)





class ShowArticles(APIView):
    def get(self, request):
        queryset = Article.objects.all()
        serializer = ArticleSerializer(instance=queryset, many=True)
        return Response(data=serializer.data)


class ArticleDetailView(APIView):
    def get(self, request, pk):
        instance = Article.objects.get(id=pk)
        serializer = ArticleSerializer(instance=instance)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated

class AddArticleView(APIView):
    permission_classes = [IsAuthenticated, BlocklistPermission, IsUserOrReadOnly]

    def post(self, request):
        serializer = ArticleSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.validated_data['user'] = request.user
            serializer.save()
            return Response(data={"response": 'Added'}, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleUpdateView(APIView):
    permission_classes = [BlocklistPermission, IsUserOrReadOnly]
    def put(self, request, pk):
        instance = Article.objects.get(id=pk)
        self.check_object_permissions(request, instance)
        serializer = ArticleSerializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(instance=instance, validated_data=serializer.validated_data)
            return Response(data={"response": 'Updated'}, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        instance = Article.objects.get(id=pk)
        instance.delete()
        return Response(data={"response": 'Deleted'}, status=status.HTTP_200_OK)


class CheckToken(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user = request.user
        return Response({'user': user.username}, status=status.HTTP_200_OK)



class GetArticleCommentView(APIView):
    def get(self, request, pk):
        comments = Article.objects.get(id=pk).comments.all()
        serializer = CommentSerializer(instance=comments, many=True)
        return Response(serializer.data, status= status.HTTP_200_OK)

class UserDetailView(APIView):
    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(instance=user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# class ArticleViewSet(viewsets.ViewSet):
#     def list(self, request):
#         querysets = Article.objects.all()
#         serializer = ArticleSerializer(instance=querysets, many=True)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)
#
#     def retrieve(self, request, pk=None):
#         querysets = Article.objects.get(id=pk)
#         serializer = ArticleSerializer(instance=querysets)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)


 class ArticleViewSet(viewsets.ModelViewSet):
     queryset = Article.objects.all()
     serializer_class = ArticleSerializer