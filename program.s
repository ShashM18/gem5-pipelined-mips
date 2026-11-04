
.text
.globl _start

_start:
    la $t0, array
    li $t1, 100

loop:
    sw $t1, 0($t0)
    lw $t2, 0($t0)

    addi $t0, $t0, 4
    addi $t1, $t1, -1

    bne $t1, $zero, loop
    nop

    li $v0, 4001
    li $a0, 0
    syscall

.data
.align 2

array:
    .space 400

