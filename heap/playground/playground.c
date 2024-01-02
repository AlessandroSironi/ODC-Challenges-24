#include <inttypes.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
# include <malloc.h>

unsigned long max_heap=0;
unsigned long min_heap=0;

int main(int argc, char ** argv) {
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    fprintf(stdout, "pid: %d\n", getpid());
    fprintf(stdout, "main: %p\n", main);

    char buffer[1000];

    min_heap = (unsigned long)malloc(1) & 0xfffffffffffff000;
    max_heap = (min_heap + 0x1000) & 0xfffffffffffff000;
    while (1) {
        fprintf(stdout, "> ");
        fgets(buffer, sizeof(buffer), stdin);
        char cmd[1000];
        intptr_t arg1, arg2;
        int num = sscanf(buffer, "%s %"SCNiPTR" %"SCNiPTR, cmd, &arg1, &arg2);
        if (strcmp(cmd, "malloc") == 0) {
            void* result = malloc(arg1);
            fprintf(stdout, "==> %p\n", result);
        } else if (strcmp(cmd, "free") == 0) {
            free((void*) arg1);
            fprintf(stdout, "==> ok\n");
        } else if (strcmp(cmd, "show") == 0) {
            if (num == 2) {
                arg2 = 1;
            }
            long * src = (long*) arg1;
            for (int i = 0; i < arg2; i++) {
                fprintf(stdout, "%p: %#16.0lx\n", &src[i], src[i]);
            }
        }
        else if (strcmp(cmd, "write") == 0) {
            if (num == 2) {
                arg2 = 1;
            }
            void * src = (void*) arg1;
            if ((unsigned long)src < min_heap || (unsigned long)src >= max_heap){
                fprintf(stdout, "==> fail\n");
            }
            else{
                fprintf(stdout, "==> read\n");
                read(0, src, arg2);
                fprintf(stdout, "==> done\n");
            }

        } else {
            puts("Commands: malloc n, free p, show p [n], write p [n]");
        }
    }
}