from locust import HttpUser, task, between
import random

class UsuarioWordPress(HttpUser):
    wait_time = between(1, 3)
    
    posts = [
        "/2025/10/21/post-com-texto-de-400kb/",
        "/2025/10/21/post-com-imagem-de-1mb/", 
        "/2025/10/21/post-com-imagem-de-300kb/"
    ]
    
    @task(1)
    def carregar_post_com_texto(self):
        self.client.get("/2025/10/21/post-com-texto-de-400kb/")
    
    @task(1) 
    def carregar_post_com_imagem_grande(self):
        self.client.get("/2025/10/21/post-com-imagem-de-1mb/")
    
    @task(1)
    def carregar_post_com_imagem_pequena(self):
        self.client.get("/2025/10/21/post-com-imagem-de-300kb/")