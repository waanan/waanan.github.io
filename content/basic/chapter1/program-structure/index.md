---
title: "程序结构介绍"
date: 2022-12-28T16:40:41+08:00
---

C++中，最经常使用的是「语句」和「函数」。

写文章时，会将文章拆分成段落和句子。代码组织上，「函数」类似于段落，「语句」相当于句子。

***
## 语句

「语句」是C++中独立计算最小的指令单元。大部分语句以「;」结尾。对于C++，一个语句，编译后对应多条机器指令。

常用的语句类型如下:
1. 声明语句
2. 表达式语句
3. 跳转语句
4. 复合语句
5. 选择语句
6. 迭代语句
7. 异常捕获块

下面是每种语句的简单例子，后面学习中会讲解语句用法。
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

「函数」将一系列「语句」打包在一起。执行时，按顺序执行语句。
使用函数，指代一系列语句。创建函数，相当于创建新指令。

{{< alert success >}}
**main函数**

每个C++程序都有一个main函数。程序启动时，顺序执行main函数中语句，直到程序结束。
{{< /alert >}}

编写函数是为了特定工作，例如如下「max」函数，求两数中最大数。

```C++
int max(int a, int b)
{
    if (a > b)
    {
        return a;
    }
    return b;
}
```

使用函数有如下好处：
1. 减少重复代码
2. 提高程序可读性
3. 降低程序的维护成本

{{< alert secondary >}}
**注**

在后续，使用「函数名」+「()」指代函数。例如，main()或doSomething(),而不是函数main或函数doSomething。
{{< /alert >}}


***
## Hello World程序的拆解

有了语句和函数，拆解下「Hello World」程序。

```C++
#include <iostream>

int main()
{
    std::cout << "Hello World!" << std::endl;
    return 0;
}
```

第一行是「预处理」指令。说明要使用「iostream」库。iostream是C++提供的用来读写命令行的标准库。
第五行std::cout与std::endl即是iostream库中功能。
如果没有本行，编译器会报错，无法找到std::cout与std::endl的定义。

第二行是空行，不会被编译。程序中使用空行将不同部分隔，增加程序可读性。

第三行告诉编译器，定义main函数。

第四行与第七行，标示main函数的开始与结束。

第五行是main函数的第一条语句。std::cout代表字符串输出。
「<<」表示将右边内容，发送给左边对象，在这里表示输出到命令行中。
std::endl表示换行。

第六行是返回语句。程序执行完成后，该语句告诉操作系统程序执行成功。
大部分操作系统，返回「0」代表程序执行成功。

***
## 语法错误

文本组成语句，函数及程序的规则，称作程序的「语法」。如同写作文时，每句话要「。」来结尾。

只有符合C++语法的文本，才能被C++编译器成功编译，否则编译器会报错，这类错误称为「语法错误」。

```C++
#include <iostream>

int main()
{
    int a;
    int b;
    std::cout << "Hello World!" << std::endl;
    return 0
}
```

上面程序中，第8行结尾，少写了「；」。编译器给出如下提示：

{{< img src="./syntax_err.png" title="语法错误">}}

第9行的「}」之前少了「;」。语法错误是编程时常见的错误。编译器会明确告知错误位置，容易修改。

尝试删除程序中任意地方，看编译器分别给出什么样的报错。

***

{{< prevnext prev="/basic/chapter0/write-first-program/" next="/basic/chapter1/comment/" >}}
0.5 第一个C++程序
<--->
1.1 注释
{{< /prevnext >}}
