#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct entry {
    char *str;
    struct entry *next;
};

void push(struct entry **head, char *str) {
    struct entry *ne = malloc(sizeof *ne);
    ne->str = str;
    ne->next = *head;
    *head = ne;
}

char *pop(struct entry **head) {
    if (*head == NULL) return NULL;
    char *rc = (*head)->str;
    struct entry *nh = (*head)->next;
    free(*head);
    *head = nh;
    return rc;
}

void main() {
    char *line = NULL;
    size_t n = 0;
    struct entry *head = NULL;
    while (getline(&line, &n, stdin) > 0) {
        line[strlen(line)-1] = '\0'; // quick and dirty \n strip
        push(&head, line);
        line = NULL;
        n = 0;
    }
    struct entry *ptr = head;
    while (ptr) {
        printf("%s\n", ptr->str);
        ptr = ptr->next;
    }
}
