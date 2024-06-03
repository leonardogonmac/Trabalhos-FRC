<!-- 
o qual sistema operacional foi usado na construção do sistema;
o quais foram as aplicações demandadas na implementação da rede LAN;
o como implementar a rede LAN;
o como validar a configuração da rede LAN;
o quais são as limitações conhecidas  -->

# Trabalho 2 FRC

- Data: 31/05/2024

<a name="top0"></a>

## Sumário
- [Trabalho 2 FRC](#trabalho-2-frc)
  - [Sumário](#sumário)
  - [1. Integrantes](#1-integrantes)
  - [2. SO Usado](#2-so-usado)
  - [3. Ambiente de Desenvolvimento](#3-ambiente-de-desenvolvimento)
  - [4. Objetivo](#4-objetivo)
  - [5. Revisão de técnicas e ferramentas para a configuração de redes de computadores usando as ferramentas tipicamente disponíveis nos sistemas GNU/Linux e \*NIX.](#5-revisão-de-técnicas-e-ferramentas-para-a-configuração-de-redes-de-computadores-usando-as-ferramentas-tipicamente-disponíveis-nos-sistemas-gnulinux-e-nix)
  - [6. Implementações e Questões para Estudo](#6-implementações-e-questões-para-estudo)
    - [6.1. Configurar a Interface WAN](#61-configurar-a-interface-wan)
      - [6.1.1. Configuração da Interface WAN:](#611-configuração-da-interface-wan)
      - [6.1.2. Reinicialização da Interface](#612-reinicialização-da-interface)
      - [6.1.3. Verificação do endereço configurado](#613-verificação-do-endereço-configurado)
    - [6.2. Configurar a Interface LAN](#62-configurar-a-interface-lan)
      - [6.2.1. Configuração da Interface LAN](#621-configuração-da-interface-lan)
      - [6.2.2. Reinicialização da Interface](#622-reinicialização-da-interface)
      - [6.2.3. Verificação do endereço configurado](#623-verificação-do-endereço-configurado)
    - [6.3. Configurar o NAT com iptables](#63-configurar-o-nat-com-iptables)
      - [6.3.1. Habilitação do IP Forwarding](#631-habilitação-do-ip-forwarding)
      - [6.3.2. Configuração do iptables para NAT](#632-configuração-do-iptables-para-nat)
      - [6.3.3. Salvar a Configuração do iptables](#633-salvar-a-configuração-do-iptables)
    - [6.4. Configuração do Serviço DHCP](#64-configuração-do-serviço-dhcp)
      - [6.4.1. Instalação do Servidor DHCP](#641-instalação-do-servidor-dhcp)
      - [6.4.2. Configuração do Servidor DHCP](#642-configuração-do-servidor-dhcp)
      - [6.4.3. Configuração de uma Lease Estática](#643-configuração-de-uma-lease-estática)
      - [6.4.4. Definição da Interface para o Servidor DHCP](#644-definição-da-interface-para-o-servidor-dhcp)
      - [6.4.5. Reinicialização do Serviço DHCP](#645-reinicialização-do-serviço-dhcp)
      - [6.4.6. Verificação das Leases DHCP](#646-verificação-das-leases-dhcp)
- [Reescrever a parte abaixo, está igual ao TCC](#reescrever-a-parte-abaixo-está-igual-ao-tcc)
- [TEM ALGUMAS DICAS NO TCC PARA VERIFICAR SE ESTA USANDO O DHCP CORRETO ENTRE OUTROS TESTES QUE PODEM SER FEITOS](#tem-algumas-dicas-no-tcc-para-verificar-se-esta-usando-o-dhcp-correto-entre-outros-testes-que-podem-ser-feitos)
  - [7. Testes e Validação](#7-testes-e-validação)
    - [7.1 Validar Conectividade WAN e LAN](#71-validar-conectividade-wan-e-lan)
      - [7.1.1. Teste de conectividade entre equipamentos da rede privada e o gateway com NAT](#711-teste-de-conectividade-entre-equipamentos-da-rede-privada-e-o-gateway-com-nat)
      - [7.1.2. Teste de conectividade entre equipamentos da rede privada e equipamentos situados na rede de saída do gateway](#712-teste-de-conectividade-entre-equipamentos-da-rede-privada-e-equipamentos-situados-na-rede-de-saída-do-gateway)
      - [7.1.3. Teste de conectividade entre equipamentos da rede privada e equipamentos na rede externa](#713-teste-de-conectividade-entre-equipamentos-da-rede-privada-e-equipamentos-na-rede-externa)
    - [7.2. Validar NAT](#72-validar-nat)
      - [7.2.1. Testar Tradução de Endereços](#721-testar-tradução-de-endereços)
    - [7.3. Isolamento de Segmento](#73-isolamento-de-segmento)
      - [7.3.1. Verificar o Isolamento](#731-verificar-o-isolamento)
  - [8. Limitações Conhecidas](#8-limitações-conhecidas)


<a name="top1"></a>

## 1. Integrantes

- Heitor Marques Simões Barbosa ..... 202016462
- José Luís Ramos Teixeira ..................... 190057858
- Leonardo Goncalves Machado ......... 211029405
- Zenilda Pedrosa Vieira ......................... 212002907

<a name="top2"></a>

## 2. SO Usado
O sistema foi criado e testado usando a versão do ???????

<a name="top3"></a>

## 3. Ambiente de Desenvolvimento
Para o ambiente de desenvolvimento foi utilizado ???????

[(Sumário - voltar ao topo)](#top0)


<a name="top4"></a>

## 4. Objetivo
Esse trabalho tem como principal objetivo exercitar conceitos de configuração de redes de computadores. Utilizando equipamentos do LDS, foi criado e testado um passo a passo para configurar uma rede privada LAN, conectada a um roteador com interface de rede WAN e um gateway.

[(Sumário - voltar ao topo)](#top0)


<a name="top5"></a>

## 5. Revisão de técnicas e ferramentas para a configuração de redes de computadores usando as ferramentas tipicamente disponíveis nos sistemas GNU/Linux e *NIX.

??????? EXPLICAR AS FERRAMENTAS UTILIZADAS COM BREVES DEFINIÇÕES

`ifconfig` -> ip addr show
`ip`
`iptables`
`systemctl`
`dhcpd`
`nano`
outros ???????

??????? E CITAR O PACOTES NECESSÁRIOS COM BREVE DESCRIÇÃO

`iptables`
`isc-dhcp-server`
outros ???????

[(Sumário - voltar ao topo)](#top0)

<a name="top6"></a>

## 6. Implementações e Questões para Estudo

Para implementar a configuração da rede em estudo, considerou-se como base uma rede de acesso de segmento 192.168.133.0/24 (rede cabeada do LDS), com gateway em 192.168.133.1. Assim, definimos:
- Rede de Acesso: 192.168.133.0/24
- Gateway da Rede de Acesso: 192.168.133.1
- Rede LAN: 10.1.0.0/16

COLOCAR DESENHO DA REDE MONTADA ???????

- Antes de tudo, desativamos os serviços de suporte às configurações de rede com o seguinte comando para realizar a configuração manual das placas de rede, também chamada de configuração estática.
```bash
sudo service NetworkManager stop
```

- E verificamos como estão os IPs das duas placas de rede instaladas no computador usando o comando:
```bash
sudo ifconfig -a
```
- E a resposta desse comando foi:

PRINT DA RESPOSTA
BREVE ANALISE DA RESPOSTA


<a name="top6.1"></a>

### 6.1. Configurar a Interface WAN
Iniciamos configurando um roteador em que a interface de rede WAN assumisse um IP da rede de acesso 192.168.133.0/24. 

#### 6.1.1. Configuração da Interface WAN:
- Editamos o arquivo `/etc/network/interfaces`:
```bash
sudo nano /etc/network/interfaces
```

- Adicionamos (ou modificamos ????) a configuração da interface WAN para colocar essa interface configurável de forma estática, assumindo `eno1`:
```plaintext
auto eno1
iface eno1 inet static
    address 192.168.133.2
    netmask 255.255.255.0
    gateway 192.168.133.1
```

#### 6.1.2. Reinicialização da Interface
- Reiniciamos a interface com o seguinte comando
```bash
sudo ifdown eno1 && sudo ifup eno1
```

#### 6.1.3. Verificação do endereço configurado
- Para verificar se o endereço foi configurado corretamente, usamos o comando
```bash
sudo ifconfig -a
```
- E a resposta desse comando foi:

PRINT DA RESPOSTA
BREVE ANALISE DA RESPOSTA

[(Sumário - voltar ao topo)](#top0)

<a name="top6.2"></a>

### 6.2. Configurar a Interface LAN
Em seguida, continuamos a configuração considerando que a rede LAN provida através desse trabalho seja uma subrede /16 usando as faixas de IP reservadas na Internet para esse tipo de configuração, 10.1.0.0/16. 

#### 6.2.1. Configuração da Interface LAN
- Da mesma forma feita anteriormente, editamos o arquivo `/etc/network/interfaces`:
```bash
sudo nano /etc/network/interfaces
```

- Adicionamos a configuração da interface LAN para colocar essa interface configurável de forma estática, assumindo `enp5s0`:
```plaintext
auto enp5s0
iface enp5s0 inet static
    address 10.1.0.1
    netmask 255.255.0.0
```

#### 6.2.2. Reinicialização da Interface
- Reiniciamos a interface com o seguinte comando:
```bash
sudo ifdown enp5s0 && sudo ifup enp5s0
```

#### 6.2.3. Verificação do endereço configurado
- Para verificar se o endereço foi configurado corretamente, usamos o comando
```bash
sudo ifconfig
```
- E a resposta desse comando foi:

PRINT DA RESPOSTA
BREVE ANALISE DA RESPOSTA

[(Sumário - voltar ao topo)](#top0)

<a name="top6.3"></a>

### 6.3. Configurar o NAT com iptables
Para realizar o mapeamento entre o IP da rede de acesso e os IPs da rede privada LAN criada foi utilizado o serviço de NAT, conforme descrito a seguir.

#### 6.3.1. Habilitação do IP Forwarding
- Editarmos o arquivo `/etc/sysctl.conf`:
```bash
sudo nano /etc/sysctl.conf
```

- Removemos o comentário da seguinte linha para ativar o encaminhamento de pacotes IP (_IP forwarding_)::
```plaintext
net.ipv4.ip_forward=1
```

- Aplicamos a mudança:
```bash
sudo sysctl -p
```

#### 6.3.2. Configuração do iptables para NAT
- Após a configuração da interface de saída WAN (eno1) e a configuração da interface interna LAN (enp5s0) sem DHCP, realizamos a limpeza de eventuais regras de _firewall_ presentes no equipamento:
```bash
sudo iptables --flush
sudo iptables --table nat --flush
sudo iptables --delete-chain
sudo iptables --table nat --delete-chain
sudo iptables -t nat -A POSTROUTING -o eno1 -j MASQUERADE
sudo iptables -A FORWARD -i enp5s0 -o eno1 -j ACCEPT
sudo iptables -A FORWARD -i eno1 -o enp5s0 -m state --state RELATED,ESTABLISHED -j ACCEPT
```
NO EXPERIMENTO DO TCC NAO TEM A ULTIMA LINHA. PRECISA?????

#### 6.3.3. Salvar a Configuração do iptables
- E para finalizar, salvamos as configurações efetivadas:  
```bash
sudo apt-get install iptables-persistent
sudo netfilter-persistent save
sudo netfilter-persistent reload
```
6.3.3 NAO TEM NO EXPERIMENTO DO TCC. PRECISA FAZER????????


```bash
sudo iptables -L -v -n
```
<a name="top6.4"></a>

### 6.4. Configuração do Serviço DHCP
Após a configuração do serviço NAT, implementamos o serviço de DHCP para prover as configurações de redes para os clientes da LAN recém criada.

#### 6.4.1. Instalação do Servidor DHCP
- Primeiramente, instalamos o servidor DHCP com os seguintes comandos:
```bash
sudo apt-get update
sudo apt-get install isc-dhcp-server
```

#### 6.4.2. Configuração do Servidor DHCP
- A seguir, editamos o arquivo `/etc/dhcp/dhcpd.conf`:
```bash
sudo nano /etc/dhcp/dhcpd.conf
```
 
ATENÇÃO: É normal ocorrer uma falha, pois, ao finalizar a instalação, ele tenta iniciar o servidor que não tem nenhum escopo DHCP criado ainda. (TCC)

- Adicionamos a configuração para a rede LAN, partindo do princípio que há um servidor DNS provido no IP 192.168.133.1.:
```plaintext
subnet 10.1.0.0 netmask 255.255.0.0 {
    range 10.1.0.10 10.1.0.100;
    option routers 10.1.0.1;
    option subnet-mask 255.255.0.0;
    option domain-name-servers 192.168.133.1;
}
```

==================================================
NO TCC TA DIFERENTE. QUAL VAMOS USAR??????
```bash
# Exemplo de configuração
# Tempo de lease: default mínimo (10 min) e máximo (2 hs)
# Outros valores: 86400 (1 dia), 604800 (1 semana) e 2592000 (30 dias)
default-lease-time 600;
max-lease-time 7200;
# Reconhece e corrige pedidos de endereços incoerentes
authoritative;
# Opções de rede comuns
option subnet-mask 255.255.255.0;
option broadcast-address 192.168.1.255;
option routers 192.168.1.1;
option domain-name-servers 192.168.1.1;
option domain-name "mydomain.org";
# Pode-se incluir opções especificas para uma subrede
subnet 192.168.1.0 netmask 255.255.255.0 {
 range 192.168.1.2 192.168.1.100;
 range 192.168.1.150 192.168.1.200;
}
# Para designar WINS server para estacões WIN
#option netbios-name-servers 192.168.1.1;
# Para atribuir um endereço especifico para um MAC - suporte a clientes
# BOOTP
host haagen {
 option host-name “leao.labredes.unb.br”;
 hardware ethernet 08:00:2b:4c:59:23;
 fixed-address 192.168.1.222;
}
```
==================================================


- Para conferir se a alteração do arquivo `/etc/dhcp/dhcpd.conf` foi feita corretamente, usamo o seguinte comando:
```bash
sudo dhcpd -t
```

- E a resposta desse comando foi:

PRINT DA RESPOSTA
BREVE ANALISE DA RESPOSTA


#### 6.4.3. Configuração de uma Lease Estática
- Para determinada máquina de testes de configurações da LAN criada, vinculamos um endereço IP de forma que aquele equipamento receba sempre o mesmo endereço como oferta do servidor DHCP. Para isso, adicionamos ao arquivo `/etc/dhcp/dhcpd.conf` as linhas de comando a seguir:
```plaintext
host test-machine {
   hardware ethernet DC:0E:A1:C8:AE:68; # MAC address da máquina de teste
   fixed-address 10.1.0.50;
}
```

#### 6.4.4. Definição da Interface para o Servidor DHCP
- Editamos o arquivo `/etc/default/isc-dhcp-server`:
```bash
sudo nano /etc/default/isc-dhcp-server
```

- Adicionamos (ou modificamos ?????) a linha a seguir para sempre disparar o serviço somente na interface enp5s0:
```plaintext
INTERFACESv4="enp5s0"   
```


#### 6.4.5. Reinicialização do Serviço DHCP
- Após todas as configurações feitas, é necessário reinicializar o servidor para que as alterações tenham efeito.
```bash
sudo systemctl restart isc-dhcp-server
```

Indique como conferir as leases providas pelo servidor DHCP em arquivos de log.
#### 6.4.6. Verificação das Leases DHCP
- Visualizamos o arquivo de leases em `/var/lib/dhcp/dhcpd.leases` para verificar as leases providas pelo servidor DHCP:
```bash
cat /var/lib/dhcp/dhcpd.leases
```

- E a resposta desse comando foi:

PRINT DA RESPOSTA
BREVE ANALISE DA RESPOSTA

Reescrever a parte abaixo, está igual ao TCC
=====
- Após a configuração do servidor DHCP, caso apresente algum problema e não esteja funcionando, pode ser necessário verificar os arquivos de log do sistema (/var/log/syslog), com o seguinte comando:
```bash
grep dhcpd /var/log/syslog
```
=====



TEM ALGUMAS DICAS NO TCC PARA VERIFICAR SE ESTA USANDO O DHCP CORRETO ENTRE OUTROS TESTES QUE PODEM SER FEITOS
=====
ATENÇÃO: Caso o comando ifconfig não aponte o ip adquirido através do DHCP, pode ser necessário reiniciar a interface de rede (ifdown <interface> + ifup <interface>) ou dhclient <interface>

Verifique se o cliente está usando o servidor DHCP correto:
```bash
sudo dhclient -v
```

Através do arquivo de leases, verifique as concessões ativas do servidor dhcp:
``` bash
sudo cat /var/lib/dhcp/dhcpd.leases | less
```
=====

<a name="top7"></a>

## 7. Testes e Validação

Foi gerada uma lista de testes necessários para validar essa solução.
- Validar a conectividade WAN e LAN
- Verificar a tradução de endereço (NAT)
- Verificar o isolamento de segmento (NAT) da rede WAN.

<a name="top6.1"></a>

### 7.1 Validar Conectividade WAN e LAN

#### 7.1.1. Teste de conectividade entre equipamentos da rede privada e o gateway com NAT

- A partir do equipamento da rede provada que criamos: 

  - Para testar a conectividade WAN enviamos pacotes ICMP para o gateway
```bash
ping 192.168.133.1
```
  - Obtemos a seguinte resposta:

    PRINT DA RESPOSTA
    BREVE ANALISE DA RESPOSTA

#### 7.1.2. Teste de conectividade entre equipamentos da rede privada e equipamentos situados na rede de saída do gateway

  - Também tentamos enviar pacotes ICMP para algum outro computador que estava conectado à outra rede para conferir as configurações de roteamento
```bash
ping 192.168.133.1    ALTERAR IP PARA UM COMPUTADOR FORA DA REDE
```
  - Obtemos a seguinte resposta:

    PRINT DA RESPOSTA
    BREVE ANALISE DA RESPOSTA

#### 7.1.3. Teste de conectividade entre equipamentos da rede privada e equipamentos na rede externa

  - E por fim, tentamos enviar pacotes ICMP para algum outro computador que estava conectado à mesma rede para testar a conectividade básica
```bash
ping 192.168.133.1    ALTERAR IP PARA UM COMPUTADOR FORA DA REDE
```
- Obtemos a seguinte resposta:

    PRINT DA RESPOSTA
    BREVE ANALISE DA RESPOSTA

- Em uma máquina cliente da rede LAN, obtenha um endereço IP e teste a conectividade:
```bash
dhclient eno1
ping 10.0.0.1
```

- Obtemos a seguinte resposta:

PRINT DA RESPOSTA

### 7.2. Validar NAT
Tradução de endereço (NAT)

#### 7.2.1. Testar Tradução de Endereços
- ?
- Verifique se a máquina cliente da LAN consegue acessar a internet:
```bash
ping 8.8.8.8
```
### 7.3. Isolamento de Segmento
Tradução de endereço (NAT)

#### 7.3.1. Verificar o Isolamento
- ?
- As máquinas na LAN não devem conseguir acessar diretamente outras máquinas na rede WAN (exceto através do roteador):
```bash
ping 192.168.133.2 # Deve responder
ping 192.168.133.3 # Não deve responder (a menos que configurado de outra forma)
```


<a name="top7"></a>

## 8. Limitações Conhecidas


[(Sumário - voltar ao topo)](#top0)


