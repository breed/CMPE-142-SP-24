#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <string.h>

int main(int argc, char **argv) {
    int fd = open(argv[1], O_RDWR);
    if (fd == -1) {
        perror(argv[1]);
        exit(2);
    }
    char *file = mmap(NULL, 64*1024, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);

    char *ptr = NULL;
    size_t n = 0;
    while (getline(&ptr, &n, stdin) > 0) {
        printf("%s", file);
        fflush(stdout);
    }
}
