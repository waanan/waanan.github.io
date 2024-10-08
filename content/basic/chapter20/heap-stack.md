---
title: "堆和栈"
date: 2024-08-20T10:49:32+08:00
---

程序使用的内存通常分为几个不同的区域，称为段：

1. 代码段（也称为文本段），编译后的程序二进制位于内存中。代码段通常是只读的。
2. bss段（也称为未初始化的数据段），其中存储零初始化的全局变量和静态变量。
3. 数据段（也称为初始化数据段），其中存储初始化的全局变量和静态变量。
4. 堆，存储分配动态分配的变量。
5. 调用栈，其中存储函数参数、局部变量和其他函数相关信息。

在本课中，我们将主要关注堆和栈，因为这是大多数有趣的事情发生的地方。

***
## 堆段

堆段（也称为“空闲存储”）跟踪用于动态分配的内存。我们在前面课程中已经稍微讨论了堆——使用new和delete进行动态内存分配，因此这里将是一个概述。

在C++中，当使用new操作符分配内存时，该内存分配在应用程序的堆段中。

假设int为4个字节：

```C++
int* ptr { new int }; // new 在堆中分配4个字节的 int
int* array { new int[10] }; // new 在堆中分配40个字节的 int[10]
```

对应内存的地址由操作符new传回，然后可以存储在指针中。您不必担心如何定位空闲内存并将其分配给用户的过程背后的机制。然而，值得知道的是，连续内存分配请求可能不会分配连续的内存地址！

```C++
int* ptr1 { new int };
int* ptr2 { new int };
// ptr1 和 ptr2 可能在内存中并不挨着
```

删除动态分配的变量时，内存将“返回”到堆，然后可以在接收到未来的分配请求时重新分配。请记住，删除指针不会删除变量，它只是将相关地址的内存返回给操作系统。

堆有优点和缺点：

1. 在堆上分配内存相对较慢。
2. 分配的内存保持分配状态，直到它被主动释放（当心内存泄漏）或应用程序结束（此时操作系统应该清理它）。
3. 必须通过指针访问动态分配的内存。解引用指针比直接访问变量慢。
4. 因为堆是一个大的内存池，所以可以在这里分配大的数组、结构体或类。

***
## 调用栈

调用栈（通常称为“栈”）可以发挥更有趣的作用。调用栈跟踪从程序开始到当前执行点的所有活动函数（那些已被调用但尚未终止的函数），并处理所有函数参数和局部变量的分配。

调用栈被实现为栈数据结构。因此，在讨论调用栈如何工作之前，我们需要了解什么是栈数据结构。

***
## 栈数据结构

数据结构是一种用于组织数据以使其能够有效使用的编程机制。您已经看到了几种类型的数据结构，如数组和结构体。这两种数据结构都提供了以有效的方式存储数据和访问该数据的机制。有许多额外的数据结构通常用于编程，其中相当一部分是在标准库中实现的，栈就是其中之一。

考虑一下自助餐厅中的一堆盘子。因为每个盘子都很重，而且它们都堆叠在一起，所以实际上只能做三件事之一：

1. 查看最顶上的盘子
2. 从最顶上取走一个盘子（下面的盘子会漏出来）
3. 将新盘子放到最顶上（将之前的盘子都盖住）

在计算机编程中，栈是保存多个对象（很像数组）的容器数据结构。然而，数组允许您以任何顺序访问和修改元素（称为随机访问），但栈的限制比较大。可以在栈上执行的操作对应于上面提到的三件事：

1. 查看栈顶的元素（通常函数名叫top(), 但有些地方也叫peek()）
2. 取走栈顶的元素（通过叫pop()的函数）
3. 将新元素放到栈顶（通过叫push()的函数）

栈是后进先出（LIFO）结构。最后一个被推到栈上的元素将是弹出的第一个元素。如果你在栈顶部放一个新盘子，从栈中取出的第一个盘子将是你最后放上的盘子。当元素被推送到栈上时，栈会变大—，当元素被弹出时，栈就会变小。

例如，下面是一个简短的序列，展示了在栈上推入和弹出的工作原理：

```C++
Stack: empty
Push 1
Stack: 1
Push 2
Stack: 1 2
Push 3
Stack: 1 2 3
Pop
Stack: 1 2
Pop
Stack: 1
```

***
## 调用栈段

调用栈段保存用于调用栈的内存。当应用程序启动时，操作系统将main()函数push到调用栈上。然后程序开始执行。

当遇到函数调用时，该函数被推送到调用栈上。当前函数结束时，该函数将从调用栈中弹出（该过程有时称为退栈）。因此，通过查看当前调用栈，我们可以看到为到达当前执行点而调用的所有函数。

我们上面的盘子比喻类似于调用栈的工作方式。栈本身是内存中的一大块内存。盘子是内存地址，我们在栈上推入和弹出的“项目”称为栈帧。栈帧跟踪与一个函数调用关联的所有数据。稍后我们将详细讨论栈帧。“标记”是一个寄存器（CPU中的一小块内存），称为栈指针（有时缩写为“SP”）。栈指针跟踪调用栈顶部的位置。

