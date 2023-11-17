---
title: "基本调试策略"
date: 2023-10-09T20:06:10+08:00
---

在上一课中，我们探索了一种查找问题的策略,通过运行程序并使用猜测来了解问题所在。在本课程中，我们将探索一些其它基本策略，用于实际进行这些猜测，并收集信息以帮助查找问题。

***
## 调试策略#1：注释代码

让我们从一个简单的程序开始。如果程序表现出错误的行为，减少必须搜索的代码量的一种方法是注释掉一些代码，并查看问题是否仍然存在。如果问题保持不变，则注释掉的代码则可能不是导致问题的原因。

考虑以下代码：

```C++
int main()
{
    getNames(); // 让用户输入一些名称
    doMaintenance(); // 做一下其他事情
    sortNames(); // 排序名称
    printNames(); // 打印排序后的名称

    return 0;
}
```

假设这个程序应该按顺序打印用户输入的名称，但它按顺序打印。问题出在哪里？getNames输入的名称是否不正确？sortNames是否排序正确？printNames是否正常打印它们？它可能是任何一种原因。但我们可能怀疑doMaintenance() 与该问题无关，所以让我们将其注释掉。

```C++
int main()
{
    getNames(); // 让用户输入一些名称
//    doMaintenance(); // 做一下其他事情
    sortNames(); // 排序名称
    printNames(); // 打印排序后的名称

    return 0;
}
```

有三种可能的结果：

1. 如果问题消失了，那么doMaintenance一定是问题的根源，我们应该将注意力集中在那里。
2. 如果问题没有改变（这更可能），那么我们可以合理地假设doMaintenance没有错，并且我们现在可以从排查中排除整个函数。这不能帮助我们理解实际的问题是在调用doMaintenance之前还是之后，但它减少了我们必须随后检查的代码量。
3. 如果注释掉doMaintenance导致问题演变为其他相关问题（例如，程序停止打印名称），则doMaintenance很可能正在做一些其他代码依赖的有用的事情。在这种情况下，我们可能无法判断问题是在doMainternance中还是在其他地方，因此我们可以取消注释doMaintentenance并尝试其他方法。


{{< alert success >}}
**警告**

不要忘记您注释掉了哪些函数，以便以后可以取消注释它们！

在进行了许多与调试相关的更改之后，很容易忽略撤消一个或两个。如果发生这种情况，最终将修复一个错误，但引入其他错误！

在这里，拥有一个好的版本控制系统是非常有用的，因为您可以将代码与主分支进行比较，以查看所有与调试相关的更改（并确保在提交更改之前还原它们）。

{{< /alert >}}

***
## 调试策略#2:验证代码流程

在更复杂的程序中，另一个常见的问题是程序调用函数的次数太多或太少（包括根本不调用）。

在这种情况下，将语句放在函数的顶部来打印函数的名称可能会很有帮助。这样，当程序运行时，您可以看到调用了哪些函数。

请考虑以下无法正常工作的简单程序：

```C++
#include <iostream>

int getValue()
{
	return 4;
}

int main()
{
    std::cout << getValue << '\n';

    return 0;
}
```

您可能需要禁用“将警告视为错误”，才能编译以上内容。

尽管我们希望该程序打印值4，但它可能打印值：

```C++
1
```

在Visual Studio（可能还有其他一些编译器）上，它可能会打印以下内容：

```C++
00101424
```

让我们为这些函数添加一些调试语句：

```C++
#include <iostream>

int getValue()
{
std::cerr << "getValue() called\n";
	return 4;
}

int main()
{
std::cerr << "main() called\n";
    std::cout << getValue << '\n';

    return 0;
}
```

现在，当这些函数执行时，它们将输出它们的名称，表示它们被调用：

```C++
main() called
1
```

现在我们可以看到函数getValue从未被调用。调用函数的代码一定有问题。让我们仔细看看这一行：

```C++
    std::cout << getValue << '\n';
```

哦，看，我们在函数调用中忘记了括号。它应该是：

```C++
#include <iostream>

int getValue()
{
std::cerr << "getValue() called\n";
	return 4;
}

int main()
{
std::cerr << "main() called\n";
    std::cout << getValue() << '\n'; // 添加括号

    return 0;
}
```

这时产生正确的输出

```C++
main() called
getValue() called
4
```

这时我们可以删除临时调试语句。

{{< alert success >}}
**提示**

打印用于调试的信息时，请使用std::cerr而不是std:∶cout。这样做的一个原因是，std::cout可能有缓冲区，这意味着在请求std:∶cout输出信息和它实际输出信息之间可能会有停顿。如果您使用std::cout输出，然后您的程序随后立即崩溃，则std::cout可能还没有实际输出。这可能会误导您定位问题的位置。另一方面，std::cerr没有缓冲，这意味着您发送给它的任何内容都将立即输出。这有助于确保所有调试输出尽快出现（以某些性能为代价，这在调试时通常不关心）。

使用std::cerr还有助于明确输出的信息用于错误情况，而不是正常情况。

