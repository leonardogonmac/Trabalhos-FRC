// Le de um servidor www
/* Esse programa recebe o nome do computador conectado a rede do servidor Web na linha de comando (não uma URL - isto é, recebe a informação sem o “http://”). O programa chama a funcao gethostbyname para traduzir o nome do computador conectado a rede em um endereço IP numerico e entao conectar um fluxo (TCP) socket na porta 80 daquele computador conectado a rede. Servidores Web falam o Protocolo de Transporte de Hipertexto (HTTP), de forma que o programa emita o comando HTTP GET e o servidor responda enviando o texto da página inicial. */
// ./socket-inet unb.br

#include <stdlib.h>
#include <stdio.h>
#include <netinet/in.h>
#include <netdb.h>
#include <sys/socket.h>
#include <unistd.h>
#include <string.h>

/* Imprime o conteudo da home page para o socket do servidor.
   Retorna uma indicacao de sucesso. */

void get_home_page (int socket_fd) {
    char buffer[10000];
    ssize_t number_characters_read;

    /* Envia o comando HTTP GET para a home page. 
       Esse comando envia uma mensagem atraves do socket para o servidor web, o qual
       responde enviando o codigo fonte ma linguagem html da pagina inicial, fechando
       a conexao em seguida*/
    sprintf (buffer, "GET /\n");
    write (socket_fd, buffer, strlen (buffer));

    /* Le a partir do socket. read pode nao receber todos os dados de uma
       so vez, entao continua tentando ate que esgotemos os dados a serem lidos. */

    while (1) {
        number_characters_read = read (socket_fd, buffer, 10000);
        if (number_characters_read == 0)
            return;

        /* Escreve os dados para a saida padrao. */
        fwrite (buffer, sizeof (char), number_characters_read, stdout);
    }
}

int main (int argc, char* const argv[]) {
    int socket_fd;
    struct sockaddr_in name; // armazena as duas partes de um endereco de socket
                             // localizado na internet: uma maquina e um numero de porta
    struct hostent* hostinfo;

    /* Cria o socket. */
    socket_fd = socket (PF_INET, SOCK_STREAM, 0);
    // PF_INET = escopo do socket -> nesse caso de dominio Internet
    // para escopo local -> PF_LOCAL ou PF_UNIX
    // SOCK_STREAM = estilo da comunicacao -> estilo de conexao 
    // SOCK_DGRAM -> estilo do tipo datagrama
    // 0 = protocolo 

    /* Armazena o nome do servidor no endereco do socket. */
    name.sin_family = AF_INET;
    
    /* Converte de sequencia de caracteres para numeros. */
    hostinfo = gethostbyname (argv[1]);
    // gethostbyname -> retorna um apontador para a estrutura struct hostinfo
    if (hostinfo == NULL) {
        perror("gethostbyname");
        return 1;
    }
    else
        //name.sin_addr = *((struct in_addr *) hostinfo->h_addr_list); 
        memcpy(&name.sin_addr, hostinfo->h_addr_list[0], sizeof(struct in_addr));
        // sin_addr: armazena endereco internet da maquina desejada (IP inteiro de 32-bit)
        // h_addr_list contem o numero IP do computador conectado a rede

    /* Sevidor web usa a porta 80. */
    name.sin_port = htons (80);
    // htons -> converte o numero da porta para ordem de byte de rede

    /* Conecta-se ao servidor web */
    if (connect (socket_fd, (struct sockaddr *)&name, sizeof (struct sockaddr_in)) == -1) {
        perror ("connect");
        return 1;
    }

    /* Requisita a home page do servidor. */
    get_home_page (socket_fd);

    return 0;
}