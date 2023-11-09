/* down & dirty ld script */
ENTRY(_start)

SECTIONS
{
    UART_Print = 0x414fc260;
    netSocket = 0x4165D58C;
	netConnect = 0x4164D014;
    netClose = 0x4164CC48;
	netRead = 0x4164C910;
    netWrite = 0x4164C9BC;
	UART_Print_u32 = 0x414fc260;
	flush_icache = 0x416971a8;
	flush_dcache = 0x4169713c;
	taskSleep = 0x416f60dc;
	calloc = 0x426f5bac;

	. = 0;

	.text :
	{
		*(.text)
		. = ALIGN(4);
	}

	.got :
	{
		*(.got)
		. = ALIGN(4);
	}

	.got.plt :
	{
		*(.got.plt)
		. = ALIGN(4);
	}

	.rodata :
	{
		*(.rodata)
		. = ALIGN(4);
	}

	.data :
	{
		*(.data)
		. = ALIGN(4);
	}

	.bss :
	{
		*(COMMON)
		*(.bss)
		. = ALIGN(4);
	}

	/DISCARD/ : {
		*(.eh_frame);
		*(.comment);
		*(.note.gnu.build-id);
	}
}
