# duc-ipv6-windows
Um script em Python que funciona como Cliente de Atualização Dinâmica (DUC) para o site noip.com. Ele suporta endereços IPv4 e IPv6 simultaneamente.

Este projeto utiliza uma adaptação do script `noip-duc`. Ele funciona como um Cliente de Atualização Dinâmica (DUC) para o **noip.com**, com foco em garantir a conectividade IPv6 para servidores atrás de CGNAT ou firewalls restritivos.

#  Descrição
O script monitora o endereço IPv6 público da máquina e atualiza o registro DNS no No-IP sempre que uma mudança é detectada. 

Diferente do cliente oficial do Windows, esta versão:
1.  Foi modificada para **Python puro** (sem necessidade de instalar bibliotecas extras como `requests`).
2.  Possui lógica específica para forçar a detecção de **IPv6**, essencial para o funcionamento correto do servidor web (Caddy).

#  Requisito Crítico (Configuração no Site)

Para que o IPv6 funcione, você **PRECISA** configurar o painel do No-IP:

1.  Acesse [https://my.noip.com/dynamic-dns](https://my.noip.com/dynamic-dns).
2.  Edite seu hostname.
3.  Certifique-se de que existe um **registro AAAA (IPv6)** criado.
    * *Se não houver um registro AAAA, o No-IP aceitará a atualização, mas salvará apenas o IPv4, quebrando o acesso ao seu servidor Caddy.*

#  Instalação e Uso (Windows)

### 1. Configuração do Script
Abra o arquivo `noip_ipv4_and_ipv6.py` com um editor de texto (Notepad, VS Code) e edite as variáveis no topo:

```python
USERNAME = "seu_usuario_noip"
PASSWORD = "sua_senha_noip"
HOSTNAME = "seu_registro_AAAA"
INTERVALO = 600  # Tempo em segundos (600 = 10 minutos)
