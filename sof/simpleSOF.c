/*
 * 最典型的栈溢出利用，通过覆盖程序的返回地址为攻击者所控制的地址
 * gcc -m32 -fno-stack-protector simpleSOF.c -o simpleSOF
 *    -m32 指生成32位程序
 *    -fno-stack-protector 指不开启堆栈保护，即关闭canary保护
 */


#include <stdio.h>
#include <string.h>
void success() { puts("You Hava already controlled it."); }
void vulnerable() {
  char s[12];
  gets(s);
  puts(s);
  return;
}
int main(int argc, char **argv) {
  vulnerable();
  return 0;
}
