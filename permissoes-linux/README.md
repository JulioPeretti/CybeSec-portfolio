# Gestão de Permissões em Linux

Neste laboratório do curso do Google, atuei como analista de segurança para auditar e ajustar as permissões de arquivos de uma equipe de pesquisa. O objetivo principal foi aplicar o princípio do privilégio mínimo para proteger dados sensíveis contra acesso não autorizado.

## Tarefas executadas
* **Auditoria de diretório:** Usei o comando `ls -la` no diretório `projects` para verificar a estrutura de propriedade (usuário `researcher2` e grupo `research_team`) e as permissões atuais de arquivos visíveis e ocultos.
  
  <img width="622" height="223" alt="image" src="https://github.com/user-attachments/assets/719fb0f6-fc02-49c9-94f0-8aca6dd181bd" />

* **Ajuste de integridade:** Identifiquei que o arquivo `project_k.txt` permitia escrita para "Outros" e removi essa permissão com o comando `chmod o-w`.
* **Restrição de acesso:** O arquivo `project_m.txt` foi configurado para acesso exclusivo do proprietário através do comando `chmod 600`, removendo leitura e escrita do grupo.

  <img width="624" height="148" alt="image" src="https://github.com/user-attachments/assets/5afdffa7-83fb-4c73-9642-2c0850bb21e0" />

* **Proteção de arquivos ocultos:** Alterei o arquivo `.project_x.txt` para o modo numérico `440`, garantindo que ele fosse apenas para leitura tanto para o usuário quanto para o grupo, evitando alterações acidentais.

  <img width="626" height="180" alt="image" src="https://github.com/user-attachments/assets/24c9a2cb-adb1-4f2f-9612-3a423ffc2b8d" />

* **Controle de diretórios:** Removi a permissão de execução do grupo no diretório `drafts` (`chmod g-x`), bloqueando o acesso de outros membros da equipe à pasta de rascunhos.

* <img width="624" height="130" alt="image" src="https://github.com/user-attachments/assets/3d3e4e06-debb-458b-9541-f1bb83e53025" />

## Competências demonstradas
* Gerenciamento de permissões via CLI (Linux).
* Uso de permissões simbólicas e numéricas com o comando `chmod`.
* Análise técnica de strings de permissão para identificar riscos de segurança.
* Aplicação prática de controles de confidencialidade e integridade em sistemas de arquivos.