在后续 检测和处理错误 章节中，我们进一步讨论了何时使用std::cout 或 std::cerr。

{{< /alert >}}

{{< alert success >}}
**相关内容**

在 函数指针 章节中，我们讨论了为什么某些编译器打印1而不是函数地址（以及如果编译器打印1但您希望它打印地址时该怎么办）。

{{< /alert >}}

{{< alert success >}}
**提示**

添加临时调试语句时，不缩进它们可能会有所帮助。这使得它们更容易找到，以便以后删除。

如果您使用clang格式来格式化代码，它将尝试自动缩进这些行。您可以这样抑制自动格式：

```C++
// clang-format off
std::cerr << "main() called\n";
// clang-format on
```

{{< /alert >}}

***
## 调试策略#3:打印值

对于某些类型的错误，程序可能在计算或传递错误的值。

我们还可以输出变量（包括参数）或表达式的值，以检查它们是是否正确。

考虑以下程序，该程序应将两个数字相加，但不能正常工作：

```C++
#include <iostream>

int add(int x, int y)
{
	return x + y;
}

void printResult(int z)
{
	std::cout << "The answer is: " << z << '\n';
}

int getUserInput()
{
	std::cout << "Enter a number: ";
	int x{};
	std::cin >> x;
	return x;
}

int main()
{
	int x{ getUserInput() };
	int y{ getUserInput() };

	std::cout << x << " + " << y << '\n';

	int z{ add(x, 5) };
	printResult(z);

	return 0;
}
```

下面是该程序的一些输出：

```C++
Enter a number: 4
Enter a number: 3
4 + 3
The answer is: 9
```

你发现错误了吗？即使在这个简短的程序中，它也很难被发现。让我们添加一些代码来调试变量的值：

```C++
#include <iostream>

int add(int x, int y)
{
	return x + y;
}

void printResult(int z)
{
	std::cout << "The answer is: " << z << '\n';
}

int getUserInput()
{
	std::cout << "Enter a number: ";
	int x{};
	std::cin >> x;
	return x;
}

int main()
{
	int x{ getUserInput() };
std::cerr << "main::x = " << x << '\n';
	int y{ getUserInput() };
std::cerr << "main::y = " << y << '\n';

	std::cout << x << " + " << y << '\n';

	int z{ add(x, 5) };
std::cerr << "main::z = " << z << '\n';
	printResult(z);

	return 0;
}
```

下面是对应的输出：

```C++
Enter a number: 4
main::x = 4
Enter a number: 3
main::y = 3
4 + 3
main::z = 9
The answer is: 9
```

变量x和y获得了正确的值，但变量z没有。问题必须在这两点之间，这使得函数add()成为关键问题所在。

让我们修改函数add：

```C++
#include <iostream>

int add(int x, int y)
{
std::cerr << "add() called (x=" << x <<", y=" << y << ")\n";
	return x + y;
}

void printResult(int z)
{
	std::cout << "The answer is: " << z << '\n';
}

int getUserInput()
{
	std::cout << "Enter a number: ";
	int x{};
	std::cin >> x;
	return x;
}

int main()
{
	int x{ getUserInput() };
std::cerr << "main::x = " << x << '\n';
	int y{ getUserInput() };
std::cerr << "main::y = " << y << '\n';

	std::cout << x << " + " << y << '\n';

	int z{ add(x, 5) };
std::cerr << "main::z = " << z << '\n';
	printResult(z);

	return 0;
}
```

现在，我们将获得输出：

```C++
Enter a number: 4
main::x = 4
Enter a number: 3
main::y = 3
add() called (x=4, y=5)
main::z = 9
The answer is: 9
```

变量y的值为3，但我们的函数add不知何故获得了参数y的值5。我们一定传递了错误的参数。果然：

```C++
	int z{ add(x, 5) };
```

就是这样。我们传递了文本5，而不是变量y的值作为参数。这很简单就可修复，然后我们可以删除调试语句。

***
## 再举一个例子

该程序与前一个程序非常相似，但也不能正常工作：

```C++
#include <iostream>

int add(int x, int y)
{
	return x + y;
}

void printResult(int z)
{
	std::cout << "The answer is: " << z << '\n';
}

int getUserInput()
{
	std::cout << "Enter a number: ";
	int x{};
	std::cin >> x;
	return --x;
}

int main()
{
	int x{ getUserInput() };
	int y{ getUserInput() };

	int z { add(x, y) };
	printResult(z);

	return 0;
}
```

如果运行此代码并看到以下内容：

```C++
Enter a number: 4
Enter a number: 3
The answer is: 5
```

嗯，有点不对劲。但在哪里呢？

让我们对该代码进行一些调试：

