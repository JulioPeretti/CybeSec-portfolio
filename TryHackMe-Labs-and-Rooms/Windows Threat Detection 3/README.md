# Windows Threat Detection 3

O último dos rooms de Windows Threat Detection, os quais focavam bastante no uso do Event Viewer, utilizando os diversos ID's para filtragem e também os logs com mais detalhes providos pelo Sysmon afim de detectar
Initial Access, Discovery, Collection, Transfering Tools e Persistence, sendo esse último disposto no Write-Up a seguir. 


## Cenário: 
Após um atacante obter acesso e extrair dados, pode ser interessante manter controle ou acesso ao sistema, a partir disso é possível constantemente gerar ameaça a organização. É indispensável ter conhecimento de como
identificar esses rastros de persistência e de C2 (Command and Control) afim de erradicar a ameaça. 

## Abordagem:
* Para casos de C2, é possível analisar a partir do Sysmon eventos com ID 11 (File Created) para identificar o download do arquivo malicioso, assim como o ID 1 (Process Create) para execução do mesmo e ID 22 (DNS Query) para
transferência de dados a um domínio.
* Para persistência, foram checadas as tentativas de login em usuários administradores a partir das falhas apontadas pelo Security Event ID 4625 e do sucesso do ID 4624. Por seguinte o atacante pode tentar mudar a senha
de usuários sobre seu controle (Security ID 4724) ou criar um novo (Security ID 4720) e adiciona-lo a um grupo com mais permissões (Security ID 4732), assim criando seu backdoor de usuario no sistema.
* Para manter controle sobre o malware antes injetado, o atacante pode tornar seu arquivo malicioso um Serviço que inicia com o boot do sistema ou uma Task que ativa com um gatilho.
* Nesses casos é possível identificar a criação de um novo serviço a partir do Sysmon ID 1 (sc.exe create) ou via Security event ID 4697, com destaque para a checagem de parent process services.exe. Para tarefas usa-se o
Sysmon ID 1 (schtasks.exe /create) ou via Security event ID 4698.
* Outra forma de executar o arquivo que gera esse canal de controle é o adicionando a pasta Startup do Windows, sendo possível identificar essa adição no Sysmon ID 11, verificando os logs pós boot é possível verificar que
o respectivo malware é executado assim que o sistema inicia tendo um parente padrão chamado explorer.exe, forçando assim a verificação do campo CommandLine e Image no log para verificar a que arquivo aquele log é respectivo,
já que pode existir outros arquivos não nocivos nessa pasta Startup que constarão com o mesmo parente.
* Semelhante ao Startup pode-se adicionar uma chave contendo o caminho do arquivo a ser executado após o boot na pasta Run do Windows. Isso é detectado no Sysmon ID 13 (Registry Value Set), podendo ser possivel visualizar
o arquivo adicionado em Details.

## Achado Principal:
A partir de diferentes abordagens foi possível checar tentativas mal sucedidas de login e posteriormente um acesso confirmado a conta administrador, a qual criou um novo usuario com nome "support" para servir como backdoor e adicionou o mesmo a um grupo com privilégios. Um malware então foi injetado chamado Nessie, o qual foi atrelado a um serviço chamado Data Protection Service. Um Cavalo de Troia também existia e foi vinculado a uma task que o executava após a inicialização do sistema e estava disfarçada com o nome AmazonSync. Por fim outro malware existia e estava disposto na pastar Startup, e outro chamado Kitten era executado pelo explorer.exe porém a partir de uma chave chamada Basket contida em run, que o executava também logo após a inicialização do sistema. 

## Indicadores/Evidência:
* Logs do Event Viewer
* Logs do Sysmon
* Técnicas MITRE ATT&CK:
  - T1547.001 (Boot or Logon Autostart Execution: Registry Run Keys / Startup Folder)
  - T1543.003 (Create or Modify System Process: Windows Service)
  - T1105 (Ingress Tool Transfer)


