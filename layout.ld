OUTPUT_FORMAT("elf32-tradlittlemips")
OUTPUT_ARCH(mips)
ENTRY(_start)

SECTIONS
{
    . = 0x10000;

    .text : {
        *(.text)
    }

    . = 0x20000;

    .data : {
        *(.data)
    }

    .bss : {
        *(.bss)
    }
}
