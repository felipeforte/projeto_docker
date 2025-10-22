#!/usr/bin/env python3
import subprocess
import json
import os
from datetime import datetime

class ExecutorTestes:
    def __init__(self):
        self.resultados = []
        self.n_instancias = 3
    
    def executar_teste_locust(self, usuarios, taxa, duracao, instancias, nome_teste):
        print(f"🚀 Executando teste: {nome_teste}")
        print(f"   👥 Usuários: {usuarios}, 📈 Taxa: {taxa}, ⏱️ Duração: {duracao}")
        
        comando = [
            "locust",
            "-f", "locustfile.py",
            "--host", "http://nginx",
            "--users", str(usuarios),
            "--spawn-rate", str(taxa),
            "--run-time", duracao,
            "--headless",
            "--only-summary",
            "--csv", f"resultados/{nome_teste}"
        ]
        
        try:
            os.makedirs("resultados", exist_ok=True)
            
            print(f"   ▶️  Executando: {' '.join(comando)}")
            
            # Executa dentro do container Locust
            resultado = subprocess.run(comando, capture_output=True, text=True, timeout=400)
            
            if resultado.returncode == 0:
                print(f"Teste {nome_teste} concluído com sucesso")
                arquivos_gerados = []
                for arquivo in os.listdir("resultados"):
                    if nome_teste in arquivo:
                        arquivos_gerados.append(arquivo)
                if arquivos_gerados:
                    print(f"Arquivos gerados: {', '.join(arquivos_gerados)}")
                else:
                    print("Nenhum arquivo de resultados foi gerado")
                
                self.salvar_resultados(usuarios, taxa, duracao, instancias, nome_teste)
                return True
            else:
                print(f"Erro no teste {nome_teste} (código: {resultado.returncode})")
                if resultado.stdout:
                    print(f"   Stdout: {resultado.stdout[:500]}...")
                if resultado.stderr:
                    print(f"   Stderr: {resultado.stderr[:500]}...")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"Timeout no teste {nome_teste}")
            return False
        except Exception as e:
            print(f"Erro ao executar teste {nome_teste}: {str(e)}")
            return False
    
    def salvar_resultados(self, usuarios, taxa, duracao, instancias, nome_teste):
        dados_resultado = {
            "timestamp": datetime.now().isoformat(),
            "nome_teste": nome_teste,
            "usuarios": usuarios,
            "taxa": taxa,
            "duracao": duracao,
            "instancias_wordpress": instancias,
            "arquivo_resultados": f"resultados/{nome_teste}_stats.csv"
        }
        self.resultados.append(dados_resultado)
    
    def testar(self):        
        configuracoes_usuarios = [10, 100, 750]
        
        print(f"\n===== INICIANDO TESTES =====")
        print("=" * 50)
        
        for usuarios in configuracoes_usuarios:
            taxa = max(1, usuarios // 10)
            duracao = "1m"
            nome_teste = f"wp_{self.n_instancias}inst_{usuarios}usuarios"
            
            print(f"\n📊 EXECUTANDO: {self.n_instancias} instância(s) + {usuarios} usuários")
            
            sucesso = self.executar_teste_locust(
                usuarios=usuarios,
                taxa=taxa,
                duracao=duracao,
                instancias=self.n_instancias,
                nome_teste=nome_teste
            )
            
            if sucesso:
                print(f"Prosseguindo...")
            else:
                print(f"Pulando para próximo teste...")
        
        self.gerar_resumo()
    
    def gerar_resumo(self):
        arquivo_resumo = "resultados/resumo_testes.json"
        try:
            with open(arquivo_resumo, 'w', encoding='utf-8') as f:
                json.dump(self.resultados, f, indent=2, ensure_ascii=False)
            
            print(f"\nResumo dos testes salvo em: {arquivo_resumo}")
            
            print("Arquivos de resultados gerados:")
            for arquivo in os.listdir("resultados"):
                print(f"   - {arquivo}")
                
            print("EXECUÇÃO CONCLUÍDA!")
        except Exception as e:
            print(f"Erro ao salvar resumo: {str(e)}")

if __name__ == "__main__":
    executor = ExecutorTestes()
    executor.testar()