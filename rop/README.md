# ROP

## 通用gadgets part1

\__libc_csu_init里gadgets可以控制三个参数

```assembly
00000000004005a0 <__libc_csu_init>:
  4005a0:   48 89 6c 24 d8          mov    %rbp,-0x28(%rsp)
  4005a5:   4c 89 64 24 e0          mov    %r12,-0x20(%rsp)
  4005aa:   48 8d 2d 73 08 20 00    lea    0x200873(%rip),%rbp        # 600e24 <__init_array_end>
  4005b1:   4c 8d 25 6c 08 20 00    lea    0x20086c(%rip),%r12        # 600e24 <__init_array_end>
  4005b8:   4c 89 6c 24 e8          mov    %r13,-0x18(%rsp)
  4005bd:   4c 89 74 24 f0          mov    %r14,-0x10(%rsp)
  4005c2:   4c 89 7c 24 f8          mov    %r15,-0x8(%rsp)
  4005c7:   48 89 5c 24 d0          mov    %rbx,-0x30(%rsp)
  4005cc:   48 83 ec 38             sub    $0x38,%rsp
  4005d0:   4c 29 e5                sub    %r12,%rbp
  4005d3:   41 89 fd                mov    %edi,%r13d
  4005d6:   49 89 f6                mov    %rsi,%r14
  4005d9:   48 c1 fd 03             sar    $0x3,%rbp
  4005dd:   49 89 d7                mov    %rdx,%r15
  4005e0:   e8 1b fe ff ff          callq  400400 <_init>
  4005e5:   48 85 ed                test   %rbp,%rbp
  4005e8:   74 1c                   je     400606 <__libc_csu_init+0x66>
  4005ea:   31 db                   xor    %ebx,%ebx
  4005ec:   0f 1f 40 00             nopl   0x0(%rax)
  4005f0:   4c 89 fa                mov    %r15,%rdx
  4005f3:   4c 89 f6                mov    %r14,%rsi
  4005f6:   44 89 ef                mov    %r13d,%edi
  4005f9:   41 ff 14 dc             callq  *(%r12,%rbx,8)
  4005fd:   48 83 c3 01             add    $0x1,%rbx
  400601:   48 39 eb                cmp    %rbp,%rbx
  400604:   75 ea                   jne    4005f0 <__libc_csu_init+0x50>
  400606:   48 8b 5c 24 08          mov    0x8(%rsp),%rbx
  40060b:   48 8b 6c 24 10          mov    0x10(%rsp),%rbp
  400610:   4c 8b 64 24 18          mov    0x18(%rsp),%r12
  400615:   4c 8b 6c 24 20          mov    0x20(%rsp),%r13
  40061a:   4c 8b 74 24 28          mov    0x28(%rsp),%r14
  40061f:   4c 8b 7c 24 30          mov    0x30(%rsp),%r15
  400624:   48 83 c4 38             add    $0x38,%rsp
  400628:   c3                      retq   
```
在`400606`处我们可以控制`rbx` `rbp` `r12` `r13` `r14` `r15`的值，然后在`4005f0`有`rdx = r15` `rsi = r14` `edi = r13`，随后调用`call qword ptr [r12+rbx*8]`。这时我们只要再将`rbx`的值赋为`0`，再通过精心构造栈上的数据，就可以控制pc去调用我们想要调用的函数了。

执行完`call qword ptr [r12+rbx*8]`后，`rbx += 1`，之后比较`rbp`和`rbx`的值。因为先前我们设置`rbx = 0`，因此这里我们只需要将rbp设置为`1`即可

## 通用gadgets part2

通过修改pc的偏移我们可以更有效地控制寄存器内容。比如下面获得了`esi`和`edi`的控制
```assembly
gdb-peda$ x/5i 0x000000000040061a
   0x40061a <__libc_csu_init+122>:  mov    r14,QWORD PTR [rsp+0x28]
   0x40061f <__libc_csu_init+127>:  mov    r15,QWORD PTR [rsp+0x30]
   0x400624 <__libc_csu_init+132>:  add    rsp,0x38
   0x400628 <__libc_csu_init+136>:  ret  
```
修改偏移得到

```assembly
gdb-peda$ x/5i 0x000000000040061b
   0x40061b <__libc_csu_init+123>:  movesi,DWORD PTR [rsp+0x28]
   0x40061f <__libc_csu_init+127>:  mov    r15,QWORD PTR [rsp+0x30]
   0x400624 <__libc_csu_init+132>:  add    rsp,0x38
   0x400628 <__libc_csu_init+136>:  ret    
   0x400629:    nop    DWORD PTR [rax+0x0]
gdb-peda$ x/5i 0x0000000000400620
   0x400620 <__libc_csu_init+128>:  movedi,DWORD PTR [rsp+0x30]
   0x400624 <__libc_csu_init+132>:  add    rsp,0x38
   0x400628 <__libc_csu_init+136>:  ret    
   0x400629:    nop    DWORD PTR [rax+0x0]
   0x400630 <__libc_csu_fini>:  repz ret
```

