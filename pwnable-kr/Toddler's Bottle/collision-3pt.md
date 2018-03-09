# collision - 3pt

## 问题描述

Daddy told me about cool MD5 hash collision today.
I wanna do something like that too!

ssh col@pwnable.kr -p2222 (pw:guest)

## 源码分析

```c
#include <stdio.h>
#include <string.h>
unsigned long hashcode = 0x21DD09EC;
unsigned long check_password(const char* p){
	int* ip = (int*)p;
	int i;
	int res=0;
	for(i=0; i<5; i++){
		res += ip[i];
	}
	return res;
}

int main(int argc, char* argv[]){
	if(argc<2){
		printf("usage : %s [passcode]\n", argv[0]);
		return 0;
	}
	if(strlen(argv[1]) != 20){
		printf("passcode length should be 20 bytes\n");
		return 0;
	}

	if(hashcode == check_password( argv[1] )){
		system("/bin/cat flag");
		return 0;
	}
	else
		printf("wrong passcode.\n");
	return 0;
}
```
这里要求参数长度为20且check_password()中的参数是char*，转换为int*时需要4个一组。因此我们只需要构造passcode使得结果等于0x21DD09EC即可


## 解题思路

0x1dd905e8 = 0x21DD09EC - 0x01010101 * 4

./col `python -c "print '\x01' * 16 + '\xE8\x05\xD9\x1D' "`

## flag

daddy! I just managed to create a hash collision :)

