#define _GNU_SOURCE
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

const char *writeout = "writing to stdout\n";
const char *writeerr = "writing to stderr\n";
const char *write3 = "writing to 3\n";

void perror_write(int fd, const char *str) {
    if (write(fd, str, strlen(str)) != strlen(str)) {
        char *msg;
        asprintf(&msg, "write to %d", fd);
        perror(msg);
    }
}

int main() {
    char *name = "foo.txt";
    int fd = open(name, O_RDWR | O_CREAT | O_TRUNC, S_IRUSR | S_IWUSR);
    if (fd == -1) {
        perror(name);
        exit(2);
    }
    remove("foo.txt");
    dup2(fd, 1);
    printf("printing to stdout\n");
    fflush(stdout);
    fprintf(stderr, "printing to stderr\n");
    fflush(stderr);
    // much danger in mixing buffered io and write!!!
    dup2(1,3);
    perror_write(1, writeout);
    perror_write(2, writeerr);
    perror_write(3, write3);
    fprintf(stderr, "foo.txt has:\n");
    char buffer[1024];
    lseek(fd, 0, SEEK_SET);
    int count = read(fd, buffer, sizeof buffer);
    write(2, buffer, count);
}
