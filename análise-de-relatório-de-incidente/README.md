# Análise de Incidente: DoS Attack (NIST CSF)

Neste projeto do curso do Google, analisei um relatório de incidente sobre um ataque de negação de serviço (DoS) em uma empresa de marketing. Estruturei a análise com base nas cinco funções do framework NIST CSF para documentar como o problema foi identificado, contido e resolvido.

## Detalhes do Incidente
* **Tipo de ataque**: Inundação de pacotes ICMP (Ping Flood).
* **Impacto**: Serviços indisponíveis e interrupção total do tráfego por cerca de duas horas.
* **Causa**: Firewall de borda mal configurado que permitiu o redirecionamento de requisições ICMP para a rede interna.

## Ações de Resposta (NIST CSF)

### 1. Identificar
* Localizei a falha na configuração de filtragem do firewall de borda.
* Iniciei uma auditoria pós-incidente para catalogar e revisar as configurações de todos os ativos de segurança da rede.

### 2. Proteger
* Implementação de limitação de pacotes ICMP no firewall (Rate Limiting).
* Configuração de verificação de IPs falsificados (Anti-spoofing).
* Adoção de ferramentas de Hardening, como sistemas IDS/IPS.

### 3. Detectar
* Implementação de software de monitoramento SIEM para centralizar logs e aumentar a visibilidade.
* Configuração de alertas em tempo real no IDS/IPS para interceptar tráfego suspeito.

### 4. Responder
* Bloqueio imediato da entrada de pacotes ICMP e isolamento de serviços para mitigar danos.
* Notificação aos clientes sobre o ocorrido e sobre as novas medidas de segurança para manter a continuidade do negócio.

### 5. Recuperar
* Restauração imediata de sistemas críticos e uso de backups íntegros para os serviços não críticos.
* Definição da nova configuração do firewall como o padrão operacional (baseline) da empresa.

## Conclusão e Notas
O ataque teve sucesso por causa de uma falha básica na configuração dos equipamentos de borda. Isso reforça a necessidade de manutenção constante e de um sistema de detecção robusto para evitar a ausência de alertas prévios verificada neste caso.
