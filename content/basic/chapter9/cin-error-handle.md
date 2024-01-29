---
title: "std::cin和处理无效输入"
date: 2024-01-17T13:13:14+08:00
---

大多数具有某种用户界面的程序都需要处理用户输入。在我们现在正在编写的程序中，一直在使用std::cin来要求用户输入文本。因为文本输入是如此自由的形式（用户可以输入任何内容），所以用户很容易输入不符合期望的输入。

在编写程序时，应该始终考虑用户将如何（无意中或以其他方式）滥用程序。一个编写良好的程序将预测用户将如何滥用它，并要么优雅地处理这些情况，要么从一开始就防止它们发生（如果可能）。一个能够很好地处理错误情况的程序被认为是健壮的。

在本课中，将专门研究用户通过std::cin输入无效文本输入的方法，并向您展示一些处理这些情况的不同方法。

***
## std::cin、缓冲区和提取

为了讨论std::cin和operator>>是如何失败的，首先了解一下它们是如何工作的。

当我们使用操作符>>获取用户输入并将其放入变量时，这称为“提取”。在该上下文中使用时，>>操作符相应地称为提取操作符。

当用户响应提取操作输入时，该数据被放在std::cin内的缓冲区中。缓冲区（也称为数据缓冲区）只是一块内存，用于在数据从一个位置移动到另一个位置时临时存储数据。在这种情况下，缓冲区用于保存用户输入，同时等待将其提取为变量。

使用提取操作符时，将执行以下过程:

1. 如果输入缓冲区中已经存在数据，则使用该数据进行提取。
2. 如果输入缓冲区不包含数据，则要求用户输入数据以进行提取（大多数情况下都是这样）。当用户点击enter时，将在输入缓冲区中放置“\n”字符。
3. 操作符>>将尽可能多的数据从输入缓冲区提取到变量中（忽略任何前导空格字符，如空格、制表符或“\n”）。
4. 无法提取的任何数据都留在输入缓冲区中，供下一次提取使用。

如果从输入缓冲区提取了至少一个字符，则提取成功。任何未提取的输入都保留在输入缓冲区中，以供将来提取。例如:

```C++
int x{};
std::cin >> x;
```

如果用户键入5a，然后单击enter，则将提取5，将其转换为整数，并分配给变量x。"a\n"将在输入缓冲区中保留，以供下次提取。

如果输入数据与要提取到的变量的类型不匹配，则提取失败。例如:

```C++
int x{};
std::cin >> x;
```

如果用户要输入“b”，则提取将失败，因为“b”无法提取为整数变量。

***
## 验证输入

检查用户输入是否符合程序期望的过程称为输入验证。

有三种基本的输入验证方法:

用户边输入边校验:

1. 阻止用户输入无效的字符。

用户输入完成后再校验:

2. 将用户输入的所有保存到字符串中, 然后验证字符串是否ok, 如果ok, 将字符串转换成最终的格式
3. 让用户任意输入, 使用 std::cin 和 operator>> 去提取数据, 同时处理提取失败的情形.

一些图形用户界面和高级文本界面允许您在用户输入时验证输入（逐个字符）。一般来说，程序员提供一个验证函数，该函数接受用户迄今为止的输入，如果输入有效则返回true，否则返回false。每次用户按下键时都会调用此函数。如果验证函数返回true，则接受用户刚才按下的键。如果验证函数返回false，则用户刚才输入的字符将被丢弃（并且不会显示在屏幕上）。使用此方法，可以确保用户输入的任何输入都是有效的，因为任何无效的击键都会被发现并立即丢弃。不幸的是，std::cin不支持这种类型的验证。

由于字符串对可以输入的字符没有任何限制，如果使用operator>>将输入提取到字符串中，提取保证成功（请记住，std::cin在第一个非前导空格字符处停止提取）。一旦提取了字符串，程序就可以解析该字符串，看看它是否有效。然而，解析字符串并将字符串输入转换为其他类型（例如数字）可能是具有挑战性的，所以这种方式只在少数情况下使用。

