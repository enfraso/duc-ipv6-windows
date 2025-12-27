import urllib.request
import base64
import time
from datetime import datetime

# ================= CONFIGURAÇÕES =================
USERNAME = "SEU_USUARIO"
PASSWORD = "SUA_SENHA"
HOSTNAME = "SEU_REGISTRO_AAAA"
INTERVALO = 600  # 10 minutos
# =================================================

def log(mensagem):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {mensagem}")

def obter_ipv6_exclusivo():
    """
    Consulta uma API que SÓ responde via IPv6.
    Se a máquina tentar usar IPv4, isso falhará (o que é intencional).
    """
    try:
        # api6.ipify.org obriga o uso de IPv6.
        url = "https://api6.ipify.org"
        req = urllib.request.Request(url)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        log(f"Erro: Não foi possível detectar um IPv6 válido. Verifique sua conexão. Detalhes: {e}")
        return None

def forcar_update_ipv6(ipv6_address):
    """
    Envia explicitamente o endereço IPv6 para o No-IP.
    """
    # A URL padrão de update é usada, mas passamos o parâmetro myip com o endereço IPv6 explícito
    base_url = "http://dynupdate.no-ip.com/nic/update"
    full_url = f"{base_url}?hostname={HOSTNAME}&myip={ipv6_address}"
    
    # Autenticação Básica
    auth_str = f"{USERNAME}:{PASSWORD}"
    auth_bytes = auth_str.encode("ascii")
    base64_bytes = base64.b64encode(auth_bytes)
    base64_string = base64_bytes.decode("ascii")

    req = urllib.request.Request(full_url)
    req.add_header("Authorization", f"Basic {base64_string}")
    req.add_header("User-Agent", "Python IPv6-Only Updater/1.0")

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        return f"Erro na conexão com No-IP: {e}"

def main():
    log(f"--- Iniciando Script IPv6 ONLY para {HOSTNAME} ---")
    ultimo_ip_conhecido = None

    while True:
        ipv6_atual = obter_ipv6_exclusivo()

        if ipv6_atual:
            # Só atualiza se o IP mudou
            if ipv6_atual != ultimo_ip_conhecido:
                log(f"Novo IPv6 detectado: {ipv6_atual}")
                resultado = forcar_update_ipv6(ipv6_atual)
                
                if "good" in resultado or "nochg" in resultado:
                    log(f"Sucesso! No-IP respondeu: {resultado}")
                    ultimo_ip_conhecido = ipv6_atual
                else:
                    log(f"Erro ao atualizar No-IP: {resultado}")
            else:
                # Opcional: Remova o print abaixo se quiser o log mais limpo
                print(f"Monitorando... IPv6 inalterado: {ipv6_atual}")
        
        time.sleep(INTERVALO)

if __name__ == "__main__":
    main()