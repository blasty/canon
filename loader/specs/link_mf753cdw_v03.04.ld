/* down & dirty ld script */
ENTRY(_start)

SECTIONS
{
    netSocket = 0x411FA12C;
	netConnect = 0x411A27F8;
    netClose = 0x411A242C;
	netRead = 0x411A20F4;
    netWrite = 0x411A21A0;
	calloc = 0x42A90F04;
    flush_icache = 0x412372CC;
    flush_dcache = 0x41237260;
    taskSleep = 0x412DC8FC;

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