```C++
#include <iostream>

int add(int x, int y)
{
std::cerr << "add() called (x=" << x << ", y=" << y << ")\n";
	return x + y;
}

void printResult(int z)
{
std::cerr << "printResult() called (z=" << z << ")\n";
	std::cout << "The answer is: " << z << '\n';
}

int getUserInput()
{
std::cerr << "getUserInput() called\n";
	std::cout << "Enter a number: ";
	int x{};
	std::cin >> x;
	return --x;
}

int main()
{
std::cerr << "main() called\n";
	int x{ getUserInput() };
std::cerr << "main::x = " << x << '\n';
	int y{ getUserInput() };
std::cerr << "main::y = " << y << '\n';

	int z{ add(x, y) };
std::cerr << "main::z = " << z << '\n';
	printResult(z);

	return 0;
}
```

现在，让我们使用相同的输入再次运行该程序：

```C++
main() called
getUserInput() called
Enter a number: 4
main::x = 3
getUserInput() called
Enter a number: 3
main::y = 2
add() called (x=3, y=2)
main::z = 5
printResult() called (z=5)
The answer is: 5
```

现在，我们可以立即看到出现了问题：用户正在输入值4，但main的x得到的是值3。在用户输入的位置和将该值分配给main的变量x的位置之间，肯定出现了问题。让我们通过向函数getUserInput添加一些调试代码来确保程序从用户处获得正确的值：

```C++
#include <iostream>

int add(int x, int y)
{
std::cerr << "add() called (x=" << x << ", y=" << y << ")\n";
	return x + y;
}

void printResult(int z)
{
std::cerr << "printResult() called (z=" << z << ")\n";
	std::cout << "The answer is: " << z << '\n';
}

int getUserInput()
{
std::cerr << "getUserInput() called\n";
	std::cout << "Enter a number: ";
	int x{};
	std::cin >> x;
std::cerr << "getUserInput::x = " << x << '\n'; // 添加额外的这一行来做调试
	return --x;
}

int main()
{
std::cerr << "main() called\n";
	int x{ getUserInput() };
std::cerr << "main::x = " << x << '\n';
	int y{ getUserInput() };
std::cerr << "main::y = " << y << '\n';

	int z{ add(x, y) };
std::cerr << "main::z = " << z << '\n';
	printResult(z);

	return 0;
}
```

输出：

```C++
main() called
getUserInput() called
Enter a number: 4
getUserInput::x = 4
main::x = 3
getUserInput() called
Enter a number: 3
getUserInput::x = 3
main::y = 2
add() called (x=3, y=2)
main::z = 5
printResult() called (z=5)
The answer is: 5
```

通过这一额外的调试行，我们可以看到用户输入被正确地接收到getUserInput的变量x中。然而，main的变量x得到了错误的值。问题一定在这两点之间。唯一的罪魁祸首是函数getUserInput的返回值。让我们更仔细地看一下那一行。

```C++
	return --x;
```

嗯，这很奇怪。那是什么--x之前的符号？我们还没有在这些教程中介绍这一点，所以如果您不知道它的含义，请不要担心。但即使不知道它意味着什么，通过调试工作，您也可以合理地确定这行代码有问题——因此，很可能是这个“——”符号导致了问题。

由于我们确实希望getUserInput仅返回x的值，因此让我们删除“--”并查看发生了什么：

```C++
#include <iostream>

int add(int x, int y)
{
std::cerr << "add() called (x=" << x << ", y=" << y << ")\n";
	return x + y;
}

void printResult(int z)
{
std::cerr << "printResult() called (z=" << z << ")\n";
	std::cout << "The answer is: " << z << '\n';
}

int getUserInput()
{
std::cerr << "getUserInput() called\n";
	std::cout << "Enter a number: ";
	int x{};
	std::cin >> x;
std::cerr << "getUserInput::x = " << x << '\n';
	return x; // 移除变量x前的“--”
}

int main()
{
std::cerr << "main() called\n";
	int x{ getUserInput() };
std::cerr << "main::x = " << x << '\n';
	int y{ getUserInput() };
std::cerr << "main::y = " << y << '\n';

	int z{ add(x, y) };
std::cerr << "main::z = " << z << '\n';
	printResult(z);

	return 0;
}
```

现在输出：

```C++
main() called
getUserInput() called
Enter a number: 4
getUserInput::x = 4
main::x = 4
getUserInput() called
Enter a number: 3
getUserInput::x = 3
main::y = 3
add() called (x=4, y=3)
main::z = 7
printResult() called (z=7)
The answer is: 7
```

程序现在正常工作。即使不了解“--”的含义，我们也能够识别导致问题的特定代码行，然后修复问题。

***
## 为什么使用打印语句进行调试不太好

虽然为诊断目的向程序中添加调试语句是一种常见的基本技术，也是一种功能性技术（特别是当调试器由于某种原因不可用时），但由于以下几个原因，它并不是那么好：

1. 调试语句扰乱了代码
2. 调试语句扰乱了输出内容
3. 调试语句需要增加和移除代码，容易引入新的问题，
4. 在解决问题之后，需要移除调试代码，这些代码完全不可重用

我们可以做得更好。我们将在以后的课程中探索如何。

***

{{< prevnext prev="/basic/chapter3/debug-strategy/" next="/basic/chapter3/more-tatics/" >}}
3.2 调试策略
<--->
3.4 更多调试策略
{{< /prevnext >}}
