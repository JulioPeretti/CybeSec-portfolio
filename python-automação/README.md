# Automação de Filtro de IPs com Python

Este script foi desenvolvido para automatizar a atualização de uma lista de IPs permitidos (allow list), removendo endereços que atingiram um limite de tentativas de login ou que constam em uma lista de bloqueio.

## Lógica do Script
O algoritmo processa dois arquivos de texto e aplica as seguintes regras de segurança:
* **Verificação de tentativas:** IPs com 3 ou mais ocorrências na lista de acesso são considerados suspeitos de brute-force e removidos.
* **Filtro de bloqueio:** IPs que constam na `remove_list.txt` são filtrados automaticamente.
* **Deduplicação:** O script garante que a nova lista não contenha endereços duplicados.
* **Atualização de arquivo:** Ao final do processamento, o arquivo original de permissões é sobrescrito com a lista limpa.

## Trecho Principal
```python
for i in allowed_list:
    if allowed_list.count(i) < 3 and i not in blocked_list and i not in new_allowed_list:
        new_allowed_list.append(i)
    elif allowed_list.count(i) >= 3:
        print(f"O IP {i} excedeu o limite de tentativas e foi bloqueado.")
