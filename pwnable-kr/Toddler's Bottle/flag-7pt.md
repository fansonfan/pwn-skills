# flag - 7pt

## 问题描述


Papa brought me a packed present! let's open it.

Download : http://pwnable.kr/bin/flag

This is reversing task. all you need is binary

## 解题思路


这次是逆向题, 文件是一个64位程序, 无法使用odjdump反编译或使用gdb调试. 因此使用ida x64打开. 发现里面并没有可读代码, 显然是加壳了. 于是尝试使用strings搜索程序中一些字符串, 发现以下:

```bash
$Info: This file is packed with the UPX executable packer http://upx.sf.net $
```

可知程序是经过UPX压缩了. 在Linux下使用upx解压缩即可. 之后查找关键代码, 找到flag字符串即可


## flag
UPX...? sounds like a delivery service :)



