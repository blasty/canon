TOOLCHAIN := arm-none-eabi
CC := $(TOOLCHAIN)-gcc
OBJCOPY := $(TOOLCHAIN)-objcopy

CFLAGS := -Os -mthumb -fno-builtin -fPIC -pie -ffreestanding -fno-exceptions -march=armv7-a

all: mf743cdw_1203 mf753cdw_0304

mf743cdw_1203:
	$(CC) $(CFLAGS) -T./specs/link_mf743cdw_v12.03.ld -o build/loader_mf743cdw_v12.03.elf src/crt0.S src/main.c -nostartfiles -nodefaultlibs -static
	$(OBJCOPY) -O binary build/loader_mf743cdw_v12.03.elf build/loader_mf743cdw_v12.03.bin
	@wc -c build/loader_mf743cdw_v12.03.bin

mf753cdw_0304:
	$(CC) $(CFLAGS) -T./specs/link_mf753cdw_v03.04.ld -o build/loader_mf753cdw_v03.04.elf src/crt0.S src/main.c -nostartfiles -nodefaultlibs -static
	$(OBJCOPY) -O binary build/loader_mf753cdw_v03.04.elf build/loader_mf753cdw_v03.04.bin
	@wc -c build/loader_mf753cdw_v03.04.bin
