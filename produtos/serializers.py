from rest_framework import serializers
from .models import Produto

class ProdutoSerializer(serializers.ModelSerializer):
    data_criacao = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S", read_only=True)
    
    class Meta:
        model = Produto
        fields = '__all__'