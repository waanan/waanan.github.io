---
title: "基本异常处理"
date: 2025-02-12T14:07:59+08:00
---

在上一节中，我们讨论了使用返回码会导致控制流和错误流混合，从而导致混乱。本节来讲解异常的基本使用。

C++中的异常是使用三个关键字来实现的，这三个关键字相互关联：throw、try和catch。

***
## 引发异常

在现实生活中，我们一直使用信号来标记特定事件的发生。例如，在足球比赛中，如果一名球员犯规，裁判会吹口哨暂停这场比赛。然后评估并执行处罚。一旦处罚得到处理，比赛通常会恢复正常。

在C++中，throw语句用于发出异常信号。发出异常信号的行为通常也被称为引发异常。

要使用throw语句，只需使用throw关键字，后跟表示发生错误的任何数据类型的值。通常，该值将是错误码、问题描述或自定义异常类。

下面是一些示例：

```C++
throw -1; // throw 一个 int 值
throw ENUM_INVALID_INDEX; // throw 一个 枚举值
throw "Can not take square root of negative number"; // throw 一个C样式字符串 (const char*)
throw dX; // throw 一个定义的变量
throw MyException("Fatal Error"); // Throw 一个 MyException 类的对象
```

这些语句中的每一个都充当信号，表示需要处理某种发生的问题。

***
## 监听异常发生

引发异常只是异常处理过程的一部分。让我们回到足球类比：一旦裁判吹响了口哨，接下来会发生什么？球员注意到需要停止比赛。足球比赛的正常进行被打乱了。

在C++中，我们使用try关键字来定义语句块（称为try块）。try块充当观察者，查找由try块中的任何语句引发的任何异常。

下面是try块的示例：

```C++
try
{
    // 任何可能会引发异常的语句，在try块内被监听
    throw -1; // 这是一个简单的throw语句
}
```

注意，try块没有定义如何处理异常。它只是告诉程序，“嘿，如果这个try块中的任何语句抛出异常，抓住它！”。

***
## 处理异常

最后，到了足球类比的最后一步：在犯规被判罚并且比赛停止后，裁判评估点球并执行它。换句话说，在恢复正常比赛之前，必须处理好点球。

实际上，处理异常是catch块的工作。catch关键字用于定义代码块（称为catch块），该代码块处理单个数据类型的异常。

下面是捕获整数异常的catch块的示例：

```C++
catch (int x)
{
    // 这里处理一个 int 类型的异常
    std::cerr << "We caught an int exception with value" << x << '\n';
}
```

Try块和catch块一起工作——Try块检测Try块中的语句抛出的异常，并将它们路由到具有匹配类型的catch块进行处理。try块后面必须紧跟至少一个catch块，但可以按顺序列出多个catch模块。

一旦异常被try块捕获并路由到匹配的catch块进行处理，则认为该异常已被处理。在匹配的catch块执行完，然后恢复正常，从最后一个catch块之后的第一条语句开始执行。

Catch参数的工作方式与函数参数类似，参数在后续的Catch块中可用。基本类型的异常可以由值捕获，但非基本类型的异常应该由常量引用捕获，以避免进行不必要的复制（在某些情况下，防止对象切片）。

与函数一样，如果参数不打算在catch块中使用变量名，则可以省略：

```C++
catch (double) // 注: 没有变量名，因为下方没有使用
{
    // 处理 double 类型的异常
    std::cerr << "We caught an exception of type double\n";
}
```

这有助于防止编译器对未使用的变量发出警告。

此外，不会对异常进行类型转换（因此不会转换int异常以匹配具有double参数的catch块）。

***
## try、throw、catch

下面是一个使用throw、try和多个catch块的完整程序：

```C++
#include <iostream>
#include <string>

int main()
{
    try
    {
        // 抛出异常
        throw -1; // 这是一个简单的例子
    }
    catch (double) // 注: 没有变量名，因为下方没有使用
    {
        // try块内的double异常会在这里处理
        std::cerr << "We caught an exception of type double\n";
    }
    catch (int x)
    {
        // try块内的int异常会在这里处理
        std::cerr << "We caught an int exception with value: " << x << '\n';
    }
    catch (const std::string&) // const引用 异常捕获
    {
        // try块内的std::string异常会在这里处理
        std::cerr << "We caught an exception of type std::string\n";
    }

    // 异常处理完后，会在这里接着执行
    std::cout << "Continuing on our merry way\n";

    return 0;
}
```

在作者的计算机上，运行上述try/catch块会产生以下结果：