我们可以做一个进一步的优化：当我们从调用栈中弹出一个项目时，我们只需向下移动栈指针——不必清理弹出的栈帧所使用的内存或将其归零。该内存不再被认为是“在栈上”，因此不会被访问。如果我们稍后将新的栈帧推送到相同的内存中，新的栈帧将覆盖那些未清理过的旧值。

***
## 正在运行的调用栈

让我们更详细地研究一下调用栈是如何工作的。下面是调用函数时发生的步骤序列：

1. 程序执行到一个函数调用
2. 栈帧被构造，然后推入栈中，栈帧包含如下的内容：
    1. 函数调用完成之后的指令的地址（称为返回地址）。这是CPU记忆在被调用函数退出后返回到何处的方式。
    2. 所有函数参数
    3. 所有局部变量所需的内存
    4. 由函数修改的任何寄存器保存的副本，这些寄存器需要在函数返回时恢复
3. CPU跳转到被调函数的首条指令
4. 开始执行函数中的所有指令

当函数终止时，将发生以下步骤：

1. 将保存的值恢复到寄存器
2. 栈帧从栈上推出，所有函数参数和局部变量的内存被释放
3. 处理返回值
4. CPU根据记录的返回地址，跳转到函数调用完成后的指令

根据计算机的体系结构，可以按许多不同的方式处理返回值。一些架构将返回值作为栈帧的一部分。其它则使用CPU寄存器来保存返回值。

通常，了解调用栈如何工作的所有细节并不重要。然而，理解函数在被调用时有效地推送到栈上，并在它们返回时弹出（退出），可以为您提供理解递归所需的基础知识，以及在调试时有用的一些其他概念。

技术说明：在某些架构上，调用栈从内存地址0往上增长。在其他架构下，它向内存地址向0减小。因此，新推送的栈帧可能具有比前一个帧更高或更低的内存地址。

***
## 函数调用栈帧示例

考虑以下简单应用：

```C++
int foo(int x)
{
    // b
    return x;
} // foo 从栈顶推出

int main()
{
    // a
    foo(5); // foo 在这里被推入栈中
    // c

    return 0;
}
```

在标记点处，调用栈如下所示：

```C++
a：
main()

b：
foo() (里面包含了参数 x)
main()

c：
main()
```

***
## 栈溢出

栈的大小有限，因此只能保存有限的信息量。在Visual Studio for Windows上，默认栈大小为1MB。对于Unix类的系统，使用g++/Clang时，其大小可以高达8MB。如果程序试图在栈上放置太多信息，则会导致栈溢出。当栈中的所有内存都已分配时，就会发生栈溢出——在这种情况下，进一步的分配会导致栈溢出到内存的其他部分。

栈溢出通常是在栈上分配太多变量和/或进行太多嵌套函数调用（其中函数A，调用函数B，调用函数C，调用函数D等）的结果。在现代操作系统上，栈溢出通常会导致操作系统告警访问冲突并终止程序。

下面是一个可能导致栈溢出的示例程序。您可以在系统上运行它，并观察程序崩溃：

```C++
#include <iostream>

int main()
{
    int stack[10000000];
    std::cout << "hi" << stack[0]; // 使用一下 stack[0] ，避免编译器把stack变量给优化掉

    return 0;
}
```

该程序试图在栈上分配一个巨大的（可能是40MB）数组。由于栈不够大，无法处理该数组，因此数组分配溢出到程序不允许使用的内存部分。

在Windows（Visual Studio）上，此程序生成以下结果：

```C++
HelloWorld.exe (process 15916) exited with code -1073741571.
```

-1073741571是十六进制的c0000005，这是访问冲突的Windows操作系统错误码。请注意，这里没打印“hi”，因为程序在该点之前终止。

下面是另一个程序，它由于不同的原因导致栈溢出：

```C++
#include <iostream>

int g_counter{ 0 };

void eatStack()
{
    std::cout << ++g_counter << ' ';

    // 这里使用g_counter，是为了避免编译器检测到函数是无限循环
    if (g_counter > 0)
        eatStack(); // 注意 eatStack() 又调用了自身

    // 这一行，为了避免编译器进行尾递归优化
    std::cout << "hi";
}

int main()
{
    eatStack();

    return 0;
}
```

在上面的程序中，每次调用函数eatStack()时，都会将栈帧推送到栈上。由于eatStack()调用自身（并且从不返回到调用方），因此栈最终将耗尽内存并导致溢出。

{{< alert success >}}
**注**

在作者的Windows 10计算机上运行（从Visual Studio社区版IDE中）时，在调试模式下进行4848次调用，在发布模式下进行128679次调用后，eatStack()崩溃。

{{< /alert >}}


栈有优点和缺点：

1. 在栈上分配内存相对较快。
2. 在栈上分配的内存只要在栈上，就保持在作用域中。它从栈中弹出时被销毁。
3. 在编译时，栈上分配的所有内存都是已知的。因此，可以通过变量直接访问对应内存。
4. 因为栈相对较小，所以做任何占用大量栈空间的事情通常不是一个好主意。这包括分配或复制大型数组或其他内存密集型结构。

{{< alert success >}}
**注**

可能在以后，我们讲解编译器相关的知识时，会详细探讨栈帧的具体数据结构。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter20/func-ptr/" next="/basic/chapter20/recursion/" >}}
20.0 函数指针
<--->
20.2 递归
{{< /prevnext >}}
