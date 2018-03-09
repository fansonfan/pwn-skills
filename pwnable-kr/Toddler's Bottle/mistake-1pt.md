# mistake - 1pt

## 问题描述

We all make mistakes, let's move on.
(don't take this too seriously, no fancy hacking skill is required at all)

This task is based on real event
Thanks to dhmonkey

hint : operator priority

ssh mistake@pwnable.kr -p2222 (pw:guest)

## 源码分析

```c
#include <stdio.h>
#include <fcntl.h>

#define PW_LEN 10
#define XORKEY 1

void xor(char* s, int len){
	int i;
	for(i=0; i<len; i++){
		s[i] ^= XORKEY;
	}
}

int main(int argc, char* argv[]){
	
	int fd;
	if(fd=open("/home/mistake/password",O_RDONLY,0400) < 0){
		printf("can't open password %d\n", fd);
		return 0;
	}

	printf("do not bruteforce...\n");
	sleep(time(0)%20);

	char pw_buf[PW_LEN+1];
	int len;
	if(!(len=read(fd,pw_buf,PW_LEN) > 0)){
		printf("read error\n");
		close(fd);
		return 0;		
	}

	char pw_buf2[PW_LEN+1];
	printf("input password : ");
	scanf("%10s", pw_buf2);

	// xor your input
	xor(pw_buf2, 10);

	if(!strncmp(pw_buf, pw_buf2, PW_LEN)){
		printf("Password OK\n");
		system("/bin/cat flag\n");
	}
	else{
		printf("Wrong Password\n");
	}

	close(fd);
	return 0;
}
```

程序会打开password文件，将其读入到pw_buf中，然后取用户输入读入到pw_buf2中，再将pw_buf2进行异或，最后再进行比对

## 解题思路

在if判读条件中
```c
fd=open("/home/mistake/password",O_RDONLY,0400) < 0
```
“=”的优先级低于“<”，因此fd恒为0，那么就会造成说两次用户输入，第一次输入到pw_buf中，第二次输入到pw_buf2中，因此我们只需要构造两个输入，满足两个输入逐位之间异或值为1即可

```bash
mistake@ubuntu:~$ ./mistake 
do not bruteforce...
0000000000
input password : 1111111111
Password OK
Mommy, the operator priority always confuses me :(
mistake@ubuntu:~$ 
```

## flag

Mommy, the operator priority always confuses me :(

