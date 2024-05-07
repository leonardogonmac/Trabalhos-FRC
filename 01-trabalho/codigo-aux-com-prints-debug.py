#!/usr/bin/env python3
import socket 
import struct 
import random
import sys


def cria_pacote(nome):
    dominios = nome.split(".")
    print("dominios", dominios)
    print("--------------------------------------------------------------------------------------------")
    busca = struct.pack(">HHHHHH", random.getrandbits(16), 0x0100, 0x0001, 0x0000, 0x0000, 0x0000)
    print("busca", busca)
    for dominio in dominios:
        busca += struct.pack("B", len(dominio)) + dominio.encode()
        print("busca", busca)
    busca += struct.pack("B", 0x0000)  
    print("busca", busca)
    busca += struct.pack(">HH", 0x0002, 0x0001)
    print("busca", busca)
    return busca

def envia_e_recebe(busca, dns_server):
    for i in range(3):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)  
        sock.sendto(busca, (dns_server, 53))
        print("pacote enviado\n", busca)  
        print("--------------------------------------------------------------------------------------------")
        try:
            resposta = sock.recvfrom(512)[0]
            print("resposta recebida:\n", resposta)
            return resposta
        except socket.timeout:
            continue
    return None 

def parse_resposta(resposta, hostname):
    if resposta is None:
        print("Nao foi possivel coletar entrada NS para", hostname)
        return

    cabecalho = struct.unpack(">HHHHHH", resposta[:12])
    print("cabecalho:", resposta[:12])
    print("--------------------------------------------------------------------------------------------")
    print("12 primeiros bytes da resposta DNS")
    print("----------------------------------")
    print("0. Transaction ID:", cabecalho[0])
    print("1. Flags:", bin(cabecalho[1])) 
    print("2. Questions:", cabecalho[2])
    print("3. Answers RRs:", cabecalho[3])
    print("4. Authority RRs:", cabecalho[4])
    print("5. Additional RRs:", cabecalho[5])
    
    if((0b0000000000001111 & int(cabecalho[1]) == 0b0000000000000000) and cabecalho[3] == 0):
        print("Dominio", hostname, "nao possui entrada NS")
        return
    elif(0b0000000000001111 & int(cabecalho[1]) == 0b0000000000000011):
        print("Dominio", hostname, "nao encontrado")
        return
    elif(0b0000000000001111 & int(cabecalho[1]) == 0b0000000000000010):
        print("Nao foi possivel coletar entrada NS para", hostname)
        return
    offset = 12  
    print("--------------------------------------------------------------------------------------------")
    print("offset=", offset, "(", (int)(offset/2), "- 16bits) - cabecalho:\n", resposta[:offset])
    while resposta[offset] != 0:
        offset += 1  
    offset += 5  
    print("--------------------------------------------------------------------------------------------")
    print("offset=", offset, "(", (int)(offset/2), "- 16bits) - cabecalho + subdominios + null + QTYPE + QCLASS:\n", resposta[:offset])
    for i in range(cabecalho[3]):  
        if resposta[offset] >= 192:  
            offset += 2  
        else:
            while resposta[offset] != 0:
                offset += 1  
            offset += 1  
        print("--------------------------------------------------------------------------------------------")
        print("offset=", offset, "(", (int)(offset/2), "- 16bits - encontrou o ponteiro x0c):\n", resposta[:offset])
        tipo = struct.unpack(">H", resposta[offset:offset+2])[0] 
        offset += 8 
        print("--------------------------------------------------------------------------------------------")
        print("offset=", offset, "(", (int)(offset/2), "- 16bits) - 2 ultimos bytes eh o tipo:\n", resposta[:offset])
        print("tipo:", tipo)
        tamanho = struct.unpack(">H", resposta[offset:offset+2])[0] 
        offset += 2 
        print("--------------------------------------------------------------------------------------------")
        print("offset=", offset, "(", (int)(offset/2), "- 16bits) - 2 ultimos bytes eh o tamanho:\n", resposta[:offset])
        print("tamanho:", tamanho)
        if tipo == 2:  
            dominios = []
            print("--------------------------------------------------------------------------------------------")
            nome_srv = parse_domain(resposta, offset, dominios)
            print(hostname, "<>", nome_srv)
        offset += tamanho
        print("--------------------------------------------------------------------------------------------")
        print("offset=", offset, "(", (int)(offset/2), " - 16bits - incluindo o tamanho par recomecar):\n", resposta[:offset])
        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        print("resposta:\n", resposta)
        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")

def parse_domain(resposta, offset, dominios):
    while True:
        tam = resposta[offset]
        if tam == 0:
            offset += 1
            break
        elif tam >= 192:  
            ponteiro = struct.unpack(">H", resposta[offset:offset+2])[0]
            offset += 2
            ponteiro = ponteiro & 0x3FFF 
            return parse_domain(resposta, ponteiro, dominios) 
        else:
            offset += 1
            dominios.append(resposta[offset:offset+tam].decode()) 
            offset += tam
    return '.'.join(dominios)

if __name__ == '__main__':

    args = sys.argv[1:]

    if (len(args) != 2):
        print(f"Uso: %s <nome_do_dominio> <servidor_dns>\n", args[0])
    else:
        print("============================================================================================")
        print("inicio main - obtem argumentos")
        print("--------------------------------------------------------------------------------------------")
        dominio = args[0]
        dns_server = args[1]
        print(f"dominio: ", dominio)
        print(f"dns_server: ", dns_server)
        print("============================================================================================")
        print("\n")
        print("============================================================================================")
        print(f"Cria um pacote DNS")
        print("--------------------------------------------------------------------------------------------")
        pacote = cria_pacote(dominio)
        print("============================================================================================")
        print("\n")
        print("============================================================================================")
        print(f"Envia o pacote DNS")
        print("--------------------------------------------------------------------------------------------")
        resposta = envia_e_recebe(pacote, dns_server)
        print("============================================================================================")
        print("\n")
        print("============================================================================================")
        print(f"Analisa a resposta DNS recebida")
        print("--------------------------------------------------------------------------------------------")
        parse_resposta(resposta, dominio)
        print("============================================================================================")
        print("\n")