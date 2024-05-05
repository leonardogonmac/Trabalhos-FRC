// Cliente de Socket de Escopo Local
//
// apos executar ./socket-server /tmp/socket em outro terminal
// compile e execute
// ./socket-client /tmp/socket2 "Hello, world"
// ./socket-client /tmp/socket2 "This is a test"
// ./socket-client /tmp/socket "quit"

#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>

/* Escreve TEXT para o socket fornecido pelo descritor de arquivo SOCKET_FD. */

void write_text (int socket_fd, const char* text)
{
    /* Escreve o numero de bytes na sequencia de caracteres, incluindo
    o caractere de fim de sequencia de caracteres. */
    int length = strlen (text) + 1;

    write (socket_fd, &length, sizeof (length));

    /* escreve a sequencia de caracteres. */
    write (socket_fd, text, length);
}

int main (int argc, char* const argv[])
{
    const char* const socket_name = argv[1];
    const char* const message = argv[2];
    int socket_fd;
    struct sockaddr_un name;

    /* Cria o socket. */
    socket_fd = socket (PF_LOCAL, SOCK_STREAM, 0);
    // PF_LOCAL = escopo do socket -> nesse caso local (poderia ser usado PF_UNIX tambem)
    // para escopo de internet -> PF_INET
    // SOCK_STREAM = estilo da comunicacao -> estilo de conexao 
    // SOCK_DGRAM -> estilo do tipo datagrama
    // 0 = unico protocolo permitido para escopo local

    /* armazena o nome do servidor no endereco do socket. */
    // escolhendo AF_LOCAL o nome do socket so eh valido no escopo local
    name.sun_family = AF_LOCAL; 
    // o campo sun_path especifica o nome do arquivo que vai ser usado
    strcpy (name.sun_path, socket_name);

    /* Conecta o socket. */
    // cliente inicia a conexao, servidor ja deve estar escutando
    // socket_fd -> socket criado
    // (struct sockaddr *)&name -> socket do servidor para se conectar
    // sizeof(name) -> comprimento em bytes da estrutura de endereco 
    // apontada pelo segundo argumento
    connect (socket_fd, (struct sockaddr *)&name, sizeof(name));
    // connect - cria uma conexao entre dois sockets

    /* escreve o texto na linha de comando para o socket. */
    write_text (socket_fd, message);

    close (socket_fd);

    return 0;
}