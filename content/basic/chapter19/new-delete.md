---
title: "使用new和delete进行动态分配内存"
date: 2024-08-19T20:25:40+08:00
---

***
## 为什么需要动态内存分配？

C++支持三种基本类型的内存分配，您已经看到了其中的两种。

1. 静态内存分配用于静态和全局变量。这些类型的变量的内存在程序运行时分配一次，并在程序的整个生命周期中保持不变。
2. 自动内存分配用于函数参数和局部变量。这些类型的变量的内存在进入相关块时分配，在退出块时释放。
3. 动态内存分配，这是本文的主题。

静态分配和自动分配都有两个共同点:

1. 在编译时必须知道变量/数组的大小。
2. 内存分配和释放自动发生（当变量被实例化/销毁时）。

大多数时候，这都很好。然而，您会遇到这些约束中的一个或两个无法满足的情况，通常是在处理外部（用户或文件）输入时。

例如，我们可能希望使用字符串来保存某人的姓名，但在他们输入姓名之前，我们不知道他们的姓名有多长。或者，我们可能想从磁盘中读入许多记录，但我们不预先知道有多少记录。或者我们可能正在创建一个游戏，让数量可变的怪物（随着时间的推移，随着一些怪物死亡和新怪物的产生而变化）试图杀死玩家。

如果我们必须在编译时声明所有内容的大小，我们所能做的最好的事情就是尝试猜测我们将需要的变量的最大大小，并希望这就足够了:

```C++
char name[25]; // 假设名字只有25个字节
Record record[500]; // 假设不会有超过50条记录
Monster monster[40]; // 假设只有40个怪物最多
Polygon rendering[30000]; // 假设3d渲染时最多只有30000个多边形
```

这是一个糟糕的解决方案，至少有四个原因:

首先，如果变量没有实际使用，就会导致内存浪费。例如，如果我们为每个名称分配25个字符，但名称平均只有12个字符长，那么我们使用的是实际需要的两倍多。或者考虑上面的渲染数组:如果渲染仅使用10000个多边形，则有20000个多边形的内存未被使用！

第二，我们如何知道实际使用了哪些内存？对于字符串，这很容易:以\0开头的字符串显然没有被使用。但怪物呢？第24个位置的怪物现在是活着还是死了？它甚至一开始就被初始化了吗？这就需要有某种方法来告诉每个怪物的状态，这增加了复杂性，并可能会占用额外的内存。

第三，大多数正常变量（包括固定数组）分配在称为栈的内存部分中。程序的栈内存量通常相当小——VisualStudio默认堆栈大小为1MB。如果超过这个数字，将导致栈溢出，操作系统可能会关闭该程序。

在Visual Studio上，你可以尝试写这样的程序看看会发生什么:

```C++
int main()
{
    int array[1000000]; // 分配100万个证书 (大概 4MB 内存)
}
```

对于许多程序来说，仅限于1MB的内存是有问题的，特别是那些处理图形的程序。

第四，也是最重要的，它可能导致人为限制或数组溢出。当用户试图从磁盘读取600条记录，但我们只为最多500条记录分配了内存时，会发生什么情况？要么我们必须给用户一个错误，只读取500条记录，要么（在最坏的情况下，我们根本不处理这种情况）溢出记录数组，并会有一些不好的事情发生。

幸运的是，这些问题很容易通过动态内存分配来解决。动态内存分配是在需要时从操作系统请求内存的一种方法。这个内存不是来自程序的有限栈内存——相反，它是从操作系统管理的更大的内存池（称为堆）中分配的。在现代机器上，堆的大小可以是GB单位。

***
## 动态分配单个变量

要动态分配单个变量，我们使用new运算符:

```C++
new int; // 动态分配一个整型（返回结果这里丢弃了）
```

在上面的例子中，我们从操作系统请求一个整数的内存。new操作符使用该内存创建对象，然后返回一个指针，该指针包含已分配的内存的地址。

通常，我们将返回值分配给指针变量，以便稍后访问分配的内存。

```C++
int* ptr{ new int }; // 动态分配一个整型，并将结果保存在指针中，以便稍后使用
```

然后，我们可以解指针以访问内存:

```C++
*ptr = 7; // 为申请的内存赋值 7
```

现在应该至少有一种情况下指针是有用的。如果没有一个指针来保存刚刚分配的内存的地址，我们将无法访问刚刚分配的内存！

请注意，访问堆分配的对象通常比访问栈分配的对象慢。因为编译器知道栈上分配对象的地址，所以它可以直接转到该地址来获取值。堆分配的对象通常通过指针访问。这需要两个步骤:一个是获取对象的地址（从指针），另一个是获得值。

***
## 动态内存分配是如何工作的？

