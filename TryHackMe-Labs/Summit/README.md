# SUMMIT

Neste laboratório do TryHackMe o objetivo era, seguindo o Framweork de Defesa Pyramid of Pain e também o MITRE ATT&CK, realizar uma simulação de ameaça e teste de engenharia de deteccção de uma ferramenta fictícia chamada de PicoSecure.


O laboratório avança na medida que o arquivo nocivo é disponibilizado a cada etapa para análise em ambiente controlado (Malware Sandbox), sendo que a cada etapa concluída o grau de dificuldade para contenção da atividade do malware aumenta.

Para conter a atividade maliciosa do atacante, regras de monitoramento e contenção são implementadas nas respectivas etapas da Pyramid of Pain demonstradas abaixo:

## Bloqueio de Hash Values
* **Scan do arquivo em Sandbox:** Com a análise do arquivo "sample1.exe" é possível visualizar o seu respectivo HASH MD5, SHA1 e SHA256.

* **Bloqueio do HASH:** Dentro da aba Manage Hashes é possível adicionar o HASH no formato escolhido para bloqueio. Bloqueio de HASHES são consideradas atitudes triviais na defesa de um malware!
  
<img width="1910" height="814" alt="image" src="https://github.com/user-attachments/assets/8ead2fb8-7957-4cca-8147-a4ab0a9db3aa" />

## Bloqueio de IP
* **Scan do arquivo em Sandbox:** Com a análise do arquivo "sample2.exe" é possível visualizar as requisições executadas pela máquina infectada ao IP do atacante.
* O atacante utiliza a máquina infectada para realizar requisições na porta 4444 (comum em backdoors e controle remoto) do seu IP e posteriormente faz requisições a um serviço Microsoft a fim de mascarar comportamento. 


<img width="1245" height="862" alt="image" src="https://github.com/user-attachments/assets/a1c1ed3c-8a06-449b-a1e5-b67142d3b0fa" />

  ---

* **Bloqueio do IP:** Usando a ferramenta de firewall do sistema, é possível bloquear todo trafego que egressa do Network local independe do IP de origem, mas que tem como destino o IP do atacante.
* O bloqueio de IP's é considerado uma prática fácil de ser contornada pelo atacante!

---

<img width="1912" height="844" alt="image" src="https://github.com/user-attachments/assets/ee79ad4b-a32d-47ff-ab60-bb5fc4efddfe" />

## Bloqueio do Domínio
* **Scan do arquivo em Sandbox:** Com a análise do arquivo "sample3.exe" é possível visualizar o exato domínio usado pelo atacante.

* **Bloqueio do Domínio:** Dentro da aba DNS Filter é possível adicionar o respectivo domínio analisado a fim de bloquear qualquer tráfego do mesmo.
* O bloqueio de Domínio é uma prática relativamente simples de ser contornada pelo atacante, porém já pode ser considerado um incômodo.
  
<img width="1913" height="911" alt="image" src="https://github.com/user-attachments/assets/6e078f08-8593-46ce-b8fb-06835de97749" />

## Bloqueio de Host Artifacts
* **Scan do arquivo em Sandbox:** Com a análise do arquivo "sample4.exe" é possível visualizar os eventos de modificação realizados no sistema pelo malware.

<img width="1249" height="572" alt="image" src="https://github.com/user-attachments/assets/fc2b8c3e-b539-439b-b254-bf9e6d331071" />

---

* **Bloqueio da atividade nociva:** Utilizando a ferramenta de criação de regra SIGMA, através da análise de logs SYSMON (serviço de monitoramento do Windows) é possível bloquear as modificações realizadas.
* As modificações nocivas feitas pelo malware condizem a desativar o monitoramento em tempo real do Windows Defender.
* Bloquear o comportamento do malware dentro da maquina hospedeira é considerado uma atitude que gera considerável perturbação no atacante!

---
<img width="1052" height="661" alt="image" src="https://github.com/user-attachments/assets/c938047b-f316-49aa-829e-216cecc0676f" />

## Bloqueio do funcionamento da ferramenta de ataque
* **Scan do arquivo em Sandbox:** Com a análise do arquivo "sample5.exe" é possível visualizar uma enornem quantidade de requisições enviadas para o mesmo IP, como já foi dito, bloquear HASH, IP e Domínio não são muito viáveis.
* Analisando o registro de LOG do sistema é possível indentificar um padrão nas requisições.

<img width="1058" height="855" alt="image" src="https://github.com/user-attachments/assets/1c59c3cc-bb08-4c9c-bef9-cbdb69b8c732" />


---

* **Bloqueio de Conexões na Network:** Utilizando a mesma ferramenta de criação de regra SIGMA e SYSMON, é possível bloquear o tráfego baseado em alguns aspectos. Os utilizados nessa etapa foram o tamanho dos pacotes e os períodos idênticos de comunicação.
* Bloquear o comportamento do malware dentro da maquina hospedeira é considerado uma atitude que gera considerável perturbação no atacante!

---
<img width="776" height="540" alt="image" src="https://github.com/user-attachments/assets/0b79ae2c-b6b9-4fc6-bfed-e3e08bebd823" />

## Bloqueio de Procedimentos do Malware
* **Scan do arquivo em Sandbox:** Com a análise do arquivo "sample6.exe" e visualização dos LOGS do cmd, é possível perceber o comportamento do malware na execução de comando no cmd.

<img width="496" height="362" alt="image" src="https://github.com/user-attachments/assets/2d215b8e-4568-49d9-b735-b3102a05640a" />

---

* **Bloqueio dos comandos executados:** Utilizando a mesma ferramenta de criação de regra SIGMA e SYSMON, é possível bloquear o comportamento no PATH e arquivo especificado.
* Bloquear Taticas, Técnicas e Procedimentos são muito nocivos ao atacante!

---
<img width="1068" height="751" alt="image" src="https://github.com/user-attachments/assets/89b061a6-62cd-444a-bbbe-7b6ff383ecd6" />
