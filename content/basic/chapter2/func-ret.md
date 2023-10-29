---
title: "函数返回值"
date: 2023-10-09T20:06:10+08:00
---

考虑以下程序：

```C++
#include <iostream>

int main()
{
    // 让用户输入一个值
    std::cout << "Enter an integer: ";
    int num{};
    std::cin >> num;

    // 输入的值 * 2, 然后输出
    std::cout << num << " doubled is: " << num * 2 << '\n';

    return 0;
}
```

这个程序由两个部分组成：首先，我们从用户那里获得一个值。然后我们告诉用户该值的两倍是多少。

尽管这个程序非常琐碎，我们不需要将其分解为多个函数，但如果我们想这样做呢？从用户那里获得整数值是一个概念上完整的部分，因此它可以封装成一个函数。

因此，让我们编写一个程序来执行此操作：

```C++
// 这个程序不会产出预期的效果
#include <iostream>

void getValueFromUser()
{
    std::cout << "Enter an integer: ";
    int input{};
    std::cin >> input;  
}

int main()
{
    getValueFromUser(); // 让用户输入一个数字

    int num{}; // 如何将getValueFromUser函数中获取的值，放置到变量num中？

    std::cout << num << " doubled is: " << num * 2 << '\n';

    return 0;
}
```

虽然该程序是一个很好的尝试，但它并不满足我们的需求。

调用函数getValueFromUser时，将要求用户按预期输入整数。但当getValueFromUser执行结束并且返回main时，输入的值将丢失。变量num无法使用用户输入的值进行初始化，因此程序始终打印答案0。

我们缺少的是从getValueFromUser将用户输入的值返回给main的某种方法，以便main可以使用该数据。

***
## 返回值

编写用户定义函数时，函数可以将值返回给调用方。要将值返回给调用者，需要两件事。

首先，函数必须指示将返回的值类型。这是通过设置函数的返回类型来完成的，该类型是在函数名称之前定义的类型。在上面的示例中，函数getValueFromUser的返回类型为void（意味着不会向调用方返回任何值），函数main的返回类型是int（意味着将向调用者返回类型为int的值）。注意，这并不确定返回什么特定的值——它只确定将返回什么类型的值。

其次，在将返回值的函数内部，我们使用return语句来指示返回给调用方的特定值。从函数返回的特定值称为返回值。执行return语句时，函数立即退出，返回值从函数复制回调用方。这个过程称为按值返回。

让我们看一看返回整数值的简单函数，以及调用它的示例程序：

```C++
#include <iostream>

// 返回值类型是 int
// 这意味着调用该函数的调用者，会得到一个 int 类型的数据
int returnFive()
{
    // 使用return语句来返回数据
    return 5; // 这里返回的是值 5
}

int main()
{
    std::cout << returnFive() << '\n'; // 打印 5
    std::cout << returnFive() + 2 << '\n'; // 打印 7

    returnFive(); // 5被返回，但main函数没有其它任何处理

    return 0;
}
```

运行时，此程序打印：

```C++
5
7
```

执行从main的顶部开始。在第一条语句中，调用函数returnFive。函数returnFive将特定值 5 返回给调用者，然后通过std::cout将其打印到控制台。

在第二个函数调用中，函数 returnFive 再次被调用。函数returnFive将5的值返回给调用者。计算表达式5+2以产生结果7，然后通过std::cout将其打印到控制台。

在第三条语句中，再次调用函数returnFive，结果将值5返回给调用者。然而，函数main不处理返回值，因此不会进一步发生任何事情（返回值被忽略）。

注意：除非调用者通过std::cout将返回值发送到控制台，否则不会打印返回值。在上面的最后一个例子中，返回值不会发送到std::cout，因此不会打印任何内容。

{{< alert success >}}
**提示**

当被调用函数返回值时，调用者可以决定在表达式或语句中使用该值（例如，通过将其分配给变量，或将其发送到std::cout），或者忽略它（不执行其他操作）。