您的计算机具有可供应用程序使用的内存（可能很多）。运行应用程序时，操作系统会将应用程序加载到该内存的某些部分中。应用程序使用的内存被划分为不同的区域，每个区域都有不同的用途。一个区域包含您的代码。另一个区域用于程序执行状态记录（跟踪调用了哪些函数，创建和销毁全局和局部变量等…）。我们稍后将详细讨论这些。当然，许多可用的内存就在那里，等待分配给请求它的程序。

当动态分配内存时，您要求操作系统分配一些内存供程序使用。如果它可以满足这个请求，它将把该内存的地址返回给您的应用程序。从那时起，应用程序可以根据需要使用该内存。当应用程序使用内存完成时，它可以将内存返回到操作系统，以提供给另一个程序。

与静态或自动内存不同，程序本身负责请求和处理动态分配的内存。

{{< alert success >}}
**关键点**

栈上对象的分配和释放是自动完成的。我们没有必要处理内存地址——编译器编写的代码可以为我们做到这一点。

堆上对象的分配和释放不会自动完成。我们需要参与。这意味着我们需要某种明确的方法来引用特定的堆分配对象，以便可以使用或后续销毁它。我们引用这些对象的方式是通过内存地址。

当我们使用操作符new时，它返回一个指针，其中包含新分配对象的内存地址。我们通常希望将其存储在指针中，以便以后可以使用该地址访问对象（并最终请求销毁它）。

{{< /alert >}}

***
## 初始化动态分配的变量

动态分配变量时，还可以通过直接初始化或统一初始化对其进行初始化:

```C++
int* ptr1{ new int (5) }; // 使用直接初始化
int* ptr2{ new int { 6 } }; // 使用统一初始化
```

***
## 销毁单个变量

当我们处理完动态分配的变量时，我们需要显式地告诉C++释放内存以供重用。对于单个变量，这是通过delete运算符完成的:

```C++
// 假设 ptr 之前是通过new分配出来的
delete ptr; // 将ptr指向的地址归还给操作系统
ptr = nullptr; // ptr赋值为nullptr
```

***
## delete内存意味着什么？

delete操作符实际上并不删除任何内容。它只是将所指向的内存返回到操作系统。然后，操作系统可以将该内存重新分配给另一个应用程序（或稍后再次分配给该本应用程序）。

尽管看起来我们正在删除一个变量，但情况并非如此！指针变量仍然具有与以前相同的作用域，并且可以像任何其他变量一样分配新的值。

请注意，删除不指向动态分配的内存的指针可能会导致糟糕的事情发生。

***
## 悬空指针

C++不保证使用指向被删除的指针将发生什么情况。在大多数情况下，返回给操作系统的内存将包含与返回之前相同的值。

指向已释放内存的指针称为悬空指针。解引用或删除悬空指针将导致未定义的行为。考虑以下程序:

```C++
#include <iostream>

int main()
{
    int* ptr{ new int }; // 动态分配一个整数
    *ptr = 7; // 给对应的内存赋值

    delete ptr; // 将内存归还给操作系统.  ptr 现在是悬空指针.

    std::cout << *ptr; // 解引用悬空指针，对导致未定义的行为
    delete ptr; //再次删除悬空指针，也会导致未定义的行为.

    return 0;
}
```

在上面的程序中，已经将ptr分配到的内存归还给操作系统，并且尝试访问该内存将导致未定义的行为。

一个delete操作可能会导致多个悬空指针。考虑以下示例:

```C++
#include <iostream>

int main()
{
    int* ptr{ new int{} }; // 动态分配一个整数
    int* otherPtr{ ptr }; // otherPtr 现在也指向同样的内存

    delete ptr; // 将内存归还给操作系统.  ptr 和 otherPtr 现在是悬空指针.
    ptr = nullptr; // ptr 设置为 nullptr

    // 然而, otherPtr 仍然是悬空指针

    return 0;
}
```

这里有一些最佳实践可以提供帮助。

首先，尝试避免让多个指针指向同一块动态内存。如果一定要这么做，请明确哪个指针“拥有”内存（并负责删除它），以及哪个指针正在访问它。

其次，当您删除指针时，如果该指针随后没有立即超出作用域，请将指针设置为nullptr。后续我们将详细讨论空指针，以及它们为什么有用。

{{< alert success >}}
**最佳实践**

将删除的指针设置为nullptr，除非它们随后立即超出作用域。

{{< /alert >}}

***
## new操作可能会失败

从操作系统请求内存时，在极少数情况下，操作系统可能没有任何内存来满足请求。

默认情况下，如果new失败，则抛出bad_alloc异常。如果这个异常没有被正确处理（并且它不会被正确处理，因为我们还没有讨论异常或异常处理），程序将简单地终止（崩溃），并出现未处理的异常错误。

