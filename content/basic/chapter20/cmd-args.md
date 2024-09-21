---
title: "命令行参数"
date: 2024-08-20T10:49:32+08:00
---

## 为什么需要命令行参数？

当编译和链接程序时，输出是一个可执行文件。当程序运行时，执行从名为main()的函数的顶部开始。到目前为止，我们这样声明main：

```C++
int main()
```

请注意，这个版本的main()不带参数。然而，许多程序需要某种类型的输入来使用。例如，假设您正在编写一个名为Thumbnail的程序，该程序读取图像文件，然后生成缩略图（图像的较小版本）。如何知道要处理的是哪张图片？用户必须有某种方法来告诉程序要打开哪个文件。为此，可以采用以下方法：

```C++
// Program: Thumbnail
#include <iostream>
#include <string>

int main()
{
    std::cout << "Please enter an image filename to create a thumbnail for: ";
    std::string filename{};
    std::cin >> filename;

    // 打开图片
    // 生成缩略图
    // 输出缩略图
}
```

然而，这种方法存在一个潜在的问题。每次运行程序时，程序将等待用户输入。如果您从命令行手动运行此程序一次，则这可能不是问题。但在其他情况下，这是有问题的，例如当您想要在许多文件上运行该程序，或者让另一个程序运行该程序时。

让我们进一步研究这些情况。

考虑您希望为给定目录中的所有图像文件创建缩略图的情况。你会怎么做？只要目录中有图像，就可以多次运行该程序，并手动输入每个文件名。然而，如果有数百张图像，这可能需要输入一整天！这里的一个好的解决方案是编写一个程序，循环遍历目录中的每个文件名，为每个文件调用一次Thumbnail。

现在考虑这样的情况，您正在运行一个网站，并且您希望每次用户将图像上传到您的网站时，您的网站都创建一个缩略图。上述创建缩略图的程序无法从用户的请求中获取输入图片，因此在这种情况下，上传程序如何输入文件名？这里的一个好的解决方案是让您的web服务器在上传后自动调用生成缩略图的程序。

在这两种情况下，需要一种方法，让外部程序在启动生成缩略图程序时将文件名作为输入传入，而不是在启动后等待用户输入文件名。

命令行参数是可选的字符串参数，在程序启动时由操作系统传递给程序。然后，程序可以将它们用作输入（或忽略它们）。就像函数参数是函数的输入一样，命令行参数为程序提供了向程序提供输入的方式。

***
## 传递命令行参数

在命令中，可以直接通过程序名来执行程序。例如，要运行位于Windows机器的当前目录中的可执行文件“WordCount”，可以输入：

```C++
WordCount
```

基于Unix的操作系统上的等效命令是：

```C++
./WordCount
```

为了将命令行参数传递给WordCount，我们只需在可执行文件名后列出命令行参数：

```C++
WordCount Myfile.txt
```

现在，当执行WordCount时，Myfile.txt将作为命令行参数提供。程序可以有多个命令行参数，由空格分隔：

```C++
WordCount Myfile.txt Myotherfile.txt
```

如果从IDE运行程序，也有输入命令行参数的方法。

在Microsoft Visual Studio中，在解决方案资源管理器中右键单击项目，然后选择属性。打开“配置属性”页面，然后选择“调试”。在右侧窗格中，有一行名为“命令参数”。您可以在那里输入命令行参数进行测试，当您运行程序时，它们将自动传递给您的程序。

***
## 使用命令行参数

现在您已经知道如何为程序提供命令行参数，下一步是从C++程序中访问它们。为此，我们使用了与以前不同的main()形式。这种新形式的main()采用两个参数（按照约定命名为argc和argv），如下所示：

```C++
int main(int argc, char* argv[])
```

您有时还会看到它被编写为：

```C++
int main(int argc, char** argv)
```

尽管这些是相同的，但我们更喜欢第一种表示，因为它在直觉上更容易理解。

