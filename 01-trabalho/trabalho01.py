#!/usr/bin/env python3

#Trabalho 01 - FRC
#Integrantes:
#       Heitor Marques Simões Barbosa - 202016462
#       Jose Luis Ramos Teixeira      - 190057858
#       Leonardo Goncalves Machado    - 211029405
#       Zenilda Pedrosa Vieira        - 212002907

import socket #biblioteca para criar socket UDP
import struct #biblioteca para criar pacotes UDP
import random
import sys

def cria_pacote(nome):
    # Cabecalho: [Transaction ID, Flags, QDCOUNT, ANCOUNT, NSCOUNT, ARCOUNT]
    # Transaction ID eh um numero aleatorio
    # Flag 0x0100 para busca DNS padrao
    # QDCOUNT = 1
    busca = struct.pack(">HHHHHH", random.getrandbits(16), 0x0100, 0x0001, 0x0000, 0x0000, 0x0000)

    # Colocando o dominio no padrao de busca DNS
    dominios = nome.split(".")
    for dominio in dominios:
        busca += struct.pack("B", len(dominio)) + dominio.encode()
    busca += struct.pack("B", 0x0000)  # Fim do hostname

    # QTYPE=2 para consulta NS, QCLASS=1 para IN (Internet)
    busca += struct.pack(">HH", 0x0002, 0x0001)
    return busca

def envia_e_recebe(busca, dns_server):
    for i in range(3):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)  # timeout = 2s
        sock.sendto(busca, (dns_server, 53))  #envia busca DNS para o servidor na porta 53 
        try:
            resposta = sock.recvfrom(512)[0]  # receber resposta do servidor DNS (tamanho maximo de 512 bytes)
            return resposta
        except socket.timeout:
            continue

    return None #caso nao haja resposta, retorna vazio para o parser

def parse_resposta(resposta, hostname):
    if resposta is None:
        print("Nao foi possivel coletar entrada NS para", hostname)
        return

    # Parsing do cabecalho
    cabecalho = struct.unpack(">HHHHHH", resposta[:12])
    #print("Transaction ID:", cabecalho[0])
    #print("Flags:", bin(cabecalho[1])) 
        # RCODE - ultimos 4 bits: (0 - sem erro) (1 - format error) (2 - serv. error) (3 - name error) (4 - query nao implem.) (5 - Recusado) 
    #print("Questions:", cabecalho[2])
    #print("Answers:", cabecalho[3])
    #print("Authority RRs:", cabecalho[4])
    #print("Additional RRs:", cabecalho[5])

    #Flag nao aponta erro, mas nao ha respostas NS
    if((0b0000000000001111 & int(cabecalho[1]) == 0b0000000000000000) and cabecalho[3] == 0):
        print("Dominio", hostname, "nao possui entrada NS")
        return
    #Flag aponta erro de nome
    elif(0b0000000000001111 & int(cabecalho[1]) == 0b0000000000000011):
        print("Dominio", hostname, "nao encontrado")
        return
    #Flag aponta erro de servidor
    elif(0b0000000000001111 & int(cabecalho[1]) == 0b0000000000000010):
        print("Nao foi possivel coletar entrada NS para", hostname)
        return

    offset = 12  # offset apos o cabecalho
    
    # Pular o campo de Questions
    while resposta[offset] != 0:
        offset += 1  # Pula o QName
    offset += 5  # pula o null apos o fim do nome 

    # Parser do campo de Anwers
    for i in range(cabecalho[3]):  # cabecalho[3] indica a quantidade de respostas

        if resposta[offset] >= 192:  # 192 = 0xC0, verifica inicio de um ponteiro
            offset += 2  # Pula os 2 bytes de ponteiro
        else:
            while resposta[offset] != 0:
                offset += 1  # Pula o nome
            offset += 1  # Pula o null 

        tipo = struct.unpack(">H", resposta[offset:offset+2])[0] #extrai o campo TYPE
        offset += 8 #pula campos TYPE, CLASS e TTL
        tamanho = struct.unpack(">H", resposta[offset:offset+2])[0] #extrai o campo RDLENGHT
        offset += 2 #pula campo RDLENGTH

        #offset += 10 #move o offset para depois do campo de tamanho 
        if tipo == 2:  # tipo = 2 eh NS
            dominios = []
            nome_srv = parse_domain(resposta, offset, dominios)
            print(hostname, "<>", nome_srv)

        offset += tamanho


def parse_domain(resposta, offset, dominios):
    while True:
        tam = resposta[offset]
        if tam == 0:
            offset += 1
            break
        elif tam >= 192:  # eh ponteiro
            ponteiro = struct.unpack(">H", resposta[offset:offset+2])[0]
            offset += 2
            ponteiro = ponteiro & 0x3FFF #Ajustar ponteiro
            return parse_domain(resposta, ponteiro, dominios) #passa o ponteiro como offset para ler o dominio
        else:
            offset += 1
            dominios.append(resposta[offset:offset+tam].decode()) #coloca o domain no nome
            offset += tam
    return '.'.join(dominios)

args = sys.argv[1:]

dominio = args[0]
dns_server = args[1]


pacote = cria_pacote(dominio)
#print(pacote)
resposta = envia_e_recebe(pacote, dns_server)
parse_resposta(resposta, dominio)

