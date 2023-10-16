---
title: "空白字符与代码样式"
date: 2023-10-09T20:06:10+08:00
---

空白字符用于格式化目的。在C++中，这主要指空格、制表符和换行符。C++中的空白通常用于3件事：代码元素分隔、字符文本中的分隔，和格式化代码。

***
## 语言元素必须用空白字符分隔

C++的语法要求某些元素由空格分隔。通常在两个关键字或标识符连续放置时，达到互相区分的目的。

例如，变量声明必须有分隔：

```C++
int x; // int 和 x 之前必须分隔开
```

如果我们改为键入intx，编译器会将其解释为标识符，然后不知道intx是什么标识符。

另一个例子，函数的返回类型和名称必须分隔：

```C++
int main(); // int 和 main 之前必须分隔开
```

当需要空白作为分隔符时，编译器不关心使用了多少空白。

以下变量定义都有效：

```C++
int x;
int                y;
            int 
z;
```

在某些情况下，换行用作分隔符。比如单行注释由换行符终止。

例如，下面这样写就是有问题的：

```C++
std::cout << "Hello world!"; // 这是注释的一部分
这不是注释的一部分
```

预处理器指令（例如#include<iostream>）也必须放在单独的行上：

```C++
#include <iostream>
#include <string>
```

***
## 字符串中的空白字符

在字符串中，空白字符的也算作有效的字符。

```C++
std::cout << "Hello world!";
```

不同于：

```C++
std::cout << "Hello          world!";
```

字符串不允许中间直接换行：

```C++
std::cout << "Hello
     world!"; // 错误
```

由空白（空格、制表符或换行符）分隔的字符串将被连接：

```C++
std::cout << "Hello "
     "world!"; // prints "Hello world!"
```

***
## 使用空白来格式化代码

空白通常被忽略。这意味着我们可以在任何地方使用空白来格式化代码，以使其更易于阅读。

例如，以下代码很难阅读：

```C++
#include <iostream>
int main(){std::cout<<"Hello world";return 0;}
```

以下是更好的版本（但仍然相当密集）：

```C++
#include <iostream>
int main() {
std::cout << "Hello world";
return 0;
}
```

以下代码更好：

```C++
#include <iostream>

int main()
{
    std::cout << "Hello world";

    return 0;
}
```

如果需要，语句可以拆分为多行：

```C++
#include <iostream>

int main()
{
    std::cout
        << "Hello world";
    return 0;
}
```

这对于特别长的语句很有用。

***
## 代码样式

与其他一些语言不同，C++不会对程序员实施任何类型的代码样式限制。因此，C++是一种与空白无关的语言。

这是一个喜忧参半的事情。一方面，有自由做你想做的事很好。另一方面，多年来开发了许多不同的C++程序格式化方法，您会发现在哪种方法最好上存在分歧。这里基本经验法则是，最好的样式是生成最可读的代码并提供最一致性的样式。

下面是我们对基本代码样式的建议：

无论哪种方式，建议您将制表符设置为4个空格的缩进值。

Google C++风格指南建议将开头的花括号放在与语句相同的行上：

```C++
int main() {
}
```

这样做的理由是，它减少了垂直空白的量，因此您可以在屏幕上容纳更多的代码。屏幕上的更多代码使程序更容易理解。

然而，我们更喜欢常用的替代方案，其中左大括号出现在自己单独的行上：

```C++
int main()
{
}
```

这增强了可读性，并且不太容易出错，因为大括号始终缩进到相同的级别。如果由于大括号不匹配而出现编译器错误，则很容易看到错误的位置。

```C++
int main()
{
    std::cout << "Hello world!\n"; // tabbed in one tab (4 spaces)
    std::cout << "Nice to meet you.\n"; // tabbed in one tab (4 spaces)
}
```

```C++
int main()
{
    std::cout << "This is a really, really, really, really, really, really, really, " 
        "really long line\n"; // one extra indentation for continuation line

    std::cout << "This is another really, really, really, really, really, really, really, "
                 "really long line\n"; // text aligned with the previous line for continuation line

    std::cout << "This one is short\n";
}
```