最常见的是，让std::cin和提取操作符来完成困难的工作。在这种方法下，我们让用户输入他们想要的任何内容，让std::cin和操作符>>尝试提取它，并在它失败时处理后果。这是最简单的方法，也是在下面详细讨论的方法。

***
## 示例程序

考虑以下没有错误处理的计算器程序:

```C++
#include <iostream>
 
double getDouble()
{
    std::cout << "Enter a decimal number: ";
    double x{};
    std::cin >> x;
    return x;
}
 
char getOperator()
{
    std::cout << "Enter one of the following: +, -, *, or /: ";
    char op{};
    std::cin >> op;
    return op;
}
 
void printResult(double x, char operation, double y)
{
    switch (operation)
    {
    case '+':
        std::cout << x << " + " << y << " is " << x + y << '\n';
        break;
    case '-':
        std::cout << x << " - " << y << " is " << x - y << '\n';
        break;
    case '*':
        std::cout << x << " * " << y << " is " << x * y << '\n';
        break;
    case '/':
        std::cout << x << " / " << y << " is " << x / y << '\n';
        break;
    }
}
 
int main()
{
    double x{ getDouble() };
    char operation{ getOperator() };
    double y{ getDouble() };
 
    printResult(x, operation, y);
 
    return 0;
}
```

这个简单的程序要求用户输入两个数字和一个数学运算符。

现在，考虑无效的用户输入，可能会破坏该程序的哪里？

首先，我们要求用户输入一些数字。如果他们输入数字以外的内容（例如“q”）会怎么样？在这种情况下，提取将失败。

其次，我们要求用户输入四个可能的符号之一。如果他们输入的字符不是我们期望的符号之一，该怎么办？我们将能够提取输入，但没有处理输入错误符号的情形。

第三，我们要求用户输入符号，而他们输入类似“*qhello”的字符串，该怎么办。尽管我们可以提取所需的“*”字符，但缓冲区中还有额外的输入，这会在以后导致问题。

***
## 无效文本输入的类型

通常可以将输入文本错误分为四种类型:

1. 输入提取成功，但输入对程序没有意义（例如，输入“k”作为数学运算符）。
2. 输入提取成功，但用户后续输入了其他输入（例如，输入“*q hello”作为数学运算符）。
3. 输入提取失败（例如，尝试在数字输入中输入“q”）。
4. 输入提取成功，但输入数值发生了溢出。


因此，为了使程序健壮，每当要求用户输入时，理想情况下，应该确定上述每一种情况是否可能发生，并编写代码来处理这些情况。

让我们深入研究每一种情况，以及如何使用std::cin处理它们。

***
## 错误情况1:提取成功，但输入无意义

这是最简单的情况。考虑上述程序的以下执行:

```C++
Enter a decimal number: 5
Enter one of the following: +, -, *, or /: k
Enter a decimal number: 7
```

在这种情况下，要求用户输入四个符号中的一个，但他们输入的是“k”，k是一个有效字符，因此std::cin将其提取到变量op中，并将其返回给main。但程序并没有预料到这种情况会发生，因此它没有正确地处理这种情况（因此从不输出任何内容）。

这里的解决方案很简单:进行输入验证。这通常包括3部分:

1. 检查用户的输入是否是我们所期望的
2. 如果是的话，执行后续流程
3. 如果不是，提示用户，并让用户进行重试

下面是一个新的getOperator()函数，对用户输入进行验证。

```C++
char getOperator()
{
    while (true) // 无限循环，直到用户输入有效的数据
    {
        std::cout << "Enter one of the following: +, -, *, or /: ";
        char operation{};
        std::cin >> operation;

        // 检查是否用户输入是否有效
        switch (operation)
        {
        case '+':
        case '-':
        case '*':
        case '/':
            return operation; // 将有效的输入返回
        default: // 否则提示用户输入有误
            std::cout << "Oops, that input is invalid.  Please try again.\n";
        }
    }
}
```

如上使用while来无限的循环，直到用户提供有效的输入。如果输入有误，要求他们重试，直到提供有效的输入、关闭程序或销毁他们的计算机。

