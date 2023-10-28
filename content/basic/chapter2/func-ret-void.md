---
title: "无返回值函数"
date: 2023-10-09T20:06:10+08:00
---

在上一课（2.1——函数简介）中，我们指出函数定义的语法如下所示：

尽管我们展示了具有返回类型void的函数的示例，但我们没有讨论这意味着什么。在本课中，我们将探索返回类型为void的函数。

***
## 无效返回值

函数不需要将值返回给调用方。要告诉编译器函数不返回值，请使用返回类型void。例如：

```C++
#include <iostream>

// void means the function does not return a value to the caller
void printHi()
{
    std::cout << "Hi" << '\n';

    // This function does not return a value so no return statement is needed
}

int main()
{
    printHi(); // okay: function printHi() is called, no value is returned

    return 0;
}
```

在上面的例子中，printHi函数有一个有用的行为（它打印“Hi”），但它不需要向调用者返回任何内容。因此，printHi被赋予无效返回类型。

当main调用printHi时，执行printHi中的代码，并打印“Hi”。在printHi结束时，控制返回main，程序继续。

不返回值的函数称为非值返回函数（或void函数）。

***
## Void函数不需要return语句

void函数将在函数结束时自动返回给调用方。不需要返回语句。

可以在void函数中使用返回语句（没有返回值）——这样的语句将导致函数在执行return语句的点返回给调用方。无论如何，这与函数末尾发生的事情是相同的。因此，将空返回语句放在void函数的末尾是多余的：

```C++
#include <iostream>

// void means the function does not return a value to the caller
void printHi()
{
    std::cout << "Hi" << '\n';

    return; // tell compiler to return to the caller -- this is redundant since the return will happen at the end of the function anyway!
} // function will return to caller here

int main()
{
    printHi();

    return 0;
}
```

{{< alert success >}}
**最佳做法**

不要将return语句放在非值返回函数的末尾。

{{< /alert >}}

***
## Void函数不能在需要值的表达式中使用

某些类型的表达式需要值。例如：

```C++
#include <iostream>

int main()
{
    std::cout << 5; // ok: 5 is a literal value that we're sending to the console to be printed
    std::cout << ;  // compile error: no value provided

    return 0;
}
```

在上述程序中，需要在std:：cout<<的右侧提供要打印的值。如果没有提供值，编译器将产生语法错误。由于对std:：cout的第二次调用没有提供要打印的值，因此这会导致错误。

现在考虑以下程序：

```C++
#include <iostream>

// void means the function does not return a value to the caller
void printHi()
{
    std::cout << "Hi" << '\n';
}

int main()
{
    printHi(); // okay: function printHi() is called, no value is returned

    std::cout << printHi(); // compile error

    return 0;
}
```

对printHi（）的第一个调用是在不需要值的上下文中调用的。由于函数不返回值，因此这很好。

对函数printHi（）的第二个函数调用甚至无法编译。函数printHi具有void返回类型，这意味着它不返回值。然而，该语句试图将printHi的返回值发送到要打印的std:：cout。std：：cout不知道如何处理此问题（它将输出什么值？）。因此，编译器会将其标记为错误。您需要注释掉这一行代码，以便使代码能够编译。

{{< alert success >}}
**提示**

一些语句需要提供值，而其他语句则不需要。

当我们单独调用函数时（例如，上面示例中的第一个printHi（）），我们调用的是函数的行为，而不是其返回值。在这种情况下，我们可以调用非值返回函数，也可以调用值返回函数并忽略返回值。

当我们在需要值的上下文中调用函数时（例如，std:：cout），必须提供值。在这种上下文中，我们只能调用返回值的函数。

```C++
#include <iostream>

// Function that does not return a value
void returnNothing()
{
}

// Function that returns a value
int returnFive()
{
    return 5;
}

int main()
{
    // When calling a function by itself, no value is required
    returnNothing(); // ok: we can call a function that does not return a value
    returnFive();    // ok: we can call a function that returns a value, and ignore that return value

    // When calling a function in a context that requires a value (like std::cout)
    std::cout << returnFive();    // ok: we can call a function that returns a value, and the value will be used
    std::cout << returnNothing(); // compile error: we can't call a function that returns void in this context

    return 0;
}
```

{{< /alert >}}

***
## 从void函数返回值是编译错误

尝试从非值返回函数中返回值将导致编译错误：

```C++
void printHi() // This function is non-value returning
{
    std::cout << "In printHi()" << '\n';

    return 5; // compile error: we're trying to return a value
}
```

***
## 测验时间

问题#1

检查以下程序，并说明它们输出的内容，或者它们是否将不编译。

1a）

```C++
#include <iostream>

void printA()
{
    std::cout << "A\n";
}

void printB()
{
    std::cout << "B\n";
}

int main()
{
    printA();
    printB();

    return 0;
}
```

显示解决方案

1b）

```C++
#include <iostream>

void printA()
{
    std::cout << "A\n";
}

int main()
{
    std::cout << printA() << '\n';

    return 0;
}
```

显示解决方案

