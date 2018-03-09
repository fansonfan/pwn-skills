# fd - 1pt

## 问题描述

Mommy! what is a file descriptor in Linux?

* try to play the wargame your self but if you are ABSOLUTE beginner, follow this tutorial link: https://www.youtube.com/watch?v=blAxTfcW9VU

ssh fd@pwnable.kr -p2222 (pw:guest)

## 源码分析

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
char buf[32];
int main(int argc, char* argv[], char* envp[]){
	if(argc<2){
		printf("pass argv[1] a number\n");
		return 0;
	}
	int fd = atoi( argv[1] ) - 0x1234;
	int len = 0;
	len = read(fd, buf, 32);
	if(!strcmp("LETMEWIN\n", buf)){
		printf("good job :)\n");
		system("/bin/cat flag");
		exit(0);
	}
	printf("learn about Linux file IO\n");
	return 0;

}
```

fd即文件描述符，这里取的是我们的第1个参数与0x1234之间的差值，然后用在read()函数中。
随后strcmp()函数比较buf和"LETMEWIN\n"

我们可以通过文件描述符来控制buf的读入读出。当fd=0时向buf写入，fd=1时将buf读出，fd=2时是输出到错误流中，这个就不用太在意。我们主要知道fd为1和0的情形即可

## 解题思路

控制fd的值为0x1234，也就是4660，然后输入"LETMEWIN\n"即可获得flag


## flag

mommy! I think I know what a file descriptor is!!