在许多情况下，让new引发异常（或让程序崩溃）是不可取的，因此有另一种形式的new，可以用来告诉new在无法分配内存时返回空指针。这是通过在new关键字和分配类型之间添加std::nothrow来完成的:

```C++
int* value { new (std::nothrow) int }; // 如果分配失败，value将是空指针
```

在上面的示例中，如果new未能分配内存，它将返回空指针，而不是所分配内存的地址。

请注意，如果随后尝试解引用该指针，将导致未定义的行为（很可能是程序崩溃）。因此，如果使用nothrow，最佳实践是检查所有内存请求，以确保它们在使用分配的内存之前实际成功。

```C++
int* value { new (std::nothrow) int{} }; // 请求分配内存
if (!value) // 处理返回为空的情况
{
    // 做错误处理
    std::cerr << "Could not allocate memory\n";
}
```

因为请求新内存很少失败（在开发环境中几乎永远不会失败），所以通常会忘记执行此检查！

***
## 空指针和动态内存分配

空指针（设置为nullptr的指针）在处理动态内存分配时特别有用。在动态内存分配的上下文中，空指针基本上表示“没有内存分配给该指针”。这允许我们执行类似是否指针有效的逻辑:

```C++
// 如果ptr没有分配内存，分配一下
if (!ptr)
    ptr = new int;
```

删除空指针没有任何问题。因此，不需要以下内容:

```C++
if (ptr) // 如果ptr不为空
    delete ptr; // 删除它
// 否则做其它的事情
```

相反，您可以只写:

```C++
delete ptr;
```

如果ptr不为nullptr，则将删除动态分配的内存。如果为nullptr，则不会发生任何事情。

{{< alert success >}}
**最佳实践**

删除空指针是可以的，并且不执行任何操作。没有必要对删除语句进行条件化。

{{< /alert >}}

***
## 内存泄漏

动态分配的内存将保持分配状态，直到它被显式释放或程序结束（并且操作系统会清理它）。然而，用于保存动态分配的内存地址的指针遵循局部变量的正常作用域规则。这种不匹配可能会产生有趣的问题。

考虑以下函数:

```C++
void doSomething()
{
    int* ptr{ new int{} };
}
```

该函数动态分配整数，但从不使用delete释放它。因为指针变量ptr只是普通变量，所以当函数结束时，ptr将超出作用域。由于ptr是唯一保存动态分配的整数地址的变量，因此当ptr被销毁时，不再有对动态分配的内存的引用。这意味着程序现在“丢失”了动态分配的内存的地址。因此，无法删除此动态分配的整数。

这称为内存泄漏。当程序在将动态分配的内存返回给操作系统之前丢失其地址时，就会发生内存泄漏。发生这种情况时，程序无法删除动态分配的内存，因为它不再知道它在哪里。操作系统也无法使用该内存，因为该内存被认为仍在由程序使用。

内存泄漏会在程序运行时耗尽可用内存，从而使可用内存减少，不仅适用于当前程序，也适用于其他正在运行的程序。具有严重内存泄漏问题的程序可能会占用所有可用内存，导致整个计算机运行缓慢，甚至崩溃。只有在程序终止后，操作系统才能清理并“回收”所有泄漏的内存。

尽管指针超出作用域可能会导致内存泄漏，但也有其他方式可能导致内存泄漏。例如，如果为保存动态分配的内存的地址的指针分配另一个值，则可能发生内存泄漏:

```C++
int value = 5;
int* ptr{ new int{} }; // 分配内存
ptr = &value; // 老的地址丢失, 导致内存泄漏
```

可以通过在重新分配指针之前删除指针来解决此问题:

```C++
int value{ 5 };
int* ptr{ new int{} }; // 分配内存
delete ptr; // 将内存归还给操作系统
ptr = &value; // ptr重新赋值
```

相同地，还可以通过双重分配造成内存泄漏:

```C++
int* ptr{ new int{} };
ptr = new int{}; // 老的地址丢失, 导致内存泄漏
```

第二次分配返回的地址覆盖第一次分配的地址。因此，第一次分配成为内存泄漏！

类似地，可以通过确保在重新分配之前删除指针来避免这种情况。

***
## 结论

运算符new和delete允许我们为程序动态分配单个变量。

动态分配的内存具有动态持续时间，并将保持分配状态，直到您归还它给操作系统或程序终止。

注意不要对悬空指针或空指针执行解引用操作。

在下一课中，我们将了解如何使用new和delete来分配和删除数组。

***

{{< prevnext prev="/basic/chapter18/time-code/" next="/basic/chapter19/new-delete-arr/" >}}
18.3 为代码计时
<--->
19.1 动态分配数组
{{< /prevnext >}}