这使得你的台词更容易阅读。在现代宽屏显示器上，它还允许您并排放置两个具有类似代码的窗口，并更容易地进行比较。

```C++
    std::cout << 3 + 4
        + 5 + 6
        * 7 * 8;
```

这有助于明确后续行是前一行的延续，并允许您对齐左侧的操作符，这使得阅读更容易。

更难阅读：

```C++
cost = 57;
pricePerItem = 24;
value = 5;
numberOfItems = 17;
```

更易于阅读：

```C++
cost          = 57;
pricePerItem  = 24;
value         = 5;
numberOfItems = 17;
```

更难阅读：

```C++
std::cout << "Hello world!\n"; // cout lives in the iostream library
std::cout << "It is very nice to meet you!\n"; // these comments make the code hard to read
std::cout << "Yeah!\n"; // especially when lines are different lengths
```

更易于阅读：

```C++
std::cout << "Hello world!\n";                  // cout lives in the iostream library
std::cout << "It is very nice to meet you!\n";  // these comments are easier to read
std::cout << "Yeah!\n";                         // especially when all lined up
```

更难阅读：

```C++
// cout lives in the iostream library
std::cout << "Hello world!\n";
// these comments make the code hard to read
std::cout << "It is very nice to meet you!\n";
// especially when all bunched together
std::cout << "Yeah!\n";
```

更易于阅读：

```C++
// cout lives in the iostream library
std::cout << "Hello world!\n";

// these comments are easier to read
std::cout << "It is very nice to meet you!\n";

// when separated by whitespace
std::cout << "Yeah!\n";
```

在本教程中，我们将遵循这些约定，它们将成为您的第二天性。当我们向您介绍新主题时，我们将介绍与这些功能配套的新样式建议。

最终，C++为您提供了选择最舒适的风格或认为最好的风格的能力。然而，我们强烈建议您使用我们在示例中使用的相同样式。它已经被数千名程序员在数十亿行代码上进行了战斗测试，并为成功而优化。

一个例外：如果您在其他人的代码库中工作，请采用他们的样式。与其偏好，不如偏好一致性。

{{< alert success >}}
**最佳做法**

考虑将行的长度保持在80个字符或更少。

{{< /alert >}}

{{< alert success >}}
**提示**

许多编辑器都有一个内置功能（或插件/扩展），它将在给定的列（例如，在80个字符处）显示一行（称为“列指南”），因此您可以很容易地看到您的行何时变得太长。要查看编辑器是否支持此功能，请搜索编辑器的名称+“列指南”。

{{< /alert >}}

{{< alert success >}}
**最佳做法**

在现有项目中工作时，与已经采用的任何样式保持一致。

{{< /alert >}}

***
## 自动设置格式

大多数现代IDE将帮助您在键入代码时格式化代码（例如，当您创建函数时，IDE将自动缩进函数体中的语句）。

然而，当您添加或删除代码，或更改IDE的默认格式，或粘贴具有不同格式的代码块时，格式可能会变得混乱。修复文件的部分或全部格式可能是一个头痛的问题。幸运的是，现代IDE通常包含自动格式化功能，该功能将重新格式化选择（用鼠标突出显示）或整个文件。

为了更容易访问，建议添加键盘快捷方式以自动格式化活动文件。

还有一些外部工具可以用于自动格式化代码。clang格式是一种流行的格式。

{{< alert success >}}
**对于Visual Studio用户**

在Visual Studio中，可以在编辑>高级>设置文档格式和编辑>高级>Format Selection下找到自动格式选项。

{{< /alert >}}

{{< alert success >}}
**对于代码：：阻止用户**

在代码：：块中，可以在鼠标右键单击>格式使用AStyle下找到自动格式选项。

{{< /alert >}}

{{< alert success >}}
**最佳做法**

强烈建议使用自动格式功能，以保持代码的格式样式一致。

{{< /alert >}}