***
## 错误情况2:提取成功，但有多余的输入

考虑上述程序的以下执行:

```C++
Enter a decimal number: 5*7
```

你认为接下来会发生什么？

```C++
Enter a decimal number: 5*7
Enter one of the following: +, -, *, or /: Enter a decimal number: 5 * 7 is 35
```

程序打印了正确的答案，但格式完全混乱。让我们仔细看看原因。

当用户输入5\*7作为输入时，该输入进入缓冲区。然后操作符>>将5提取到变量x，将"\*7\n"留在缓冲区中。接下来，程序打印"Enter one of the following: +, -, \*, or /:"。然而，当调用提取操作符时，它看到"\*7\n"正在缓冲区中等待提取，因此它使用该操作符，而不是要求用户提供更多输入。r然后，它提取“*”字符，在缓冲区中保留"7\n"。

在要求用户输入另一个十进制数后，直接从缓冲区中提取7。由于用户从未有机会输入额外的数据并按enter键（换行），因此输出提示都在同一行上一起运行。

尽管上面的程序可以工作，但执行是混乱的。最好一个办法是简单地忽略输入的任何无关字符。幸运的是，很容易忽略字符:

```C++
std::cin.ignore(100, '\n');  // 清空缓存中的100个字符, 或者直到一个 '\n' 被清除
```

这个调用将删除多达100个字符，但如果用户输入的字符超过100个，我们将再次得到混乱的输出。要忽略下一个“\n”之前的所有字符，可以将std::numeric_limits<std::streamsize>::max()传递给std::cin.ignore()。std::numeric_limits<std::streamsize>::max() 返回可以存储在类型为std::streamsize的变量中的最大值。将该值传递给std::cin.ignore()会导致std::cin清空所有缓存。

要忽略直到并包括下一个“\n”字符的所有内容，调用

```C++
std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
```

这一行代码对于它所做的事情来说相当长，所以将它包装在一个可以代替std::cin.ignore()调用的函数中很方便。

```C++
#include <limits> // for std::numeric_limits

void ignoreLine()
{
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}
```

由于用户输入的最后一个字符通常是“\n”，因此我们可以告诉std::cin忽略缓冲字符，直到它找到换行符（“\n”也被删除）。

现在更新getDouble()函数以忽略任何无关的输入:

```C++
double getDouble()
{
    std::cout << "Enter a decimal number: ";
    double x{};
    std::cin >> x;

    ignoreLine();
    return x;
}
```

现在，程序将按预期工作，即使第一个输入了“5*7”——5将被提取，其余的字符将从输入缓冲区中删除。由于输入缓冲区现在为空，因此下次执行提取操作时将正确要求用户输入！

{{< alert success >}}
**提示**

在某些情况下，最好将无关的输入视为故障情况（而不是忽略它）。然后，我们可以要求用户重新输入。

为了做到这一点，我们需要某种方法来确定在成功提取后输入流中是否还有任何输入。我们可以使用std::cin.peek()函数，它允许查看输入流中的下一个字符，而不提取它。

下面是getDouble()的变体，它要求用户在输入任何无关输入时重新输入:

```C++
double getDouble()
{
    while (true) // 无限循环，直到用户输入有效的数据
    {
        std::cout << "Enter a decimal number: ";
        double x{};
        std::cin >> x;

        // 如果有额外的输入, 当做用户输入失败
        if (!std::cin.eof() && std::cin.peek() != '\n')
        {
            ignoreLine(); // 移除缓冲区内的所有字符
            continue;
        }
    
        ignoreLine();

        return x;
    }
}
```

{{< /alert >}}

***
## 错误情况3:提取失败

现在考虑执行以下的执行:

```C++
Enter a decimal number: a
```

您不应该对程序没有按预期执行感到惊讶，但它如何失败是有趣的:

```C++
Enter a decimal number: a
Enter one of the following: +, -, *, or /: Oops, that input is invalid.  Please try again.
Enter one of the following: +, -, *, or /: Oops, that input is invalid.  Please try again.
Enter one of the following: +, -, *, or /: Oops, that input is invalid.  Please try again.
```

