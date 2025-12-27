import urllib.request
import base64
import time
from datetime import datetime

# ================= CONFIGURAÇÕES DO USUÁRIO =================
USERNAME = "SEU_USUARIO_NOIP"
PASSWORD = "SUA_SENHA_NOIP"
HOSTNAME = "SEU_REGISTRO_AAAA"
INTERVALO = 600  # Tempo em segundos entre checagens (600s = 10 minutos)
# ============================================================

# URL especial do No-IP que força a conexão via IPv6
# Isso garante que a gente não pegue o IPv4 por engano
URL_UPDATE = "http://ip1.dynupdate6.no-ip.com/nic/update"

def log(mensagem):
    """Função simples para mostrar mensagens com hora/data"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {mensagem}")

def obter_ipv6_publico():
    """Descobre qual é o seu IPv6 atual usando um serviço externo"""
    try:
        # api6.ipify.org só responde se você tiver IPv6 funcionando
        with urllib.request.urlopen("https://api6.ipify.org", timeout=10) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        log(f"Erro ao detectar IPv6: {e}")
        return None

def atualizar_noip(ipv6_atual):
    """Envia o novo IP para o No-IP"""
    full_url = f"{URL_UPDATE}?hostname={HOSTNAME}&myip={ipv6_atual}"
    
    # Prepara a autenticação (Codifica usuário:senha em Base64)
    auth_str = f"{USERNAME}:{PASSWORD}"
    auth_bytes = auth_str.encode("ascii")
    base64_bytes = base64.b64encode(auth_bytes)
    base64_string = base64_bytes.decode("ascii")

    req = urllib.request.Request(full_url)
    req.add_header("Authorization", f"Basic {base64_string}")
    req.add_header("User-Agent", "Python No-IP Updater/1.0")

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            resultado = response.read().decode('utf-8')
            return resultado
    except urllib.error.HTTPError as e:
        return f"Erro HTTP: {e.code}"
    except Exception as e:
        return f"Erro de conexão: {e}"

def main():
    log(f"Iniciando atualizador IPv6 para: {HOSTNAME}")
    ultimo_ip = None

    while True:
        # 1. Tenta descobrir o IPv6 atual da máquina
        ipv6_atual = obter_ipv6_publico()

        if ipv6_atual:
            # 2. Se o IP mudou desde a última vez, atualiza
            if ipv6_atual != ultimo_ip:
                log(f"Novo IPv6 detectado: {ipv6_atual}. Atualizando No-IP...")
                resposta = atualizar_noip(ipv6_atual)
                
                # Verifica a resposta do servidor No-IP
                if "good" in resposta or "nochg" in resposta:
                    log(f"Sucesso! Servidor respondeu: {resposta}")
                    ultimo_ip = ipv6_atual
                else:
                    log(f"Falha na atualização. Resposta: {resposta}")
            else:
                # Opcional: comentar esta linha para limpar o log
                print(f"IPv6 mantém-se o mesmo ({ipv6_atual}). Nenhuma ação necessária.")
        else:
            log("Não foi possível obter o IPv6 público. Verifique sua conexão.")

        # 3. Espera X segundos antes de tentar de novo
        time.sleep(INTERVALO)

if __name__ == "__main__":
    main()
