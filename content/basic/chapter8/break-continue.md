---
title: "break与continue"
date: 2024-01-02T10:33:49+08:00
---

## break

之前，在switch语句学习时，已经对break有了一定的了解。这里对break做一个全面的总结。break语句会导致while循环、do-while环、for循环或switch语句结束，并执行循环或者switch后的下一个语句。

***
## swtich中的break

在switch语句的上下文中，通常在每个case的末尾使用break来表示case已完成（这可以防止fallthrough到下一个case中）：

```C++
#include <iostream>

void printMath(int x, int y, char ch)
{
    switch (ch)
    {
    case '+':
        std::cout << x << " + " << y << " = " << x + y << '\n';
        break; // 不会 fall-through 到下一个标签
    case '-':
        std::cout << x << " - " << y << " = " << x - y << '\n';
        break; // 不会 fall-through 到下一个标签
    case '*':
        std::cout << x << " * " << y << " = " << x * y << '\n';
        break; // 不会 fall-through 到下一个标签
    case '/':
        std::cout << x << " / " << y << " = " << x / y << '\n';
        break;
    }
}

int main()
{
    printMath(2, 3, '+');

    return 0;
}
```

***
## break跳出循环

在循环的上下文中，可以使用break语句提前结束循环。执行循环后的下一条语句。

例如：

```C++
#include <iostream>

int main()
{
    int sum{ 0 };

    // 允许用户最多输入10次
    for (int count{ 0 }; count < 10; ++count)
    {
        std::cout << "Enter a number to add, or 0 to exit: ";
        int num{};
        std::cin >> num;

        // 用户输入0，直接跳出循环
        if (num == 0)
            break; // 跳出循环

        // 将用户输入的值累加
        sum += num;
    }

    // for循环break之后继续执行
    std::cout << "The sum of all the numbers you entered is: " << sum << '\n';

    return 0;
}
```

该程序允许用户键入最多10个数字，并打印所有输入数字的总和。如果用户输入0，break将导致循环提前终止（在输入10个数字之前）。

下面是执行示例：

```C++
Enter a number to add, or 0 to exit: 5
Enter a number to add, or 0 to exit: 2
Enter a number to add, or 0 to exit: 1
Enter a number to add, or 0 to exit: 0
The sum of all the numbers you entered is: 8
```

break也是有意的跳出无限循环的常见方法：

```C++
#include <iostream>

int main()
{
    while (true) // 无限循环
    {
        std::cout << "Enter 0 to exit or any other integer to continue: ";
        int num{};
        std::cin >> num;

        // 用户输入0，直接跳出循环
        if (num == 0)
            break;
    }

    std::cout << "We're out!\n";

    return 0;
}
```

上述程序的示例运行：

```C++
Enter 0 to exit or any other integer to continue: 5
Enter 0 to exit or any other integer to continue: 3
Enter 0 to exit or any other integer to continue: 0
We're out!
```

***
## break与return

新程序员有时难以理解break与return之间的区别。break语句终止switch或循环，并在switch或循环之外的第一个语句处继续执行。return语句终止循环所在的整个函数，并在调用函数的点继续执行。

```C++
#include <iostream>

int breakOrReturn()
{
    while (true) // 无限循环
    {
        std::cout << "Enter 'b' to break or 'r' to return: ";
        char ch{};
        std::cin >> ch;

        if (ch == 'b')
            break; // 会执行循环后的第一条语句

        if (ch == 'r')
            return 1; // 结束执行，并返回到调用函数（这里是main()函数）
    }

    // 上面的break语句执行后，会在这里继续执行

    std::cout << "We broke out of the loop\n";

    return 0;
}

int main()
{
    int returnValue{ breakOrReturn() };
    std::cout << "Function breakOrReturn returned " << returnValue << '\n';

    return 0;
}
```

下面是该程序的两次运行：

```C++
Enter 'b' to break or 'r' to return: r
Function breakOrReturn returned 1
```

```C++
Enter 'b' to break or 'r' to return: b
We broke out of the loop
Function breakOrReturn returned 0
```

***
## continue

continue语句提供了一种方法，可以在不终止整个循环的情况下结束循环的当前迭代。

下面是使用continue的示例：

```C++
#include <iostream>

int main()
{
    for (int count{ 0 }; count < 10; ++count)
    {
        // 如果count被4整除, 结束本轮迭代
        if ((count % 4) == 0)
            continue; // 进入下一次迭代

        // 否则正常执行
        std::cout << count << '\n';

        // 后续的其它可能的语句
    }

    return 0;
}
```

该程序打印0到9之间不能被4整除的所有数字：

```C++
1
2
3
5
6
7
9
```

continue语句的工作方式是使当前执行点跳到当前循环的底部。

在for循环的情况下，for循环的递增/递减语句（在上面的示例中，是 ++count）仍然在continue之后执行（因为这发生在循环体的末尾之后）。

将continue语句与while或do-while循环一起使用时要小心。这些循环通常在循环体内更改循环变量。如果使用continue语句跳过这些行，循环可能变为无限循环！

考虑以下程序：

```C++
#include <iostream>

int main()
{
    int count{ 0 };
    while (count < 10)
    {
        if (count == 5)
            continue; // 调到循环体末尾

        std::cout << count << '\n';

        ++count; // 如果count加到 5 之后，这条语句永远不会再执行

        // continue 语句跳到这里
    }

    return 0;
}
```

该程序想打印0到9之间除了5的每个数字。但它实际上打印：

```C++
0
1
2
3
4
```

然后进入无限循环。当count为5时，if语句的计算结果为true，continue导致执行跳到循环的底部。++count不会被执行到。因此，在下一次迭代中，count仍然是5，if语句仍然为true，并且程序继续永远循环。

当然，您已经知道，如果有一个明显的计数器变量，则应该使用for循环，而不是while或do-while循环。

***
## 提前返回

不是函数中最后一个语句的return语句称为提前返回（early return）。许多程序员认为应该避免提前返回。return语句只在函数的最底部，这具有简单性——函数将接受参数，执行任何逻辑，并返回结果。有额外的返回会使逻辑复杂化。

但是，使用提前返回允许函数在完成后立即退出，这减少了对不必要逻辑的判断执行，并最大限度地减少了对条件嵌套的需要，这使得代码更具可读性。

一些开发人员采取中间立场，只在函数顶部使用提前返回来进行参数验证（捕获传入的错误参数）。

我们的立场是，提前返回更有帮助，而不是有害。

***
