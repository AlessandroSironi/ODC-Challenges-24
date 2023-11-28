#include <stdio.h>

int main() {
	unsigned char magic0[13] = { 0x1b, 0x51, 0x17, 0x2a, 0x1e, 0x4e, 0x3d, 0x10, 0x17, 0x46, 0x49, 0x14, 0x3d };
	unsigned char magic1[12] = { 0xeb, 0x51, 0xb0, 0x13, 0x85, 0xb9, 0x1c, 0x87, 0xb8, 0x26, 0x8d, 0x07 };
	char babuzz[6] = "babuzz";
	unsigned char var;	
	char flag[100];
	int i = 0;

	//First Stage
	for (i = 0; i < 13; i++) {
		/* c = (char)byte_array[i];
		printf("%c",c); */
		flag[i] = babuzz[i % 6] ^ magic0[i];
	}

	//Second Stage
	var = (char)-69;
	for (int j = 0; j < 12; j++) {
		i++;
		flag[i] = (char) (magic1[j] - var);
		var += flag[i];
		/* printf("%c\t", flag[i]); */
	}

	flag[i+1] = '\0';
	
	printf("flag{");
	for (int x = 0; x < 100 && flag[x] != '\0'; x++) {
		printf("%c", flag[x]);
	}
	printf("}\n");

	return 0;
}
