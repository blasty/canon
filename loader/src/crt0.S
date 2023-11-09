.global _start

.arm

_start:
	ldr r0, =0x12345678
	blx main
.pool
