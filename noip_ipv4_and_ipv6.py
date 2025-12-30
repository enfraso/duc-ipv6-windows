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

# URLs de detecção de IP
URL_CHECK_IPV4 = "https://api.ipify.org"
URL_CHECK_IPV6 = "https://api6.ipify.org"

# URL padrão de update do No-IP
URL_UPDATE_BASE = "http://dynupdate.no-ip.com/nic/update"

def log(mensagem):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {mensagem}")

def obter_ip(url_api):
    """Função genérica para pegar IP (seja v4 ou v6)"""
    try:
        with urllib.request.urlopen(url_api, timeout=10) as response:
            return response.read().decode('utf-8')
    except Exception:
        # Silencia o erro para não poluir o log se um dos protocolos falhar
        return None

def atualizar_noip(ip_address):
    """Envia o IP para o No-IP"""
    # Monta a URL. O No-IP detecta automaticamente se é v4 ou v6 pelo formato do IP
    full_url = f"{URL_UPDATE_BASE}?hostname={HOSTNAME}&myip={ip_address}"
    
    auth_str = f"{USERNAME}:{PASSWORD}"
    auth_bytes = auth_str.encode("ascii")
    base64_bytes = base64.b64encode(auth_bytes)
    base64_string = base64_bytes.decode("ascii")

    req = urllib.request.Request(full_url)
    req.add_header("Authorization", f"Basic {base64_string}")
    req.add_header("User-Agent", "Python Dual-Stack Updater/2.0")

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        return f"Erro de conexão: {e}"

def main():
    log(f"--- Iniciando Atualizador Dual-Stack (IPv4 & IPv6) para: {HOSTNAME} ---")
    
    ultimo_ipv4 = None
    ultimo_ipv6 = None

    while True:
        # 1. Verifica IPv4
        ipv4_atual = obter_ip(URL_CHECK_IPV4)
        if ipv4_atual and ipv4_atual != ultimo_ipv4:
            log(f"[IPv4] Mudança detectada: {ipv4_atual}")
            resp = atualizar_noip(ipv4_atual)
            if "good" in resp or "nochg" in resp:
                log(f"[IPv4] Atualizado com sucesso: {resp}")
                ultimo_ipv4 = ipv4_atual
            else:
                log(f"[IPv4] Erro na resposta: {resp}")
        elif not ipv4_atual:
            log("[IPv4] Não foi possível detectar.")

        # 2. Verifica IPv6
        ipv6_atual = obter_ip(URL_CHECK_IPV6)
        if ipv6_atual and ipv6_atual != ultimo_ipv6:
            log(f"[IPv6] Mudança detectada: {ipv6_atual}")
            resp = atualizar_noip(ipv6_atual)
            if "good" in resp or "nochg" in resp:
                log(f"[IPv6] Atualizado com sucesso: {resp}")
                ultimo_ipv6 = ipv6_atual
            else:
                log(f"[IPv6] Erro na resposta: {resp}")
        elif not ipv6_atual:
            # Comum se a rede não suportar IPv6
            pass 

        # 3. Dorme
        time.sleep(INTERVALO)

if __name__ == "__main__":
    main()
