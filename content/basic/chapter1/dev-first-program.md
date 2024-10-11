---
title: "开发第一个程序"
date: 2023-10-022T20:06:10+08:00
---

前面的课程介绍了许多术语和概念，我们将在程序中使用这些术语和概念。在本课中，将介绍的这些知识集成到第一个简单程序中的过程。

***
## 乘以2

首先，创建一个程序，要求输入整数，等待输入整数，返回该数字的2倍是多少。程序产生以下输出（假设输入了4作为输入）：

```C++
Enter an integer: 4
Double that number is: 8
```

如何解决这一问题？将编写该程序分步。

完成每个步骤时，将对应的程序输入（不要复制/粘贴）到编译器中，编译并运行它。

首先，创建一个新的控制台项目。

现在，从一些基本的架子开始。需要main（）函数（因为所有C++程序都必须有main函数），因此创建一个：

```C++
int main()
{
    return 0;
}
```

将文本输出到控制台，并从用户的键盘获取文本，因此需要包括iostream来访问std::cout和std::cin。

```C++
#include <iostream>

int main()
{
    return 0;
}
```

现在，告诉用户输入整数：

```C++
#include <iostream>

int main()
{
    std::cout << "Enter an integer: ";

    return 0;
}
```

此时，程序应产生结果：

```C++
Enter an integer: 
```

然后终止。

接下来，将获取用户的输入。使用std::cin和operator>>来获取用户的输入。还需要定义一个变量来存储以供以后使用。

```C++
#include <iostream>

int main() // note: 该程序存在一个错误
{
    std::cout << "Enter an integer: ";

    int num{ }; // 定义一个存储整数的变量num
    std::cin << num; // 从用户的键盘输入中，获取一个整数值

    return 0;
}
```

是时候编译代码了。

以下是作者在Visual Studio 2017上获得的信息：


```C++
1>------ Build started: Project: Double, Configuration: Release Win32 ------
1>Double.cpp
1>c:\vcprojects\double\double.cpp(8): error C2678: binary '<<': no operator found which takes a left-hand operand of type 'std::istream' (or there is no acceptable conversion)
1>c:\vcprojects\double\double.cpp: note: could be 'built-in C++ operator<<(bool, int)'
1>c:\vcprojects\double\double.cpp: note: while trying to match the argument list '(std::istream, int)'
1>Done building project "Double.vcxproj" -- FAILED.
========== Build: 0 succeeded, 1 failed, 0 up-to-date, 0 skipped ==========
```

遇到了编译错误！

首先，由于程序是在进行最新更新之前可以正常编译。因此错误一定在刚才添加的代码中（第7行和第8行）。这大大减少了发现错误的工作量。第7行相当简单（只是一个变量定义），错误可能不在这。使得第8行为可能的罪魁祸首。

其次，此错误消息不容易阅读。区分一些关键元素：它在第8行遇到了错误。意味着实际的错误可能在第8行，可能在前一行，正是我们之前的猜测。接下来，编译器告诉我们，它找不到具有类型std::istream（即std:∶cin的类型）的左侧操作数的“<<”运算符。换句话说，操作符<<不知道如何处理std::cin，因此错误必须是由于使用std:∶cin或使用操作符<<。

看到错误了吗？如果没有，花点时间看看。

下面是更正代码的程序：

```C++
#include <iostream>

int main()
{
    std::cout << "Enter an integer: ";

    int num{ };
    std::cin >> num; // std::cin 使用 >>, 而不是 <<!

    return 0;
}
```

现在程序将通过编译，可以测试它。程序将等待您输入数字，输入4。输出应如下所示：

```C++
Enter an integer: 4
```

最后一步将数字加倍。

完成了最后一步，程序将编译并成功运行，产生所需的输出。

至少有3种方法可以做到这一点。让我们从最坏的改进到最好的版本。

{{< alert success >}}
**最佳实践**

新手程序员通常一次性编写整个程序，在它产生大量错误时不知所措。更好的策略是一次添加一个代码片段，确保它编译并测试它。然后，当确定它正常工作时，继续编写下一个片段。

{{< /alert >}}