最后一行持续打印，直到程序关闭。

这看起来与无关的输入案例非常相似，但有点不同。让我们仔细看看。

当用户输入“a”时，该字符将放在缓冲区中。然后操作符>>尝试将“a”提取到变量x，该变量的类型为double。由于“a”无法转换为double，因此操作符>>无法执行提取。此时会发生两件事:“a”留在缓冲区中，std::cin进入“故障模式”。

一旦进入“故障模式”，未来的输入提取请求将自动失败。因此，在我们的程序中，输出提示仍然打印，但任何进一步提取的请求都将被忽略。这意味着，进行输入操作时，将跳过输入提示符，并且将陷入无限循环中。

幸运的是，我们可以检测提取是否失败:

```C++
if (std::cin.fail()) // 是否之前的提取失败
{
    // 这里来处理失败
    std::cin.clear(); // 将std::cin调回 '正常' 模式 
    ignoreLine();     // 移除缓存中的错误数据
}
```

由于std::cin可以直接指示上一次提取操作的状态，因此更习惯于将上面的内容编写为:

```C++
if (!std::cin) // 是否之前的提取失败
{
    // 这里来处理失败
    std::cin.clear(); // 将std::cin调回 '正常' 模式 
    ignoreLine();     // 移除缓存中的错误数据
}
```

让我们将其集成到getDouble()函数中:

```C++
double getDouble()
{
    while (true) // 无限循环，直到用户输入有效的数据
    {
        std::cout << "Enter a decimal number: ";
        double x{};
        std::cin >> x;

        if (!std::cin) // 是否之前的提取失败
        {
            // 这里来处理失败
            std::cin.clear(); // 将std::cin调回 '正常' 模式 
            ignoreLine();     // 移除缓存中的错误数据
        }
        else // 或者之前提取成功
        {
            ignoreLine();
            return x; // 这里返回提取的数据
        }
    }
}
```

由于无效输入而导致提取失败，将导致变量分配为值0。

在Unix系统上，输入文件尾（EOF）字符（键盘上输入ctrl-D）关闭输入流。这是std::cin.clear()无法修复的问题，此时std::cin永远不会离开故障模式，这会导致所有后续输入操作失败。这也会导致程序无限循环，直到被杀死。

要更优雅地处理这种情况，可以显式检查是否EOF:

```C++
        if (!std::cin) // 是否之前的提取失败
        {
            if (std::cin.eof()) // 是否输入流被关闭
            {
                exit(0); // 直接关闭程序
            }

            // 这里来处理失败
            std::cin.clear(); // 将std::cin调回 '正常' 模式 
            ignoreLine();     // 移除缓存中的错误数据
        }
```

{{< alert success >}}
**关键点**

一旦提取失败，未来的输入提取请求（包括对ignore()的调用）将静默失败，直到调用clear()函数。因此，在检测到失败的提取后，调用clear()通常是您应该做的第一件事。

{{< /alert >}}

***
## 错误情况4:输入提取成功，但输入数值发生了溢出

考虑下面的简单示例:

```C++
#include <cstdint>
#include <iostream>

int main()
{
    std::int16_t x{}; // x 是 16 位, 存储范围 -32768 到 32767
    std::cout << "Enter a number between -32768 and 32767: ";
    std::cin >> x;

    std::int16_t y{}; // y 是 16 位, 存储范围 -32768 到 32767
    std::cout << "Enter another number between -32768 and 32767: ";
    std::cin >> y;

    std::cout << "The sum is: " << x + y << '\n';
    return 0;
}
```

如果用户输入的数字太大（例如40000），会发生什么情况？

在上述情况下，std::cin会立即进入“故障模式”，但也会将范围内最接近的值分配给变量。因此，x的赋值为32767。这时会跳过其他输入，将y保留为初始化值0。可以用与处理提取失败相同的方法来处理这种错误。

***
## 把它们放在一起