{{< /alert >}}

***
## 修复问题代码

现在我们可以修复我们在课程顶部演示的程序：

```C++
#include <iostream>

int getValueFromUser() // 本函数返回一个int值
{
     std::cout << "Enter an integer: ";
    int input{};
    std::cin >> input;  

    return input; // 将用户输入的值返回给调用函数
}

int main()
{
    int num { getValueFromUser() }; // 使用getValueFromUser()的结果初始化变量num

    std::cout << num << " doubled is: " << num * 2 << '\n';

    return 0;
}
```

当这个程序执行时，main中的第一条语句将创建一个名为num的int变量。当程序初始化num时，它将看到有一个对getValueFromUser()的函数调用，因此它将执行该函数。函数getValueFromUser要求用户输入一个值，然后将该值返回给调用者（main）。此返回值用作变量num的初始化值。

自己编译这个程序并运行几次，以证明它是有效的。

***
## 重新理解main()

对函数调用有了概念之后，让我门来理解main()函数的实际工作方式。当程序执行时，操作系统对main进行函数调用。然后执行跳到main的顶部。main中的语句按顺序执行。最后，main返回一个整数值（通常为0），程序终止。来自main的返回值有时称为状态代码（有时也称为退出代码，或称为返回代码），因为它用于指示程序是否成功运行。

根据定义，状态代码0表示程序成功执行。

非零状态代码通常用于指示故障（虽然这在大多数操作系统上都很好，但严格地说，它不能保证是可移植的）。

C++不允许显式调用main函数。

现在，您还应该在代码文件的底部，其他函数的下面定义main函数。

{{< alert success >}}
**最佳实践**

如果程序正常运行，则主函数应返回值0。

{{< /alert >}}

{{< alert success >}}
**对于高级读者**

C++标准仅定义3个状态代码的含义：0、EXIT_SUCCESS和EXIT_FAILURE。0和EXIT_SUCCESS都表示程序成功执行。EXIT_FAILURE表示程序未成功执行。

EXIT_SUCCESS和EXIT_FAILURE是在<cstdlib>头中定义的预处理器宏：

```C++
#include <cstdlib> // for EXIT_SUCCESS and EXIT_FAILURE

int main()
{
    return EXIT_SUCCESS;
}
```

如果要最大限度地提高可移植性，则应仅使用0或EXIT_SUCCESS表示成功终止，或使用EXIT_FAILURE表示不成功终止。

我们在预处理器简介小节中介绍预处理器和预处理器宏。

{{< /alert >}}

***
## 获取未返回值的函数的结果将产生未定义的行为

如果函数的返回类型不是void，但未使用return函数返回结果。调用该函数，获取的值将导致未定义的行为。

下面是一个产生未定义行为的函数的示例：

```C++
#include <iostream>

int getValueFromUserUB() // 返回一个int值
{
     std::cout << "Enter an integer: ";
    int input{};
    std::cin >> input;

    // note: 无return语句
}

int main()
{
    int num { getValueFromUserUB() }; // 使用 getValueFromUserUB() 的返回值初始化num

    std::cout << num << " doubled is: " << num * 2 << '\n';

    return 0;
}
```

现代编译器应该生成警告，因为getValueFromUserUB被定义为返回int，但没有提供返回语句。运行这样的程序将产生未定义的行为，因为getValueFromUserUB()是一个不返回值的可获取返回值的函数。

在大多数情况下，编译器将检测您是否忘记返回值。然而，在某些复杂的情况下，编译器可能无法在所有情况下正确检查函数是否返回值，因此不应依赖于此。

{{< alert success >}}
**最佳实践**

确保具有非void返回类型的函数在所有情况下都返回值。

{{< /alert >}}

***
## 如果未提供返回语句，函数main将隐式返回0