***
## 不好的解决方案

```C++
#include <iostream>

// 最坏的方式
int main()
{
    std::cout << "Enter an integer: ";

    int num{ };
    std::cin >> num;

    num = num * 2; // 将num的值翻倍，然后赋值给num

    std::cout << "Double that number is: " << num << '\n';

    return 0;
}
```

使用一个表达式将num乘以2，然后将该值赋回num。此刻开始，num为加倍的数字。

为什么这是个糟糕的解决方案：

1. 在赋值语句之前，num为用户的输入。赋值后，它为不同的值。令人困惑。
2. 通过为变量分配新的值来覆盖用户的输入。如果想在以后程序中使用该输入值做其他事情（例如，将用户的输入增加三倍），它已经丢失了。


***
## 好点的解决方案

```C++
#include <iostream>

// 不那么坏的版本
int main()
{
    std::cout << "Enter an integer: ";

    int num{ };
    std::cin >> num;

    int doublenum{ num * 2 }; // 将 num * 2 赋值给新的变量
    std::cout << "Double that number is: " << doublenum << '\n';

    return 0;
}
```

该解决方案非常容易阅读和理解，并解决了最差解决方案中遇到的两个问题。

主要缺点是，定义了新的变量（这增加了复杂性）来存储只使用一次的值。我们可以做得更好。

***
## 首选解决方案

```C++
#include <iostream>

// 推荐版本
int main()
{
    std::cout << "Enter an integer: ";

    int num{ };
    std::cin >> num;

    std::cout << "Double that number is: " <<  num * 2 << '\n'; // 在输出的时候，使用一个表达式来计算num * 2 的值

    return 0;
}
```

这是首选解决方案。当执行std::cout时，将计算表达式num*2，结果是num的倍数。然后打印该值。num不会被更改，如果愿意，稍后再次使用它。

此版本是首选解决方案。

{{< alert success >}}
**注**

编程的主要目标是使程序工作。不管程序写得多好，不工作的程序都是没有用处的。

然而，我很喜欢一句话：“你必须编写完程序一次，才能知道应该如何第一次编写它。”说明了一个事实，即最好的解决方案并不明显，而对问题的第一个解决方案通常没有做到最好。

当专注于弄清楚如何使程序工作时，甚至不知道是否某些代码能正确运行。所以我们会跳过错误处理和注释等内容。在整个解决方案中插入调试代码，以帮助诊断问题和发现错误。边做边学，认为奏效的事情可能会不奏效，回过头来，尝试另一种方法。

结果是，初始解决方案不是结构良好、健壮（防错）、可读或简洁的。因此，即使程序开始工作，工作也没有完成（除非程序是一次性的）。下一步是清理代码。涉及到一些事情：删除（或注释掉）临时/调试代码，添加注释，处理错误情况，格式化代码，以及确保遵循最佳实践。即使如此，程序也可能没有那么优雅——也许存在可以合并的冗余逻辑，或者可以组合的多个语句，或者不需要的变量，或者多个可以简化的东西。

教程提供的解决方案中，很少有第一次编写就写到最好的。相反，它们是不断改进的结果，直到没有东西改进为止。在许多情况下，读者仍然可以找到许多其他的改进建议！

所有这一切都是在说：如果你的解决方案没有从大脑中完美地优化出来时，不要沮丧。这很正常。编程中的完善是一个迭代过程（需要重复进行的过程）。

{{< /alert >}}

{{< alert success >}}
**注**

还有一件事：您可能会想，“C++有这么多规则和概念。我如何记住所有这些东西？”。

简短的回答：没有人能记住。使用C++分为两部分，一部分是使用您所知道的内容，另一边部分是查找如何完成其余工作。

当你第一次阅读这个网站时，不要太注重记忆细节，而要更多地理解什么是可行的。然后，当需要在编写的程序中实现某些东西时，可以回到这里（或到参考网站），并重新了解如何去做的细节。

{{< /alert >}}


***

{{< prevnext prev="/basic/chapter1/exp/" next="/basic/chapter1/summary/" >}}
1.9 表达式简介
<--->
1.11 第1章总结
{{< /prevnext >}}
