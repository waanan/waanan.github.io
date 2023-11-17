---
title: "更多调试策略"
date: 2023-10-09T20:06:10+08:00
---

在上一课中，我们开始探索如何手动调试问题。在末尾，我们对使用语句打印调试文本提出了一些缺点：

1. 调试语句扰乱了代码
2. 调试语句扰乱了输出内容
3. 调试语句需要增加和移除代码，容易引入新的问题，
4. 在解决问题之后，需要移除调试代码，这些代码完全不可重用

本节所述技术可以缓解其中一些问题。

***
## 条件化调试代码

考虑以下包含一些调试语句的程序：

```C++
#include <iostream>
 
int getUserInput()
{
std::cerr << "getUserInput() called\n";
	std::cout << "Enter a number: ";
	int x{};
	std::cin >> x;
	return x;
}
 
int main()
{
std::cerr << "main() called\n";
    int x{ getUserInput() };
    std::cout << "You entered: " << x << '\n';
 
    return 0;
}
```

完成调试后，您要么需要删除它们，要么将它们注释掉。如果以后需要它们，则必须重新添加它们，或取消注释它们。

使用预处理指令，可以很容易的在整个程序中启用或禁用调试语句。

```C++
#include <iostream>
 
#define ENABLE_DEBUG // 注释掉这一行，可以禁用掉调试输出

int getUserInput()
{
#ifdef ENABLE_DEBUG
std::cerr << "getUserInput() called\n";
#endif
	std::cout << "Enter a number: ";
	int x{};
	std::cin >> x;
	return x;
}
 
int main()
{
#ifdef ENABLE_DEBUG
std::cerr << "main() called\n";
#endif
    int x{ getUserInput() };
    std::cout << "You entered: " << x << '\n';
 
    return 0;
}
```

现在，我们可以通过注释/取消注释 #define ENABLE_DEBUG 来启用或禁用调试语句。这允许我们重用以前添加的调试语句，然后在处理完后禁用它们，而不是从代码中实际删除它们。如果这是一个多文件程序，#define ENABLE_DEBUG 将放在头文件中，被所有用到的地方引用，方便我们可以在单个位置注释/取消注释#define，并将其传播到所有代码文件。

这解决了必须删除调试语句和删错代码的风险，但代价是代码更加混乱。这种方法的另一个缺点是，如果您输入错误（例如拼写错误的“DEBUG”）或忘记将头文件包含在代码文件中，则对应的文件就没有调试语句输出了。因此，尽管这比之前的版本更好，但仍有改进的余地。

***
## 使用日志记录器（Logger）

通过预处理器进行条件化调试的另一种方法是将调试信息发送到日志。日志是已发生事件的顺序记录，通常带有时间戳。生成日志的过程称为日志记录。通常，日志被写入磁盘上的文件（称为日志文件），以便稍后查看。大多数应用程序和操作系统都会将运行信息写入日志文件，可用于帮助诊断发生的问题。

日志文件有几个优点。由于写入日志文件的信息与程序的输出分离，因此可以避免混合正常输出和调试输出所导致的混乱。日志文件也可以很容易地发送给其他人进行诊断——因此，如果使用您的软件的人有问题，您可以要求他们向您发送日志文件，这可能有助于为您提供问题所在的线索。

C++包含一个名为std::clog的输出流，用于写入日志信息。然而，默认情况下，std::clog写入标准错误流（与std::cerr相同）。虽然您可以将其重定向到文件，但一个通常最好使用许多现有第三方日志库。

为了便于说明，我们将展示使用plog库。Plog被实现为一组头文件，因此很容易将其包含在您需要的任何位置，并且它是轻量级的，易于使用。

```C++
#include <plog/Log.h> // Step 1: 引用对应的头文件
#include <plog/Initializers/RollingFileInitializer.h>
#include <iostream>

int getUserInput()
{
	PLOGD << "getUserInput() called"; // PLOGD 在 plog 对应的头文件库中定义

	std::cout << "Enter a number: ";
	int x{};
	std::cin >> x;
	return x;
}

int main()
{
	plog::init(plog::debug, "Logfile.txt"); // Step 2: 初始化plog库，指定对应的输出文件

	PLOGD << "main() called"; // Step 3: 将所有需要记录的信息写入日志文件中

	int x{ getUserInput() };
	std::cout << "You entered: " << x << '\n';

	return 0;
}
```

以下是来自上述代码的输出（在Logfile.txt文件中）：

```C++
2018-12-26 20:03:33.295 DEBUG [4752] [main@14] main() called
2018-12-26 20:03:33.296 DEBUG [4752] [getUserInput@4] getUserInput() called
```

您如何引用、初始化和使用日志记录器将因您选择的库而异。

请注意，使用此方法也不需要条件编译指令，因为大多数记录器都有对应的方法来控制日志的写入输出。这使得代码更容易阅读，因为条件编译行增加了许多混乱。使用plog，可以通过将init语句更改为以下内容来临时禁用日志记录：

```C++
	plog::init(plog::none , "Logfile.txt"); // plog::none 关闭写入日志功能
```

我们在以后的课程中不会使用plog，因此您不需要担心学习它。

{{< alert success >}}
**旁白**

如果要自己编译上述示例，或在自己的项目中使用plog，可以按照以下说明进行安装：

首先，获取最新的plog版本：

1. 访问[plog repo](https://github.com/SergiusTheBest/plog)。 
2. 单击右上角的绿色Code按钮，然后选择“Download zip”

接下来，将整个存档解压缩到硬盘上的某个位置。

最后，对于对应的项目，将somewhere\plogmaster\include\目录设置为IDE中的包含目录。

{{< /alert >}}

{{< alert success >}}
**提示**

在较大或对性能敏感的项目中，可以首选速度更快、功能更丰富的记录器，例如[spdlog](https://github.com/gabime/spdlog)。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter3/debug-tatics/" next="/basic/chapter3/step/" >}}
3.3 基本调试策略
<--->
3.5 使用集成调试器：单步执行
{{< /prevnext >}}
