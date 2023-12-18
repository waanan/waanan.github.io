---
title: "代码块"
date: 2023-12-18T16:52:52+08:00
---

代码块语句（block statement）是零个或多个语句组成的一组复合语句，编译器将其视为单个语句。

代码块以「 { 」符号开始，以「 } 」符号结束，要执行的语句放在两者之间。代码块可以在允许单个语句的任何地方使用。末尾不需要分号。

您已经看到了编写函数时的代码块示例，因为函数体是代码块：

```C++
int add(int x, int y)
{ // 代码块开始
    return x + y;
} // 代码块结束 (没有分号)

int main()
{ // 代码块开始

    // 多个语句
    int value {}; // 这是变量初始化，不是代码块
    add(3, 4);

    return 0;

} // 代码块结束 (没有分号)
```

***
## 代码块嵌套

函数不能嵌套在其他函数中，但代码块可以嵌套在其他块中：

```C++
int add(int x, int y)
{ // 代码块开始
    return x + y;
} // 代码块结束 

int main()
{ // 外围代码块

    // 多个语句
    int value {};

    { // 内部嵌套的代码块
        add(3, 4);
    } // 内部嵌套的代码块结束

    return 0;

} // 外围代码块结束
```

***
## 使用代码块在条件语句中执行多个语句

代码块的最常见用例之一是与if语句结合使用。默认情况下，如果条件表达式的计算结果为true，则if语句执行单个语句。如果希望在这时执行多个语句，则可以用语句块替换这条语句。

例如：

```C++
#include <iostream>

int main()
{ // 外围代码块
    std::cout << "Enter an integer: ";
    int value {};
    std::cin >> value;
    
    if (value >= 0)
    { // 内部嵌套的代码块
        std::cout << value << " is a positive integer (or zero)\n";
        std::cout << "Double this number is " << value * 2 << '\n';
    } // 内部嵌套的代码块结束
    else
    { // 内部嵌套的代码块
        std::cout << value << " is a negative integer\n";
        std::cout << "The positive of this number is " << -value << '\n';
    } // 内部嵌套的代码块结束

    return 0;
} // 外围代码块结束
```

如果用户输入数字3，该程序将打印：

```C++
Enter an integer: 3
3 is a positive integer (or zero)
Double this number is 6
```

如果用户输入数字-4，该程序将打印：

```C++
Enter an integer: -4
-4 is a negative integer
The positive of this number is 4
```

***
## 代码块多层嵌套

代码块可以多层嵌套：

```C++
#include <iostream>

int main()
{ // block 1, 层级 1
    std::cout << "Enter an integer: ";
    int value {};
    std::cin >> value;
    
    if (value >  0)
    { // block 2, 层级 2
        if ((value % 2) == 0)
        { // block 3, 层级 3
            std::cout << value << " is positive and even\n";
        }
        else
        { // block 4, 层级 3
            std::cout << value << " is positive and odd\n";
        }
    }

    return 0;
}
```

函数中代码块的最大嵌套深度，是从最外围到最内层的代码块的级数。在上面的函数中，有4个块，但嵌套级别为3，因为在该程序中，最大只能到第三层。

C++标准规定C++编译器应该支持256级嵌套——然而，并非所有的编译器都支持（例如，在编写本文时，VisualStudio支持较少的嵌套）。

最好将嵌套级别保持在3或更少。正如过长的函数是重构的良好候选者（分解为较小的函数）一样，过度嵌套的块很难阅读，也是重构的良好候选对象（大多数嵌套的块可以重构为单独的函数）。

{{< alert success >}}
**最佳实践**

将函数的嵌套级别保持在3或更少。如果函数需要更多嵌套级别，请考虑将函数重构为多个子函数。

{{< /alert >}}

***
