#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <stdio.h>


int main(){
  setvbuf(stdin, 0, 2, 0);
  setvbuf(stdout, 0, 2, 0);
  printf("  ________.__                         ________   ___.            __                 \n /  _____/|__| _____   _____   ____   \\_____  \\  \\_ |__ ___.__._/  |_  ____   ______\n/   \\  ___|  |/     \\ /     \\_/ __ \\    _(__  <   | __ <   |  |\\   __\\/ __ \\ /  ___/\n\\    \\_\\  \\  |  Y Y  \\  Y Y  \\  ___/   /       \\  | \\_\\ \\___  | |  | \\  ___/ \\___ \\ \n \\______  /__|__|_|  /__|_|  /\\___  > /______  /  |___  / ____| |__|  \\___  >____  >\n        \\/         \\/      \\/     \\/         \\/       \\/\\/                \\/     \\/ \n>");
  char* array = mmap(0, 0x1000, 7, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
  int i;
  int temp;
  float ftemp;

  read(0, array, 0x3);
  // write(1, "here we go\\n", 11);
  (*(void(*)())array)();

}