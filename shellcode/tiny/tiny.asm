
; mov    rax,0x3b
push   0x3b
pop    rax 



; Load "/bin/sh" into RDI (assuming you're using Linux)

; Load "sh" into the lower 32 bits of RDI
mov edi, 0x68732f2f  ; Equivalent to "sh//"

; Shift the value to the left by 16 bits to make room for "/bin"
shl rdi, 16

; Load "/bin" into the lower 16 bits of RDI
mov dil, 0x6e69      ; Equivalent to "/bin"




syscall
