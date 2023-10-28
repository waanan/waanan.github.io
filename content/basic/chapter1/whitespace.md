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

1. 使用Tab或空格进行缩进都是可以的（大多数IDE都有一个设置，可以将制表符转换为适当数量的空格）。有些人喜欢空格，因为它使格式具有自我描述性——无论编辑器如何，使用空格分隔的代码看起来总是正确的。Tab的支持者，认为Tab是为缩进而设计的字符，尤其是因为你可以将Tab的展示宽度设置为你喜欢的任何宽度。这里没有正确的答案，争论它就像争论蛋糕还是馅饼更好。归根结底，这取决于个人喜好。

无论哪种方式，建议您将制表符设置为4个空格的缩进值。

2. 有两种函数开头的花括号的放置方式。

Google C++风格指南建议将开头的花括号放在与语句相同的行上：

```C++
int main() {
}
```

这样做的理由是，它使代码段落更加紧凑，因此您可以在屏幕上容纳更多的代码。屏幕上的更多代码使程序更容易理解。

然而，我们更喜欢常用的替代方案是，其中左大括号出现在自己单独的行上：

```C++
int main()
{
}
```

这增强了可读性，并且不太容易出错，因为大括号始终缩进到相同的级别。如果由于大括号不匹配而出现编译器错误，则很容易看到错误的位置。

3. 每个语句，在它属于的大括号的层级中，以tab或者4个空格开头。

```C++
int main()
{
    std::cout << "Hello world!\n"; // tabbed in one tab (4 spaces)
    std::cout << "Nice to meet you.\n"; // tabbed in one tab (4 spaces)
}
```

4. 每一行不应该太长，通常的限制是80个字符（包含空格）。如果屏幕比较大，一般也可以放宽到120个字符。
如果语句超长，需要在合适的节点换行。换行后相比原语句，前置额外的tab或4个空格缩进。
或者换行后的元素和前一行相同类型的元素对齐亦可。

```C++
int main()
{
    std::cout << "This is a really, really, really, really, really, really, really, " 
        "really long line\n"; // 换行后增加缩进

    std::cout << "This is another really, really, really, really, really, really, really, "
                 "really long line\n"; // 换行后按相同元素对齐

    std::cout << "This one is short\n";
}
```

5. 如果换行的地方有一个操作符（例如 + 或者 << ）。这个操作符应该出现在下一行的开头，而不是当前行的结尾。

```C++
    std::cout << 3 + 4
        + 5 + 6
        * 7 * 8;
```

这样可以清楚的看出后续行是前一行的延续，并且对齐左侧的操作符，会使得代码更可读。

6. 使用空格将赋值操作，注释对齐。

难以阅读：

```C++
cost = 57;
pricePerItem = 24;
value = 5;
numberOfItems = 17;
```

容易阅读：

```C++
cost          = 57;
pricePerItem  = 24;
value         = 5;
numberOfItems = 17;
```

难以阅读：

```C++
std::cout << "Hello world!\n"; // cout 在iostream库中
std::cout << "It is very nice to meet you!\n"; // 这样的注释让代码看起来难以阅读
std::cout << "Yeah!\n"; // 尤其是每行长度不一
```

更易于阅读：

```C++
std::cout << "Hello world!\n";                  // cout 在iostream库中
std::cout << "It is very nice to meet you!\n";  // 这样的注释让代码看起来易于阅读
std::cout << "Yeah!\n";                         // 注释对齐
```

在本教程中，我们将遵循这些约定。当介绍新知识时，同时将介绍与这些功能配套的新样式建议。

C++为您提供了选择您最舒适的风格或认为最好的风格的能力。然而，我们强烈建议您使用我们在示例中使用的相同样式。
它已经被大量程序员在数以亿行代码上进行了验证。

{{< alert success >}}
**最佳实践**

再已有的项目中开发时，选择与原有项目一致的代码样式。
{{< /alert >}}

***
## 自动格式化

大多数现代IDE将帮助您在编写代码时自动格式化代码（例如，当您创建函数时，IDE将自动缩进函数体中的语句）。

然而，当您添加或删除代码，或更改IDE的默认格式，或粘贴具有不同格式的代码块时，格式可能会变得混乱。修复文件的部分或全部格式可能是一个头痛的问题。幸运的是，现代IDE通常包含自动格式化功能，该功能将重新格式化选定的代码或整个文件。

为了更容易操作，建议添加使用键盘快捷，来自动格式化代码文件。

还有一些外部工具可以用于自动格式化代码。clang-format是一个流行的工具。

{{< alert success >}}
**对于Visual Studio用户**

在Visual Studio中，可以在 编辑>高级 下找到自动格式化的选项。

{{< /alert >}}

{{< alert success >}}
**最佳实践**

强烈建议使用自动格式功能，以保持代码的格式样式一致。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter1/keywords-and-naming-identifiers/" next="/basic/chapter1/literal-operator/" >}}
1.6 关键字和变量命名规则
<--->
1.8 字面值和操作符简介
{{< /prevnext >}}