argc是一个整数参数，代表传递给程序的参数数量的个数（argc=参数个数）。argc至少为1，因为第一个参数始终是程序本身的名称。用户提供的每个命令行参数都将导致argc增加1。

argv是存储实际参数值的位置（argv=参数值）。尽管argv的声明看起来很吓人，但argv实际上只是一个C风格的字符指针数组（每个指针都指向C风格的字符串）。此数组的长度为argc。

让我们编写一个名为“MyArgs”的短小程序来打印所有命令行参数的值：

```C++
// Program: MyArgs
#include <iostream>

int main(int argc, char* argv[])
{
    std::cout << "There are " << argc << " arguments:\n";

    // 遍历每个命令行参数并进行打印
    for (int count{ 0 }; count < argc; ++count)
    {
        std::cout << count << ' ' << argv[count] << '\n';
    }

    return 0;
}
```

现在，当我们使用命令行参数“Myfile.txt”和“100”调用该程序（MyArgs）时，输出如下：

```C++
There are 3 arguments:
0 C:\MyArgs
1 Myfile.txt
2 100
```

参数0是正在运行的当前程序的路径和名称。在本例中，参数1和2是我们传入的两个命令行参数。

请注意，我们不能使用基于范围的for循环来迭代argv，因为基于范围的for循环不适用于退化的C样式数组。

***
## 处理数值参数

命令行参数始终作为字符串传递，即使提供的值本质上是数字。要将命令行参数用作数字，必须将其从字符串转换为数字。不幸的是，C++这一点上比预期的要困难一些。

执行此操作的C++方法如下：

```C++
#include <iostream>
#include <sstream> // for std::stringstream
#include <string>

int main(int argc, char* argv[])
{
	if (argc <= 1)
	{
		// 在某些操作系统上, argv[0] 可能是空字符串而不是程序名
		// 这里进行判断
		if (argv[0])
			std::cout << "Usage: " << argv[0] << " <number>" << '\n';
		else
			std::cout << "Usage: <program name> <number>" << '\n';
            
		return 1;
	}

	std::stringstream convert{ argv[1] }; // 将参数 argv[1] 放入stringstream中，以方便进行转换

	int myint{};
	if (!(convert >> myint)) // 进行转换
		myint = 0; // 如果转换失败，设置为默认值

	std::cout << "Got integer: " << myint << '\n';

	return 0;
}
```

当以输入“567”运行时，该程序打印：

```C++
Got integer: 567
```

stringstream的工作原理与std::cin非常相似。在这种情况下，我们使用argv[1]的值对其进行初始化，以便可以使用操作符>>将值提取为整数变量（与使用std::cin相同）。

在以后的一章中，我们将更多地讨论std::stringstream。

***
## 操作系统会预处理命令行参数

在命令行中键入内容（或从IDE运行程序）时，操作系统负责根据需要转换和路由该请求。这不仅涉及运行可执行文件，还涉及解析的任何参数，以确定如何处理这些参数并将其传递给应用程序。

通常，操作系统有处理双引号和反斜杠等特殊字符的特殊规则。

例如：

```C++
MyArgs Hello world!
```

打印：

```C++
There are 3 arguments:
0 C:\MyArgs
1 Hello
2 world!
```

通常，以双引号传递的字符串被认为是同一字符串的一部分：

```C++
MyArgs "Hello world!"
```

打印：

```C++
There are 2 arguments:
0 C:\MyArgs
1 Hello world!
```

大多数操作系统都允许您通过反斜杠加双引号来传递原始的双引号：

```C++
yArgs \"Hello world!\"
```

打印：

```C++
There are 3 arguments:
0 C:\MyArgs
1 "Hello
2 world!"
```

其他字符也可能需要反斜杠转义，这取决于您的操作系统如何解释它们。


***
## 结论

命令行参数为用户提供了一种很好的方法，可以让程序在启动时将输入数据传递到程序中。当然在程序中，也需要对传入的参数的有效性进行判定。

***
