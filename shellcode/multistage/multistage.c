#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/mman.h>

#define MAXCHAR 20

int main(){
  void *data;
  setvbuf(stdin, 0, 2, 0);
  setvbuf(stdout, 0, 2, 0);
  printf("   _____ __    _____ ____                __ _____ _    __ ___\n  / ___// /_  |__  // / /_________  ____/ /|__  /| |  / /|__ \\\n  \\__ \\/ __ \\  /_ </ / // ___/ __ \\/ __  /  /_ < | | / / __/ /\n ___/ / / / /___/ / / // /__/ /_/ / /_/ / ___/ / | |/ / / __/ \n/____/_/ /_//____/_/_/ \\___/\\____/\\__,_/ /____/  |___/ /____/ \n                                                             \n  ");

  data = mmap(0, 0x1000, 7, 0x22, -1, 0);
  read(0, data, MAXCHAR);
  printf("Executing you shellcode.");
  register long rax __asm__("rax") = data;
  asm("jmp %rax");

}