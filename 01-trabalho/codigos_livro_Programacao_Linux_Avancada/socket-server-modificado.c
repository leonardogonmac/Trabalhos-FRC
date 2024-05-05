// Servidor de Socket de Escopo Local
//
// para executar apos compilar
// ./socket-server /tmp/socket
// e executa socket-client em outro terminal
//
// se o processo ficar ativo e nao encerrar adequadamente
// lsof -U | grep /tmp/socket
// kill -9 <numero_processo>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>

/* Le texto de um socket e exibe-o. Continua ate que o socket feche. Retorna um valor nao nulo se o cliente envia mesnsagem de saida ("quit"), retorna zero nos outros casos. */

int server(int client_socket)
{
    while (1) {
        int length;
        char* text;

        /* Primeiro, le o comprimento da mensagem de texto a partir do socket. 
           Se read retorna zero, o cliente fecha a conexao. */
        if (read(client_socket, &length, sizeof(length)) == 0) 
            return 0;
        
        /* Aloca um espaco temporario de armazenamento para manter o texto. */
        text = (char*) malloc(length);
        //memset(text, 0, length); // Inicializa a memória alocada com zeros

        /* Le o texto propriamente dito, e mostra-o. */
        //printf("%s antes\n", text);
        //read(client_socket, text, length);
        int bytes_read = read(client_socket, text, length);
        if (bytes_read < 0) {
            perror("Erro ao ler do socket");
            free(text);
            return 0; // Ou qualquer ação apropriada
        } else if (bytes_read == 0) {
            printf("Cliente fechou a conexão\n");
            free(text);
            return 0;
        } else if (bytes_read != length) {
            printf("Quantidade de bytes lidos diferente do esperado\n");
            free(text);
            return 0;
        }
        printf("%s\n", text);
        
        /* Se o cliente enviar a mensagem "quit", terminamos tudo. */
        if (!strcmp(text, "quit")){
            free(text);
            return 1;
        }
        
        /* Libera o espaco temporario de armazenamento. */
        free(text);

   }
}

int main(int argc, char* const argv[])
{
    const char* const socket_name = argv[1];
    int socket_fd;
    struct sockaddr_un name;
    int client_sent_quit_message;

    /* Cria o socket. */
    socket_fd = socket(PF_LOCAL, SOCK_STREAM, 0);
    // PF_LOCAL = escopo do socket -> nesse caso local (poderia ser usado PF_UNIX tambem)
    // para escopo de internet -> PF_INET
    // SOCK_STREAM = estilo da comunicacao -> estilo de conexao 
    // SOCK_DGRAM -> estilo do tipo datagrama
    // 0 = unico protocolo permitido para escopo local
        if (socket_fd == -1) {
        perror("Erro ao criar socket");
        return 1;
    }
    
    /* Indica isso ao servidor. */
    // escolhendo AF_LOCAL o nome do socket so eh valido no escopo local
    name.sun_family = AF_LOCAL; 
    // o campo sun_path especifica o nome do arquivo que vai ser usado
    strcpy(name.sun_path, socket_name);
    //bind (socket_fd , &name, SUN_LEN (&name));
    //bind(socket_fd, (struct sockaddr *)&name, sizeof(name));
    // bind - rotula um socket de servidor com um endereco
    // um endereco deve ser associado ao socket do servidor usando bind se
    // for para um cliente encontra-lo.
    // socket_fd -> descritor de arquivo do socket
    // (struct sockaddr *)&name -> apontador para uma estrutura de endereco de socket
    // sizeof(name) -> comprimento da estrutura de endereco em bytes
    if (bind(socket_fd, (struct sockaddr *)&name, sizeof(name)) == -1) {
        perror("Erro ao fazer bind do socket");
        close(socket_fd);
        return 1;
    }

    /* escuta esperando por conexoes. */
    //listen(socket_fd, 5);
    // listen - configura um socket para aceitar condicoes
    //          indica que eh um servidor
    // socket_fd -> descritor de arquivo do socket
    // 5 -> quantas conexoes pendentes sao enfileiradas
    if (listen(socket_fd, 5) == -1) {
        perror("Erro ao escutar por conexões");
        close(socket_fd);
        return 1;
    }

    /* Repetidamente aceita conexoes, usando um ciclo em torno da funcao server() para 
    tratar com cada cliente. Continua ate que um cliente envia uma mensagem "quit". */
    do {
        struct sockaddr_un client_name;
        socklen_t client_name_len;
        int client_socket_fd;

        /* Aceita uma conexao. */
        // accept - aceita uma conexao e cria um novo socket para conexao
        // socket_fd -> descritor de arquivo do socket
        // (struct sockaddr *)&client_name -> apontador para uma estrutura 
        //                                    de endereco de socket do cliente
        // client_name_len -> comprimento da estrutura de endereco em bytes
        client_socket_fd = accept(socket_fd, (struct sockaddr *)&client_name, &client_name_len);
        if (client_socket_fd == -1) {
            perror("Erro ao aceitar conexão");
            close(socket_fd);
            return 1;
        }

        /* Manipula a conexao. */
        client_sent_quit_message = server(client_socket_fd);

        /* Fecha nosso fim da conexao. */
        close(client_socket_fd);

    } while (!client_sent_quit_message);

    /* Remove o arquivo de socket. */
    close(socket_fd); // destroi o socket
    unlink(socket_name);

    return 0;
}