如果想要控制超过三个参数的寄存器，我们可以使用_dl_runtime_resolve()里的gadgets，通过该gadgets可以控制六个寄存器的值

```assembly
0x7ffff7def200 <_dl_runtime_resolve>:   sub    rsp,0x38
0x7ffff7def204 <_dl_runtime_resolve+4>: mov    QWORD PTR [rsp],rax
0x7ffff7def208 <_dl_runtime_resolve+8>: mov    QWORD PTR [rsp+0x8],rcx
0x7ffff7def20d <_dl_runtime_resolve+13>:    mov    QWORD PTR [rsp+0x10],rdx
0x7ffff7def212 <_dl_runtime_resolve+18>:    mov    QWORD PTR [rsp+0x18],rsi
0x7ffff7def217 <_dl_runtime_resolve+23>:    mov    QWORD PTR [rsp+0x20],rdi
0x7ffff7def21c <_dl_runtime_resolve+28>:    mov    QWORD PTR [rsp+0x28],r8
0x7ffff7def221 <_dl_runtime_resolve+33>:    mov    QWORD PTR [rsp+0x30],r9
0x7ffff7def226 <_dl_runtime_resolve+38>:    movrsi,QWORD PTR [rsp+0x40]
0x7ffff7def22b <_dl_runtime_resolve+43>:    movrdi,QWORD PTR [rsp+0x38]
0x7ffff7def230 <_dl_runtime_resolve+48>:    call   0x7ffff7de8680 <_dl_fixup>
0x7ffff7def235 <_dl_runtime_resolve+53>:    mov    r11,rax
0x7ffff7def238 <_dl_runtime_resolve+56>:    mov    r9,QWORD PTR [rsp+0x30]
0x7ffff7def23d <_dl_runtime_resolve+61>:    mov    r8,QWORD PTR [rsp+0x28]
0x7ffff7def242 <_dl_runtime_resolve+66>:    movrdi,QWORD PTR [rsp+0x20]
0x7ffff7def247 <_dl_runtime_resolve+71>:    movrsi,QWORD PTR [rsp+0x18]
0x7ffff7def24c <_dl_runtime_resolve+76>:    movrdx,QWORD PTR [rsp+0x10]
0x7ffff7def251 <_dl_runtime_resolve+81>:    movrcx,QWORD PTR [rsp+0x8]
0x7ffff7def256 <_dl_runtime_resolve+86>:    movrax,QWORD PTR [rsp]
0x7ffff7def25a <_dl_runtime_resolve+90>:    add    rsp,0x48
0x7ffff7def25e <_dl_runtime_resolve+94>:    jmp    r11
```
从`0x7ffff7def235`开始，就是这个通用gadget的地址了。通过这个gadget我们可以控制rdi，rsi，rdx，rcx， r8，r9的值。但要注意的是`_dl_runtime_resolve()`在内存中的地址是随机的。所以我们需要先用information leak得到`_dl_runtime_resolve()`在内存中的地址。那么`_dl_runtime_resolve()`的地址被保存在了哪个固定的地址呢？

通过反编译level5程序我们可以看到write@plt()这个函数使用PLT [0] 去查找write函数在内存中的地址，函数jump过去的地址*0x600ff8其实就是`_dl_runtime_resolve()`在内存中的地址了。所以只要获取到0x600ff8这个地址保存的数据，就能够找到`_dl_runtime_resolve()`在内存中的地址

另一个要注意的是，想要利用这个gadget，我们还需要控制rax的值，因为gadget是通过rax跳转的：

```assembly
0x7ffff7def235 <_dl_runtime_resolve+53>:    mov    r11,rax
……
0x7ffff7def25e <_dl_runtime_resolve+94>:    jmp    r11
```

所以我们接下来用ROPgadget查找一下libc.so中控制rax的gadget：

```assembly
ROPgadget --binary libc.so.6 --only "pop|ret" | grep "rax"
0x000000000001f076 : pop rax ; pop rbx ; pop rbp ; ret
0x0000000000023950 : pop rax ; ret
0x000000000019176e : pop rax ; ret 0xffed
0x0000000000123504 : pop rax ; ret 0xfff0
```

`0x0000000000023950`刚好符合我们的要求。有了`pop rax`和`_dl_runtime_resolve`这两个gadgets，我们就可以很轻松的调用想要的调用的函数了。
