# Tempest

Este room é o capstone da linha SOC Level 1 do TryHackMe e simula um caso completo de resposta a incidente em um ambiente Windows. A máquina TEMPEST foi comprometida através de uma campanha de phishing, e o objetivo é 
reconstruir toda a cadeia do ataque desde o vetor inicial até o acesso administrativo persistente utilizando os artefatos forenses: logs do Sysmon (EVTX), tráfego de rede capturado (PCAP) 
e evidências decodificadas de comando e controle.



## Cenário: 
Um usuário da máquina TEMPEST (benimaru) abriu um documento do Word recebido por phishing, o que deu início a uma cadeia de comprometimento em múltiplos estágios. 
Foi preciso investigar os artefatos disponíveis para entender como o invasor obteve execução inicial, garantiu persistência, estabeleceu um canal de C2, roubou credenciais, escalou privilégios e, por fim, 
consolidou acesso administrativo de longo prazo na máquina.

## Abordagem:
* A investigação começou pela conversão do log sysmon.evtx para CSV usando o EvtxECmd (EvtxECmd.exe -f sysmon.evtx --csv <pasta> --csvf sysmon.csv), permitindo a análise cronológica dos eventos no Timeline Explorer. 
Em paralelo, o mesmo log foi exportado em XML pelo Event Viewer e carregado no SysmonView, o que facilitou visualizar as relações de processo pai/filho e as queries DNS geradas por cada binário.
* Partindo do WINWORD.EXE — vetor mais comum de exploração em arquivos .doc — foi identificada uma query DNS suspeita para o domínio phishteam.xyz, seguida da criação do arquivo
free_magicules.doc em C:\Users\benimaru\Downloads. Cruzando o PID do processo (496) com a árvore de execução no Timeline Explorer, confirmou-se que ele disparava um comando PowerShell codificado em Base64,
decodificado para um script que baixava um update.zip na pasta Startup, garantindo persistência via autostart. A análise do tráfego HTTP para phishteam.xyz (IP 167.71.199.191) no Wireshark confirmou o download
sequencial de free_magicules.doc, index.html e, no boot seguinte, do first.exe, baixado via certutil a partir do mesmo servidor — tendo o explorer.exe como parent process, evidenciando a execução automática no início da sessão.
* A partir do first.exe, identificou-se uma nova query DNS para resolvecyber.xyz (167.71.222.162), com tráfego HTTP característico de um beacon de C2: um primeiro GET de check-in, seguido de requisições GET com
parâmetro ?q= carregando strings Base64 de tamanho crescente. Decodificando esses blocos no CyberChef, foram recuperados dois artefatos importantes: o conteúdo de um script automation.ps1 contendo credenciais
em texto claro do usuário TEMPEST\benimaru (senha infernotempest), e a saída de um comando de reconhecimento de portas TCP ativas, destacando a porta 5985 (WinRM) como aberta.
* Com a porta 5985 identificada, o mesmo canal de C2 foi usado para baixar ch.exe, identificado — após pesquisa e confirmação no Timeline Explorer — como o Chisel,
ferramenta que estabelece um reverse SOCKS proxy. Esse túnel permitiu ao atacante autenticar no serviço WinRM da máquina usando a credencial roubada, obtendo uma sessão interativa completa e não mais apenas
execução isolada de comandos via C2.
* Já com acesso via WinRM, foi observado o download de spf.exe, reconhecido como o PrintSpoofer, ferramenta que abusa do privilégio SeImpersonatePrivilege para escalar de um usuário comum para SYSTEM.
O binário foi executado com o parâmetro -c, disparando C:\ProgramData\final.exe, que por sua vez abre uma conexão TCP na porta 8080. Com acesso SYSTEM em mãos, o atacante criou dois novos usuários locais
(shion e shuma), adicionando shion ao grupo local administrators. Por fim, para garantir persistência administrativa de longo prazo, foi criado um serviço Windows via sc.exe, com o comando
sc.exe \\TEMPEST create TempestUpdate2 binpath= C:\ProgramData\final.exe start= auto, configurado para iniciar automaticamente com o sistema.

## Achado Principal:
* A investigação confirmou que a campanha de phishing distribuída a partir do domínio phishteam.xyz obteve êxito ao comprometer a máquina TEMPEST através do documento free_magicules.doc, aberto pelo usuário benimaru.
* O ataque evoluiu em múltiplos estágios: persistência via pasta Startup, download de um segundo payload (first.exe) e estabelecimento de um canal de C2 em resolvecyber.xyz, através do qual o atacante exfiltrou credenciais em texto claro contidas em um script de automação esquecido na máquina.
* Com essas credenciais e um túnel SOCKS reverso via Chisel, o atacante autenticou-se no serviço WinRM (porta 5985), obtendo acesso interativo. A partir daí, abusou do SeImpersonatePrivilege com o PrintSpoofer para escalar a SYSTEM, criou usuários locais com privilégio administrativo e instalou um serviço Windows malicioso configurado para início automático, garantindo controle persistente e privilegiado sobre o host.

## Indicadores/Evidência:

* Logs Sysmon (EVTX) convertidos via EvtxECmd, analisados no Timeline Explorer e no SysmonView
* Captura de tráfego de rede (PCAP) analisada no Wireshark, filtrando por http.host
* Decodificação de payloads Base64 do canal de C2 via CyberChef
* Domínios: phishteam.xyz (167.71.199.191), resolvecyber.xyz (167.71.222.162)
* Arquivos: free_magicules.doc, update.zip, first.exe, automation.ps1, ch.exe (Chisel), spf.exe (PrintSpoofer), final.exe
* Credencial comprometida: TEMPEST\benimaru / infernotempest
* Usuários locais criados pelo atacante: shion (administrators), shuma
* Serviço malicioso persistente: TempestUpdate2 → C:\ProgramData\final.exe (start automático)
  
* Técnicas MITRE ATT&CK:

  * T1566.001 (Phishing: Spearphishing Attachment)
  * T1204.002 (User Execution: Malicious File)
  * T1547.001 (Boot or Logon Autostart Execution: Startup Folder)
  * T1059.001 (Command and Scripting Interpreter: PowerShell)
  * T1027 (Obfuscated Files or Information: Base64)
  * T1071.001 (Application Layer Protocol: Web Protocols — C2 sobre HTTP)
  * T1552.001 (Unsecured Credentials: Credentials In Files)
  * T1046 (Network Service Discovery)
  * T1572 (Protocol Tunneling — Chisel/SOCKS)
  * T1021.006 (Remote Services: Windows Remote Management)
  * T1134.001 (Access Token Manipulation: Token Impersonation/Theft — PrintSpoofer)
  * T1136.001 (Create Account: Local Account)
  * T1543.003 (Create or Modify System Process: Windows Service)