下面是我们的示例中，更新了一些额外的错误检查:

```C++
#include <iostream>
#include <limits>

void ignoreLine()
{
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

double getDouble()
{
    while (true) // 无限循环，直到用户输入有效的数据
    {
        std::cout << "Enter a decimal number: ";
        double x{};
        std::cin >> x;

        // 检查是否提取失败
        if (!std::cin) // 提取失败的情况
        {
            if (std::cin.eof()) // 是否输入流被关闭
            {
                exit(0); // 直接关闭程序
            }

            // 这里来处理失败
            std::cin.clear(); // 将std::cin调回 '正常' 模式 
            ignoreLine();     // 移除缓存中的错误数据

            std::cout << "Oops, that input is invalid.  Please try again.\n";
        }
        else
        {
            ignoreLine(); // 移除任何额外的输入
            return x;
        }
    }
}

char getOperator()
{
    while (true) // 无限循环，直到用户输入有效的数据
    {
        std::cout << "Enter one of the following: +, -, *, or /: ";
        char operation{};
        std::cin >> operation;

        if (!std::cin) // 检查是否提取失败
        {
            if (std::cin.eof()) // 是否输入流被关闭
            {
                exit(0); // 直接关闭程序
            }

            // 这里来处理失败
            std::cin.clear(); // 将std::cin调回 '正常' 模式 
        }

        ignoreLine(); // 移除任何额外的输入

        // 检查输入是否在范围内
        switch (operation)
        {
        case '+':
        case '-':
        case '*':
        case '/':
            return operation; // 将输入返回
        default: // 告诉用户输入错误
            std::cout << "Oops, that input is invalid.  Please try again.\n";
        }
    }
}
 
void printResult(double x, char operation, double y)
{
    switch (operation)
    {
    case '+':
        std::cout << x << " + " << y << " is " << x + y << '\n';
        break;
    case '-':
        std::cout << x << " - " << y << " is " << x - y << '\n';
        break;
    case '*':
        std::cout << x << " * " << y << " is " << x * y << '\n';
        break;
    case '/':
        std::cout << x << " / " << y << " is " << x / y << '\n';
        break;
    default: // 即使getOperator()函数确保返回有效的输入，这里的检查可以让程序更加健壮
        std::cout << "Something went wrong: printResult() got an invalid operator.\n";
    }
}
 
int main()
{
    double x{ getDouble() };
    char operation{ getOperator() };
    double y{ getDouble() };
 
    printResult(x, operation, y);
 
    return 0;
}
```

***
## 结论

在编写程序时，请考虑用户将如何滥用您的程序，特别是在文本输入方面。对于每个文本输入点，请考虑:

1. 提取是否会失败？
2. 用户是否可以输入比预期更多的输入？
3. 用户是否可以输入无意义的输入？
4. 用户输入是否会溢出？


可以使用if语句和布尔逻辑来测试输入是否预期和有意义。

以下代码将清除任何无关的输入:

```C++
std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
```

以下代码将测试并修复失败的提取或溢出（并删除无关的输入）:

```C++
if (!std::cin) // 是否之前提出失败，或者发生了溢出
{
    if (std::cin.eof()) // 是否输入流关闭
    {
        exit(0); // 关闭程序
    }

    // 这里来处理故障
    std::cin.clear(); // 将std::cin调回 '正常' 模式 
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); // 移除缓存中的无关输入
}
```

我们可以测试是否存在未提取的输入（换行除外），如下所示:

```C++
        // 是否有额外的输入
        if (!std::cin.eof() && std::cin.peek() != '\n')
        {
            // 做我们想做的任何事情 -- 例如:
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); // 移除无关输入
            continue; // 返回循环的顶部，让用户重新输入
        }
```

最后，如果原始输入无效，则使用循环要求用户重新输入。

{{< alert success >}}
**注**

输入验证很重要，也很有用，但它也会使程序变得更复杂，更难理解。因此，在未来的课程中，通常不会进行任何类型的输入验证，除非它与试图教授的内容相关。

{{< /alert >}}

***
