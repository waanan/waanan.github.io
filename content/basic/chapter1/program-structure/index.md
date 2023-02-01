---
title: "程序结构介绍"
date: 2022-12-28T16:40:41+08:00
---

在C++中，最经常使用的部分就是「语句」和「函数」。

在写文章的时候，我们会将文章拆分为段落和句子。在代码的组织上，「函数」就类似于段落，「语句」就相当于句子。

***
## 语句

「语句」是C++中独立计算的最小的指令单元。大部分的语句都是以「;」结尾。对于C++而言，一个语句，编译后基本会对应多条机器指令。

常用的语句类型如下:
1. 声明语句
2. 表达式语句
3. 跳转语句
4. 复合语句
5. 选择语句
6. 迭代语句
7. 异常捕获块

下面是每种语句的简单例子，后面的学习过程中会详细讲解每种语句的用法。
```C++
// 声明语句
int n = 1;

// 表达式语句
n = n + 1;
std::cout << "n = " << n << std::endl;

// 跳转语句
mylabel:
    cout << n << ", ";
    n--;
    if (n>0) goto mylabel;

// 复合语句
{ 语句1; 语句2; 语句3; }

// 选择语句
if (x == 100) cout << "x is 100";

// 迭代语句
while (n>0) {
    cout << n << ", ";
    --n;
}

// 异常捕获块
try
{
    throw 20;
}
catch (int e)
{
    cout << "An exception occurred. Exception Nr. " << e << '\n';
}
```

***
## 函数及main函数

「函数」将一系列的「语句」打包到一起并且按顺序去执行这些语句。
通过使用函数，可以使用函数名


{{< alert success >}}
**main函数**


{{< /alert >}}

***
## HelloWorld程序的拆解
```C++
#include <iostream>

int main()
{
    std::cout << "Hello World!" << std::endl;
    return 0;
}
```

***
## 语法错误

{{< img src="./syntax_err.png" title="语法错误">}}

***

{{< prevnext prev="/basic/chapter0/write-first-program/" next="/basic/chapter1/comment/" >}}
第一个C++程序
<--->
注释
{{< /prevnext >}}