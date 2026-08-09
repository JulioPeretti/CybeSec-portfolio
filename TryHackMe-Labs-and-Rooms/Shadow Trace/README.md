# Shadow Trace

Este write-up detalha a investigação de um artefato malicioso e a posterior triagem de alertas de segurança, focando fortemente em Análise Estática de Malware, Inteligência de Ameaças (Threat Intel) e decodificação de comandos ofuscados (Base64 e ASCII) executados em memória, visando mapear toda a infraestrutura de Comando e Controle (C2) do atacante.


## Cenário: 
Após a identificação de um arquivo suspeito em um endpoint, fez-se necessário entender as reais capacidades do artefato antes de sua execução. Entender o comportamento planejado do malware, como suas técnicas de evasão e métodos de comunicação de rede, é indispensável para criar regras de bloqueio eficazes. Além disso, a análise de alertas gerados pelo sistema de monitoramento permite correlacionar o artefato estático inicial com as ações dinâmicas e furtivas tomadas pelo atacante no ambiente comprometido.

## Abordagem:
* Para a identificação primária, foi gerado o hash SHA256 do arquivo malicioso nativamente através do PowerShell (certutil -hashfile), o qual foi consultado no VirusTotal, retornando um community score de 45/70 e classificando o artefato (um PE 64-bit) como um Trojan/Downloader.
* Na análise estática da estrutura do executável via PE-bear, a checagem das abas de Imports e Strings revelou a preparação de táticas de evasão (chamadas às funções IsDebuggerPresent e Sleep), além da importação da biblioteca nativa WS2_32.dll (verificada na aba Libraries do PeStudio) para conexões de rede via sockets e urlmon.dll (URLDownloadToFileA) para baixar artefatos adicionais.
* Na fase de triagem de alertas (Shadow Trace), analisou-se execuções suspeitas nos hosts. Identificou-se comandos ofuscados no PowerShell requerendo decodificação de Base64, e injeções de JavaScript no navegador Chrome utilizando arrays de caracteres ASCII, ambos com o objetivo de burlar detecções baseadas em strings literais.

## Achado Principal:
* A partir das análises, constatou-se que o arquivo inicial mascara-se como uma atualização legítima (nomeado security-update.exe através de typosquatting no domínio tryhatme.com), possuindo capacidade de exfiltração de dados camuflados em Base64 na própria URL via requisições HTTP para o subdomínio responses.tryhatme.com.
* Aprofundando nos alertas gerados após a infecção, detectou-se o uso do processo do PowerShell para baixar um segundo estágio (payload) diretamente de https://tryhatme.com/dev/main.exe através de um comando ofuscado em Base64. Além disso, o atacante utilizou o processo do Google Chrome para executar um JavaScript que convertia código ASCII de volta para texto, forçando o download silencioso de um executável malicioso hospedado em https://reallysecureupdate.tryhatme.com/update.exe.
* É válido notar a técnica de evasão no código JavaScript, que salva o executável sob o nome test.txt (a.download='test.txt') para tentar evadir proteções baseadas em extensão de arquivo. Tais descobertas permitiram mapear por completo a infraestrutura do atacante e recuperar as flags do incidente (ex: THM{you_g0t_some_IOCs_friend}).

## Indicadores/Evidência:
Ferramentas Utilizadas: PE-bear, PowerShell (certutil), VirusTotal, Pestudio.
* IoCs (Domínios e URLs):
  * tryhatme.com
  * responses.tryhatme.com
  * https://reallysecureupdate.tryhatme.com/update.exe
  * https://tryhatme.com/dev/main.exe
* Técnicas MITRE ATT&CK:
  * T1105 (Ingress Tool Transfer)
  * T1036.005 (Masquerading: Match Legitimate Name or Location)
  * T1027 (Obfuscated Files or Information - Base64 & ASCII Array)
  * T1048.003 (Exfiltration Over Alternative Protocol: Unencrypted Non-C2 Protocol)
  * T1497.001 (Virtualization/Sandbox Evasion: System Checks)*   
