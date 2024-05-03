#!/usr/bin/env python3
import socket #biblioteca para criar socket UDP
import struct #biblioteca para criar pacotes UDP
import random
import sys

def cria_pacote(hostname):
    # Cabecalho: [Transaction ID, Flags, QDCOUNT, ANCOUNT, NSCOUNT, ARCOUNT]
    # Transaction ID eh um numero aleatorio
    # Flag 0x0100 para busca DNS padrao
    # QDCOUNT = 1
    busca = struct.pack(">HHHHHH", random.getrandbits(16), 0x0100, 0x0001, 0x0000, 0x0000, 0x0000)

    # Colocando o dominio no padrao de busca DNS
    dominios = hostname.split(".")
    for dominio in dominios:
        busca += struct.pack("B", len(dominio)) + dominio.encode()
    busca += struct.pack("B", 0x0000)  # Fim do hostname

    # QTYPE=2 para consulta NS, QCLASS=1 para IN (Internet)
    busca += struct.pack(">HH", 0x0002, 0x0001)
    return busca

def envia_e_recebe(busca, dns_server):
    for i in range(3):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(2)  # timeout = 2s
            sock.sendto(busca, (dns_server, 53))  #envia busca DNS para o servidor na porta 53 
            try:
                resposta, _ = sock.recvfrom(512)  # receber resposta do servidor DNS (tamanho maximo de 512 bytes)
                return resposta
            except socket.timeout:
                continue

    return None #caso nao haja resposta, retorna vazio para o parser

def parse_resposta(resposta, hostname):
    if resposta is None:
        print("Ficou no vacuo")
        return

    # Parsing the response header
    cabecalho = struct.unpack(">HHHHHH", resposta[:12])
    #print("Transaction ID:", cabecalho[0])
    print("Flags:", cabecalho[1])
    #print("Questions:", cabecalho[2])
    #print("Answers:", cabecalho[3])
    #print("Authority RRs:", cabecalho[4])
    #print("Additional RRs:", cabecalho[5])
    
    offset = 12  # Initial offset after the header
    # Skip over the question section
    while resposta[offset] != 0:
        offset += 1  # Skip the domain name
    offset += 5  # Skip the null byte + Type (2 bytes) + Class (2 bytes)

    # Process each answer
    for _ in range(cabecalho[3]):  # header[3] is the ANCOUNT
        # Check for a pointer (common in responses)
        if resposta[offset] >= 192:  # 192 = 0xC0, the start of a pointer
            offset += 2  # Skip the pointer
        else:
            while resposta[offset] != 0:
                offset += 1  # Skip the domain name
            offset += 1  # Skip the null byte

        type, cls, ttl, rdlength = struct.unpack(">HHIH", resposta[offset:offset + 10])
        offset += 10
        if type == 2:  # Type 2 is NS
            nome = []
            name_server = parse_domain(resposta, offset, nome)
            print(hostname, "<>", name_server)


        # For type A (IPv4 address), read and print the IP address
        #if type == 1 and cls == 1:  # Type 1 is A, Class 1 is IN
        #   ip_addr = socket.inet_ntoa(response[offset:offset + rdlength])
        #    print("IP Address:", ip_addr)

        offset += rdlength


def parse_domain(resposta, offset, nome):
    # This function needs to handle pointers properly to parse domain names
    while True:
        tam = resposta[offset]
        if tam == 0:
            offset += 1
            break
        elif tam >= 192:  # This is a pointer
            pointer = struct.unpack(">H", resposta[offset:offset+2])[0]
            offset += 2
            # Dereference pointer (note: pointer offset is from the start of the packet, adjust if needed)
            return parse_domain(resposta, pointer & 0x3FFF, nome)
        else:
            offset += 1
            nome.append(resposta[offset:offset+tam].decode())
            offset += tam
    return '.'.join(nome)

args = sys.argv[1:]

hostname = args[0]
dns_server = args[1]

query = cria_pacote(hostname)

resposta = envia_e_recebe(query, dns_server)
parse_resposta(resposta, hostname)