```C++
We caught an int exception with value -1
Continuing on our merry way
```

throw语句用于引发值为-1的异常，该异常属于int类型。然后，throw语句被try块捕获，并路由到处理int类型异常的适当catch块。该catch块打印了适当的错误消息。

一旦异常被处理，程序在catch块后继续正常运行，并打印“Continuing on our merry way”。

***
## 异常处理概括

异常处理实际上相当简单，下面两段涵盖了您需要记住的大部分内容：

当引发异常时（使用throw），运行的程序会查找最近的try块（如果需要查找try块，则向上查看堆栈——我们将在下一课中更详细地讨论这一点），以查看附加到try块的任何catch处理程序是否可以处理该类型的异常。如果是这样，则执行流跳到对应catch块的顶部，该异常被认为已处理。

如果最近的try块中不存在适当的catch处理程序，则程序将继续查看后续try块中的catch块。如果在程序结束之前找不到适当的捕获处理程序，则程序将失败，并出现运行时异常错误。

请注意，当将异常与catch块匹配时，程序不会执行隐式类型转换或提升！例如，char异常将与int catch块不匹配。int异常将与float catch块不匹配。然而，将执行从派生类到其父类的强制转换。

这就是异常的全部内容。本章的其余部分将致力于展示这些原则在实际中的示例。

***
## 立即处理异常

下面是一个简短的程序，演示如何立即处理异常：

```C++
#include <iostream>

int main()
{
    try
    {
        throw 4.5; // 抛出类型为 double 的异常
        std::cout << "This never prints\n";
    }
    catch (double x) // 处理类型为 double 的异常
    {
        std::cerr << "We caught a double of value: " << x << '\n';
    }

    return 0;
}
```

这个程序非常简单。发生的情况如下：throw语句是执行的第一个语句——这导致抛出double类型的异常。执行立即移动到最近的try块，这是该程序中唯一的try块。然后检查catch处理程序，以查看是否有任何catch处理程序匹配。我们的异常是double类型，因此寻找double类型的catch处理程序。有一个，所以它会执行。

因此，该程序的结果如下：

```C++
We caught a double of value: 4.5
```

请注意，从不打印“This never prints”，因为异常导致执行路径立即跳转到double的catch处理程序。

***
## 一个更现实的例子

让我们看一个更实际的例子：

```C++
#include <cmath> // for sqrt()
#include <iostream>

int main()
{
    std::cout << "Enter a number: ";
    double x {};
    std::cin >> x;

    try // 监听try块内的异常，并将其发送到catch块
    {
        // 如果用户输入小于0, 那么肯定是有问题
        if (x < 0.0)
            throw "Can not take sqrt of negative number"; // 抛出类型为 const char* 的异常

        // 否则, 打印计算结果
        std::cout << "The sqrt of " << x << " is " << std::sqrt(x) << '\n';
    }
    catch (const char* exception) // 处理类型为 const char* 的异常
    {
        std::cerr << "Error: " << exception << '\n';
    }
}
```

在此代码中，要求用户输入数字。如果输入正数，则不会执行If语句，不会引发异常，并打印数字的平方根。因为在这种情况下不会引发异常，所以catch块内的代码不执行。结果如下：

```C++
Enter a number: 9
The sqrt of 9 is 3
```

如果用户输入负数，则抛出const char\*类型的异常。因为我们在try块中，并且找到了匹配的异常catch处理程序，所以控制流立即转移到const char\*异常处理程序。结果是：

```C++
Enter a number: -4
Error: Can not take sqrt of negative number
```

现在，您应该已经了解了异常背后的基本思想。在下一课中，我们将再举几个例子来展示异常的灵活性。

***
## catch块通常做什么

如果异常被路由到catch块，则即使catch块为空，也会将其视为“已处理”。然而，通常您希望catch块执行一些有用的操作。当catch块捕获异常时，它们通常做四件事：

首先，catch块可以打印错误（到控制台或日志文件），然后允许函数继续执行。

其次，catch块可以将值或错误码返回给调用者。

第三，catch块可能会引发另一个异常。因为catch块在try块之外，所以在这种情况下新抛出的异常不由当前try块处理——它由更外围的try块来处理。

第四，main()中的catch块可以用于捕获致命错误并以干净的方式终止程序。

***

{{< prevnext prev="/basic/chapter27/exception-need/" next="/basic/chapter27/exception-func-stack-unwind/" >}}
27.0 为什么需要异常机制
<--->
27.2 异常、函数和堆栈展开
{{< /prevnext >}}
