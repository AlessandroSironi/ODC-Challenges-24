#include <stdio.h>
#include <stdint.h>

int main(void) {
    //uint64_t DAT_00104020[] = {0x74, 0x1a, 0x65, 0x34, 0x00, 0x00, 0x00, 0x00};
    char *segments_hex[] = {"726cfc2d", "26c6defe", "db065621", "99f5c7d0", "da4f4930"};
    uint64_t license, local_50, local_48, local_40, local_38, local_30, local_28, local_20, local_18, local_70, serial;
    int j, loop, loop2;

    local_70 = 0;
    printf("\nSerial code: ");
    for (j = 0; j < 5; j = j + 1) {
        license = segments_hex[j];
        printf("%04llx-", license);
        printf("\n");

        local_50 = license;
        for (loop = 1; loop < 8; loop = loop + 1) {
            local_48 = 1;
            for (loop2 = 0; loop2 < loop; loop2 = loop2 + 1) {
                local_40 = local_48;
                local_38 = license;
                local_30 = 0;
                while ((local_38 != 0 && (local_40 != 0))) {
                    if ((local_38 & 1) != 0) {
                        local_30 = local_30 ^ local_40;
                    }
                    local_40 = local_40 << 1;
                    if ((local_40 & 0x100000000) != 0) {
                        local_40 = local_40 ^ 0x10000008d;
                    }
                    local_38 = local_38 >> 1;
                }
                local_48 = local_30;
            }
            local_28 = license[loop % (sizeof(license) / sizeof(uint64_t))];
            local_20 = local_48;
            local_18 = 0;
            while ((local_20 != 0 && (local_28 != 0))) {
                if ((local_20 & 1) != 0) {
                    local_18 = local_18 ^ local_28;
                }
                local_28 = local_28 << 1;
                if ((local_28 & 0x100000000) != 0) {
                    local_28 = local_28 ^ 0x10000008d;
                }
                local_20 = local_20 >> 1;
            }
            local_50 = local_50 ^ local_18;
        }
        local_70 = local_50 ^ local_70;
        if (j != 4) {
            printf("%04llx-", local_70);
        }
        serial = local_70;
    }
    printf("%04llx\n", serial);
    return 0;
}

/*     for (loop = 1; loop < 8; loop = loop + 1) {
      local_48 = 1;
      for (loop2 = 0; loop2 < loop; loop2 = loop2 + 1) {
        local_40 = local_48;
        local_38 = license;
        local_30 = 0;
        while ((local_38 != 0 && (local_40 != 0))) {
          if ((local_38 & 1) != 0) {
            local_30 = local_30 ^ local_40;
          }
          local_40 = local_40 << 1;
          if ((local_40 & 0x100000000) != 0) {
            local_40 = local_40 ^ 0x10000008d;
          }
          local_38 = local_38 >> 1;
        }
        local_48 = local_30;
      }
      local_28 = (&DAT_00104020)[loop];
      local_20 = local_48;
      local_18 = 0;
      while ((local_20 != 0 && (local_28 != 0))) {
        if ((local_20 & 1) != 0) {
          local_18 = local_18 ^ local_28;
        }
        local_28 = local_28 << 1;
        if ((local_28 & 0x100000000) != 0) {
          local_28 = local_28 ^ 0x10000008d;
        }
        local_20 = local_20 >> 1;
      }
      local_50 = local_50 ^ local_18;
    }
    local_70 = local_50 ^ local_70;
    if (j != 4) {
      printf("%04llx-",local_70);
    }
    serial = local_70;
  }
  printf("%04llx\n",serial);
  return 0; */