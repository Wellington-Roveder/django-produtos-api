from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from .models import Produto

class ProdutoAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.produto = Produto.objects.create(
         nome = "notebook gamer3500",
         descricao = "notebook gamer para teste",
         valor = 2999.99,
         quantidade = 10
        )

    def test_listar_produtos(self):
       response = self.client.get('/api/produtos/') 
       self.assertEqual(response.status_code, 200)

    def test_criar_produto(self):
        data = {
            'nome': 'Mouse gamer',
            'descricao': 'Mouse para teste',
            'valor': 299.99,
            'quantidade': 5
        }
        
        response = self.client.post('/api/produtos/', data)
        self.assertEqual(response.status_code, 201) 
        quant =  Produto.objects.count() 
        self.assertEqual(quant, 2)  


    def test_deletar_produto(self):
        response = self.client.delete(f'/api/produtos/{self.produto.id}/') 
        self.assertEqual(response.status_code, 204)
        quant =  Produto.objects.count() 
        self.assertEqual(quant, 0)

    def test_put_produto(self):
        data = {
            'nome': 'Mouse gamer',
            'descricao': 'Mouse so que de cor diferente',
            'valor': 450.77,
            'quantidade': 10
        }
         

        response = self.client.put(f'/api/produtos/{self.produto.id}/', data)
        self.assertEqual(response.status_code, 200)
        quant =  Produto.objects.count() 
        self.assertEqual(quant, 1)
    
    def test_atualizar_produto(self):
        data = {
            'nome': 'Mouse gamer',
            'descricao': 'Mouse so que de cor diferente'
        }
         

        response = self.client.patch(f'/api/produtos/{self.produto.id}/', data)
        self.assertEqual(response.status_code, 200)
        quant =  Produto.objects.count() 
        self.assertEqual(quant, 1)
                