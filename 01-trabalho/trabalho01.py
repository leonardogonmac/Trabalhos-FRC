import socket
import struct
import random

def create_ns_query(domain):
    # Header: [Transaction ID, Flags, QDCOUNT, ANCOUNT, NSCOUNT, ARCOUNT]
    # Transaction ID is arbitrary but should be random for security reasons
    # Flags set to 0x0100 for standard query
    # QDCOUNT (number of questions) = 1
    query = struct.pack(">HHHHHH", random.getrandbits(16), 0x0100, 0x0001, 0x0000, 0x0000, 0x0000)
    # Encode the domain name to DNS labels format
    labels = domain.split(".")
    for label in labels:
        query += struct.pack("B", len(label)) + label.encode()
    query += struct.pack("B", 0)  # End of domain name label
    # QTYPE=2 for NS records, QCLASS=1 for IN (Internet)
    query += struct.pack(">HH", 2, 1)
    return query

def send_dns_query(query, dns_server):
    # Create a UDP socket
    for i in range(3):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(2)  # Set a timeout of 2 seconds
            sock.sendto(query, (dns_server, 53))  # DNS uses port 53
            try:
                data, _ = sock.recvfrom(512)  # DNS response size limit is 512 bytes
                return data
            except socket.timeout:
                continue

    return None

def parse_dns_response(response):
    if response is None:
        print("No response received.")
        return

    # Parsing the response header
    header = struct.unpack(">HHHHHH", response[:12])
    print("Transaction ID:", header[0])
    print("Flags:", header[1])
    print("Questions:", header[2])
    print("Answers:", header[3])
    print("Authority RRs:", header[4])
    print("Additional RRs:", header[5])
    
    offset = 12  # Initial offset after the header
    # Skip over the question section
    while response[offset] != 0:
        offset += 1  # Skip the domain name
    offset += 5  # Skip the null byte + Type (2 bytes) + Class (2 bytes)

    # Process each answer
    for _ in range(header[3]):  # header[3] is the ANCOUNT
        # Check for a pointer (common in responses)
        if response[offset] >= 192:  # 192 = 0xC0, the start of a pointer
            offset += 2  # Skip the pointer
        else:
            while response[offset] != 0:
                offset += 1  # Skip the domain name
            offset += 1  # Skip the null byte

        type, cls, ttl, rdlength = struct.unpack(">HHIH", response[offset:offset + 10])
        offset += 10
        print("\nAnswer:")
        print("Type:", type, "Class:", cls, "TTL:", ttl, "Data length:", rdlength)

        if type == 2:  # Type 2 is NS
            name = []
            name_server = parse_name(response, offset, name)
            print("Name Server:", name_server)


        # For type A (IPv4 address), read and print the IP address
        if type == 1 and cls == 1:  # Type 1 is A, Class 1 is IN
            ip_addr = socket.inet_ntoa(response[offset:offset + rdlength])
            print("IP Address:", ip_addr)

        offset += rdlength


def parse_name(response, offset, name):
    # This function needs to handle pointers properly to parse domain names
    while True:
        length = response[offset]
        if length == 0:
            offset += 1
            break
        elif length >= 192:  # This is a pointer
            pointer = struct.unpack(">H", response[offset:offset+2])[0]
            offset += 2
            # Dereference pointer (note: pointer offset is from the start of the packet, adjust if needed)
            return parse_name(response, pointer & 0x3FFF, name)
        else:
            offset += 1
            name.append(response[offset:offset+length].decode())
            offset += length
    return '.'.join(name)

hostname = input()
dns_server = input()

query = create_ns_query(hostname)
print(query)

response = send_dns_query(query, dns_server)
parse_dns_response(response)