函数必须通过return语句返回值，这一规则的唯一例外是函数main()。如果没有提供return语句，函数main()将隐式返回值0。也就是说，最好的做法是显式地从main返回一个值，以显示您的意图，并与其他函数保持一致（如果未指定返回值，则会显示未定义的行为）。

***
## 函数只能返回单个值

函数每次被调用时只能将单个值返回给调用方。

注意，return语句中提供的值不需要是文本——它可以是任何有效表达式的结果，包括变量，甚至是对另一个函数的调用结果。在上面的getValueFromUser（）示例中，我们返回了一个变量，其中保存了用户输入的数字。

有各种方法可以解决函数只能返回单个值的限制，我们将在以后的课程中介绍这一点。

***
## 函数作者可以决定返回值的含义

函数返回的值的含义由函数的作者确定。一些函数使用返回值作为状态代码，以指示它们是成功的还是失败的。其他函数返回计算值或选定值。其他函数不返回任何内容（我们将在下一课中看到这些函数的示例）。

由于这里有各种各样的可能性，最好用注释来记录函数，说明返回值的含义。例如：

```C++
// 让用户输入数字
// 返回值是用户输入的数字
int getValueFromUser()
{
     std::cout << "Enter an integer: ";
    int input{};
    std::cin >> input;  

    return input;
}
```

***
## 重复使用函数

现在，我们可以说明函数重用的一个很好的例子。考虑以下程序：

```C++
#include <iostream>

int main()
{
    int x{};
    std::cout << "Enter an integer: ";
    std::cin >> x; 

    int y{};
    std::cout << "Enter an integer: ";
    std::cin >> y; 

    std::cout << x << " + " << y << " = " << x + y << '\n';

    return 0;
}
```

虽然这个程序可以工作，但它有点冗余。事实上，这个程序违反了良好编程的核心原则之一：不要重复自己（通常缩写为DRY）。

为什么重复的代码是坏的？如果我们想将文本“Enter an integer:”更改为其他内容，我们必须在两个位置更新它。如果我们想初始化10个变量，而不是2个，那会怎么样？这将是大量冗余代码（使我们的程序更长、更难理解），并且有很大的空间让打字错误蔓延进来。

让我们更新此程序，以使用上面开发的getValueFromUser函数：

```C++
#include <iostream>

int getValueFromUser()
{
     std::cout << "Enter an integer: ";
    int input{};
    std::cin >> input;  

    return input;
}

int main()
{
    int x{ getValueFromUser() };
    int y{ getValueFromUser() };

    std::cout << x << " + " << y << " = " << x + y << '\n';

    return 0;
}
```

该程序产生以下输出：

```C++
Enter an integer: 5
Enter an integer: 7
5 + 7 = 12
```

在该程序中，我们调用getValueFromUser两次，一次初始化变量x，一次初始变量y。这避免了我们重复代码以获取用户输入，并降低了出错的几率。一旦我们知道getValueFromUser工作正常，我们可以根据需要多次调用它。

这是模块化编程的本质：编写函数、测试它、确保它工作正常，然后可以根据需要多次重用它。

{{< alert success >}}
**最佳实践**

遵循DRY（Don’t Repeat Yourself）最佳实践：“不要重复自己”。如果您需要多次执行某些操作，请考虑如何修改代码以尽可能地删除冗余。变量可以用于存储需要多次使用的计算结果（因此我们不必重复计算）。函数可以用于定义要多次执行的语句序列。循环（我们将在后面的章节中介绍）可以用于多次执行语句。

{{< /alert >}}

{{< alert success >}}
**旁白…**

DRY的反义词是WET（“将所有内容写入两次”，“Write everything twice”）。

{{< /alert >}}

***
## 总结

返回值为函数提供了一种将单个值返回给函数调用方的方法。

函数提供了一种最小化程序冗余的方法。

***

{{< prevnext prev="/basic/chapter2/intro-func/" next="/basic/chapter2/func-ret-void/" >}}
2.0 函数简介
<--->
2.2 无返回值函数
{{< /prevnext >}}
