# Análise de Logs e Detecção de Scans com Python

Este script analisa logs de servidores web para identificar endereços IP com comportamento suspeito, especificamente aqueles que geram um alto volume de erros HTTP 404 (Not Found). Isso é um forte indicativo de varredura de diretórios (Directory Fuzzing) ou reconhecimento automatizado.

## Lógica do Script
O algoritmo processa o arquivo de log linha por linha e realiza as seguintes operações:
* **Mapeamento via Regex:** Utiliza a biblioteca `re` para extrair endereços IPv4 associados a requisições que retornaram o status 404.
* **Contagem de Frequência:** Armazena os IPs em um dicionário para rastrear quantas vezes cada endereço gerou o erro.
* **Flag de Comportamento:** IPs que ultrapassam o limite definido (5 ou mais erros 404) são sinalizados como potenciais ameaças.
* **Exportação:** A lista final de IPs suspeitos é consolidada e exportada para um novo arquivo (`suspects_log.txt`) para posterior bloqueio no firewall.

## Trecho Principal (Regex)
```python
# Expressão regular para capturar o IPv4 seguido por um erro 404
pattern = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).* 404"
actual_list = re.findall(pattern, line)
