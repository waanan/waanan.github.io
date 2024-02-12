---
title: "默认参数"
date: 2024-02-10T01:33:43+08:00
---

默认参数是为函数参数提供的默认值。例如：

```C++
void print(int x, int y=10) // 10 是默认的参数值
{
    std::cout << "x: " << x << '\n';
    std::cout << "y: " << y << '\n';
}
```

进行函数调用时。如果调用方提供了对应值，则以传递的值为准。如果调用方不提供对应的值，则使用默认参数的值。

考虑以下程序：

```C++
#include <iostream>

void print(int x, int y=4) // 4 是默认的参数值
{
    std::cout << "x: " << x << '\n';
    std::cout << "y: " << y << '\n';
}

int main()
{
    print(1, 2); // 参数 y 使用传递的值 2
    print(3); // 参数 y 使用默认值 4, 就像调用的是 print(3, 4)

    return 0;
}
```

该程序产生以下输出：

```C++
x: 1
y: 2
x: 3
y: 4
```

在第一个函数调用中，调用方为这两个参数提供了显式值，因此使用这些值。在第二个函数调用中，调用方省略了第二个参数，因此使用了默认值4。

请注意，必须使用等号来指定默认参数。使用括号或大括号不符合语法：

```C++
void foo(int x = 5);   // ok
void goo(int x ( 5 )); // 编译失败
void boo(int x { 5 }); // 编译失败
```

也许令人惊讶的是，默认参数由编译器在函数调用点处理。在上面的例子中，当编译器看到print(3)时，它将把这个函数调用重写为print(3, 4)，以便传递值的数量与参数的数量匹配。然后，重写的函数调用按常规工作。

***
## 何时使用默认参数

当函数需要具有合理默认值，但您希望调用方可以根据需要覆盖该值时，默认参数是一个很好的功能。

例如，下面是两个通常使用默认参数的函数原型：

```C++
int rollDie(int sides=6);
void openLogFile(std::string filename="default.log");
```

***
## 多个默认参数

函数可以具有多个具有默认值的参数：

```C++
#include <iostream>

void print(int x=10, int y=20, int z=30)
{
    std::cout << "Values: " << x << " " << y << " " << z << '\n';
}

int main()
{
    print(1, 2, 3); // 全部显式传值
    print(1, 2); // z 使用默认参数
    print(1); // y z 使用默认参数
    print(); // x y z 使用默认参数

    return 0;
}
```

产生以下输出：

```C++
Values: 1 2 3
Values: 1 2 30
Values: 1 20 30
Values: 10 20 30
```

C++不支持这样的函数调用语法，如print(, , 3)（作为一种在使用x和y的默认参数时为z提供显式值的方法）。这有一个主要后果：

如果一个参数使用了默认值，那么所有后续直到结束的参数，都必须使用默认值

同时也不允许出现以下情况：

```C++
void print(int x=10, int y); // 不允许
```

{{< alert success >}}
**规则**

如果为参数给定默认值，则所有后续参数（右侧）也必须给定默认值。

{{< /alert >}}

***
## 无法重新声明默认参数

一旦声明，默认参数就不能重新声明（在同一文件中）。这意味着对于具有前向声明和函数定义的函数，默认参数可以在前向声明或函数定义中单独声明，但不能同时在两者中声明。

```C++
#include <iostream>

void print(int x, int y=4); // 前向声明

void print(int x, int y=4) // error: 重新定义默认参数
{
    std::cout << "x: " << x << '\n';
    std::cout << "y: " << y << '\n';
}
```

最佳实践是在前向声明中声明默认参数，而不是在函数定义中声明，因为前向声明更可能被其他文件看到（特别是在头文件中）。

在foo.h中：

```C++
#ifndef FOO_H
#define FOO_H
void print(int x, int y=4);
#endif
```

在main.cpp中：

```C++
#include "foo.h"
#include <iostream>

void print(int x, int y)
{
    std::cout << "x: " << x << '\n';
    std::cout << "y: " << y << '\n';
}

int main()
{
    print(5);

    return 0;
}
```

注意，在上面的例子中，我们能够为函数print()使用默认参数，因为main.cpp引用了foo.h，它具有定义默认参数的前向声明。

{{< alert success >}}
**最佳实践**

如果函数具有前向声明（特别是头文件中的声明），请在那里放置默认参数。否则，再将默认参数放在函数定义中。

{{< /alert >}}

***
## 默认参数和函数重载

可以重载具有默认参数的函数。例如，允许以下操作：

```C++
#include <string>

void print(std::string)
{
}

void print(char=' ')
{
}

int main()
{
    print("Hello, world"); // 调用的是 print(std::string)
    print('a'); // 调用的是 print(char)
    print(); // 调用的是 print(char)

    return 0;
}
```

对print()的函数调用的作用类似于用户显式调用了print('')，它解析为print(char)。

现在考虑这种情况：

```C++
void print(int x);
void print(int x, int y = 10);
void print(int x, double y = 20.5);
```

具有默认值的参数将能够区分重载函数（意味着上面的将通过编译）。然而，这样的函数在调用时可能会导致潜在的不明确匹配。例如：

```C++
print(1, 2); // 解析到 print(int, int)
print(1, 2.5); // 解析到 print(int, double) 
print(1); // 不明确匹配的函数调用
```

在最后一种情况下，编译器无法判断print(1)应该解析为print(int)，还是第二个参数具有默认值的两个函数之一。结果是一个不明确的函数调用。

***
## 总结

默认参数提供了一种有用的机制，用户可以选择覆盖或不覆盖参数的默认值。它在C++中经常使用，您将在以后的课程中看到它。

***
