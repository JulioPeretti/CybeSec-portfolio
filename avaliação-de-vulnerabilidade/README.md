# Relatório de Análise de Vulnerabilidades

Este projeto consistiu em uma avaliação de riscos para um banco de dados MySQL de e-commerce que hospeda informações sensíveis (PII) e leads de clientes. O foco principal foi identificar e mitigar os riscos da exposição pública do servidor na internet.

## Descrição do Sistema
* **Ambiente**: Servidor Linux com banco de dados MySQL.
* **Segurança atual**: Conexões criptografadas via SSL/TLS.
* **Problema identificado**: O banco de dados está exposto à rede pública (porta 3306 aberta), permitindo tentativas de acesso externo mesmo com criptografia ativa.

## Avaliação de Riscos (NIST SP 800-30)
Analisei as ameaças considerando probabilidade e severidade (escala de 1 a 3):

1. **Ataques DoS (Hacker)**: Risco 9 (Probabilidade 3 / Severidade 3). Interrupção das vendas e perda financeira imediata.
2. **Exfiltração de Dados (Malware)**: Risco 6 (Probabilidade 2 / Severidade 3). Roubo de PII e violação de leis de proteção de dados (LGPD/GDPR).
3. **Network Sniffing (APT)**: Risco 4 (Probabilidade 2 / Severidade 2). Monitoramento persistente do tráfego interno.

## Estratégia de Remediação

### 1. Isolação de Rede (Zero Trust)
* Remoção do banco de dados da internet pública.
* Implementação de Firewall com política "Deny All" por padrão.
* Acesso restrito via VPN com autenticação de dois fatores (MFA).

### 2. Hardening do Sistema
* Configuração do MySQL para não rodar com privilégios de 'root' ou 'sudo'.
* Vinculação do serviço MySQL apenas à interface de rede interna (localhost/IP privado), impedindo exposição em IPs públicos.

### 3. Princípio do Privilégio Mínimo (PoLP)
* Auditoria completa das contas de usuário do banco de dados.
* Implementação de RBAC: permissões de leitura (SELECT) para analistas de marketing e permissões administrativas restritas a DBAs seniores.

### 4. Monitoramento Contínuo
* Exportação de logs de conexão e queries para um sistema SIEM.
* Configuração de alertas em tempo real para detectar tentativas de acesso não autorizado ou exportações em massa de dados.
