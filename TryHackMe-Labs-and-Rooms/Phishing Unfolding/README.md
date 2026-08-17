# TryHackMe - Phishing Unfolding

Este room simula o ambiente de um Centro de Operações de Segurança (SOC). O objetivo principal é realizar a triagem de alertas, identificando falsos positivos e ameaças reais de phishing, 
e em seguida conduzir uma investigação avançada utilizando o Splunk com logs do Sysmon para entender a extensão e o impacto do ataque no ambiente corporativo.


## Cenário: 
Após um ataque inicial de phishing bem-sucedido, o invasor consegue comprometer um endpoint na rede. É indispensável entender como a ameaça escalou no ambiente, identificando o roubo de arquivos sensíveis, as técnicas de evasão e, principalmente, o método utilizado para a exfiltração dos dados. 
O foco do analista é mapear todo o fluxo do ataque para erradicar a presença maliciosa e recomendar os bloqueios corretos.

## Abordagem:
* Para a triagem inicial, os alertas do dashboard do SOC foram analisados. Alertas referentes a processos legítimos do Windows (como sincronização de certificados no System32 e atualizações em background) foram classificados como falsos positivos.
* Em contrapartida, e-mails com técnicas de engenharia social focados em roubo de credenciais bancárias e automação de disparos suspeitos foram marcados como incidentes reais e escalados para bloqueio de domínio.
* Na investigação mais profunda utilizando o Splunk, os logs do Sysmon foram a principal fonte da caçada.
* Analisou-se a criação de processos para identificar comandos de reconhecimento do sistema, como o powershell.exe chamando o net.exe e realizando a evasão de defesas através do parâmetro ExecutionPolicy Bypass.
* Para rastrear a coleta de dados (Staging), buscou-se pela criação de diretórios suspeitos, como uma pasta chamada exfiltration, e o mapeamento de unidades de rede via robocopy.exe.
* O método de exfiltração foi detectado monitorando anomalias em requisições DNS (comando nslookup), onde identificou-se o uso de strings longas em Base64 para vazar arquivos ZIP em pequenos blocos.
* Para a persistência, os logs evidenciaram o download de scripts remotos em memória (Powercat) e conexões não padrão para túneis externos.
## Achado Principal:
A investigação confirmou que a campanha de phishing proveniente do domínio fashionindustrytrends.xyz obteve êxito no comprometimento do host. 
O atacante utilizou PowerShell para enumerar permissões e mapear um servidor de arquivos financeiros. 
Documentos confidenciais foram copiados, compactados em um arquivo chamado exfilt8me.zip e convertidos para Base64. 
Esses dados foram então exfiltrados silenciosamente através de diversas consultas DNS para um domínio controlado pelo atacante (haz4rdw4re.io). 
Para garantir o controle contínuo da máquina, o invasor baixou o backdoor Powercat e estabeleceu um túnel reverso ativo utilizando a infraestrutura do Ngrok.

## Indicadores/Evidência:
* Logs do Dashboard de SOC
* Logs do Splunk (Sysmon Event IDs para Process Creation e DNS Queries)
* Técnicas MITRE ATT&CK:
* * T1566.001 (Phishing: Spearphishing Attachment)
* * T1059.001 (Command and Scripting Interpreter: PowerShell)
* * T1056 (Collection: Data from Local System and Network Shared Drive)
* * T1048.003 (Exfiltration Over Alternative Protocol: DNS)
* * T1090 (Proxy: Connection Proxying via Ngrok)


