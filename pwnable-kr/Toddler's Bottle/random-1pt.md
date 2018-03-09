# random - 1pt

## 问题描述

Daddy, teach me how to use random value in programming!

ssh random@pwnable.kr -p2222 (pw:guest)

## 源码分析

```c
#include <stdio.h>

int main(){
	unsigned int random;
	random = rand();	// random value!

	unsigned int key=0;
	scanf("%d", &key);

	if( (key ^ random) == 0xdeadbeef ){
		printf("Good!\n");
		system("/bin/cat flag");
		return 0;
	}

	printf("Wrong, maybe you should try 2^32 cases.\n");
	return 0;
}

```

设置了一个随机数并与输入的key异或，取值是否为0xdeadbeef

## 解题思路

随机数并没有初始化，因此是固定值，可以用gdb调出来

## flag

key = 0x6b8b4567 ^ 0xdeadbeef = 3039230856

Mommy, I thought libc random is unpredictable...

