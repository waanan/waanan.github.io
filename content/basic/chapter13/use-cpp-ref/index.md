---
title: "如何使用c++语言手册"
date: 2024-03-08T13:20:57+08:00
---

根据您当前学习的进度，本网站可能是您用于学习C++或查找内容的唯一资源。本网站旨在以初学者友好的方式解释概念，但它不能涵盖C++语言的所有方面。当您开始探索本教程无法覆盖的主题时，不可避免地会遇到本教程无法回答的问题。在这种情况下，您需要利用外部资源。

一个非常好的查询的地方是C++语言手册。本教程倾向于关注比较重要的主题，并使用非正式或通用语言来简化学习，与之不同的是，语言手册使用正式术语精确地描述C++。因此，参考手册往往是全面、准确和难以理解的。

在本课中，将通过研究3个示例来展示如何使用cpp手册网站（ https://zh.cppreference.com/w/%E9%A6%96%E9%A1%B5 ）。

***
## 概述

网站首页上包含核心语言以及标准库：

{{< img src="./sy.png" title="首页">}}

从这里，可以看到C++手册网站上的所有内容，使用搜索功能或搜索引擎可能更容易查找您想了解的部分。一旦您完成本网站上的教程，这里概览是一个很好的地方，可以更深入地研究标准库，并查看该语言还提供了哪些您可能不知道的内容。

表的上半部分显示了该语言当前的功能，而下半部分显示技术规范，这些功能可能在未来版本中添加到C++，也可能不会添加到C++中，或者已经被该语言部分接受。如果想了解即将推出的新功能，这可能很有用。

从C++11开始，新增的功能会标记出来是哪个版本添加的。这是上图中一些链接旁边的绿色小数字。没有版本号的功能从C++98/03开始提供。版本号不仅在概述中，而且在手册上无处不在，让您确切地知道在特定的C++版本中可以使用或不能使用什么。

{{< alert success >}}
**提示**

c++语言手册中包含C语言与C++语言两部分。由于C++与C共享一些函数名，因此在搜索某些内容后，您可能会在C语言部分找到。

{{< /alert >}}

***
## std::string::length

我们之前已经了解过std::string::length，该函数返回字符串的长度。

在cppreference首页，点击字符串库，来查看字符串相关的文档。

{{< img src="./str.png" title="字符串库">}}

这里，可以看到，字符串库，根据字符串内存储不同的字符，有多个对应的类型。std::string，其实是std::basic_string\<char\>的别名。\<char\>表示字符串里的每个字符都是char类型，当想在字符串里存储unicode而不是ASCII码时，其它类型可能会比较容易使用点。

{{< img src="./str_char.jpg" title="字符串库详情">}}

点击std::string，可以查看对应的手册。在下面，对应的小节里，可以看到，有一个length成员函数，返回字符串中的字符数。

{{< img src="./str_len.png" title="字符串库详情">}}

点击进去，可以看到，有length函数对应的功能介绍，参数，返回值以及使用样例。

{{< img src="./str_len_detail.png" title="str len详情">}}

因为std::string::length是一个简单的函数，所以该页面上没有太多内容。

当在学习C++时，示例中会有一些您以前没有见过的功能。可以点击对应的连接跳转过去，进行学习。

***
## std::cin.ignore

在前面，我们学习了std::cin.ignore，它用于忽略直到换行符的所有内容。该函数的参数之一是一些冗长的值。那又是什么？让我们弄清楚！

首先，cin是流式输入，因此，我们点击“基于流的输入/输出”。

{{< img src="./index_iostream.png" title="基于流的输入输出">}}

在对应的页面上，可以找到cin的说明，继续点击查看细节。

{{< img src="./iostream.png" title="iostream">}}

这个页面上，可以看到std::cin和std::wcin的声明，并告诉我们它们所在的头文件。

{{< img src="./cin.png" title="cin">}}

这里并没有ignore相关的讲解，单可以看到，std::cin是一个类型为std::istream的对象。让我们访问std::istream的链接。

哦，在这个页面，我们看到了熟悉的内容，继续点击。

{{< img src="./istream.png" title="istream">}}、

在页面顶部有函数签名和其两个参数的描述。参数后面的=符号表示默认参数）。如果没有为具有默认值的参数提供值，则使用默认值。

{{< img src="./ignore.png" title="ignore">}}

这里回到了我们所有的问题。可以看到，std::numeric_limits\<std::streamsize\>::max()对std::cin.ignore具有特殊意义，它禁用了字符计数检查。这意味着std::cin.ignore将继续忽略字符，直到找到分隔符，或者直到用完要查看的字符。

许多时候，如果您已经知道函数的整个描述，但忘记了参数或返回值的含义，则不需要阅读它的整个描述。在这种情况下，读取参数或返回值描述就足够了。

***
## 语言语法示例

除了标准库之外，cppreference还记录了语言语法。下面是一个示例程序：

```C++
#include <iostream>

int getUserInput()
{
  int i{};
  std::cin >> i;
  return i;
}

int main()
{
  std::cout << "How many bananas did you eat today? \n";

  if (int iBananasEaten{ getUserInput() }; iBananasEaten <= 2)
  {
    std::cout << "Yummy\n";
  }
  else
  {
    std::cout << iBananasEaten << " is a lot!\n";
  }

  return 0;  
}
```

为什么在if语句的条件中有变量定义？让我们使用cppreference查看下if的语法。

{{< img src="./if.png" title="if">}}

在这里可以看到。在条件之前，有一个可选的初始化语句，它看起来像上面代码中发生的事情。

在语法参考下面，有语法的每个部分的解释，包括初始化语句。它表示初始化语句通常是具有初始值设定项的变量的声明。

然后，我们将页面往下滚动一点，就可以看到对应的示例，当然这里的例子有很多我们稍微介绍的功能，但不必理解这些，也可以看明白初始化语句的使用方式:

```C++
// 迭代器, 还没学过，跳过
if (auto it = m.find(10); it != m.end()) { return it->second.size(); }

// [10], 啥东西? 跳过.
if (char buf[10]; std::fgets(buf, 10, stdin)) { m[0] += buf; }

// std::lock_guard, 肯定是个类型反正
if (std::lock_guard lock(mx); shared_flag) { unsafe_ping(); shared_flag = false; }

// 这个很简单, 定了个 int 变量!
if (int s; int count = ReadBytesWithSignal(&s)) { publish(count); raise(s); }

// Oh, 似乎有些复杂!
if (auto keywords = {"if", "for", "while"};
    std::any_of(keywords.begin(), keywords.end(),
                [&s](const char* kw) { return s == kw; })) {
  std::cerr << "Token must not be a keyword\n";
}
```

***
## 关于cppreference准确性的警告

Cppreference不是官方文档——相反，它是一个wiki。有了Wiki，任何人都可以添加和修改内容——内容来自社区。尽管这意味着某人很容易添加错误的信息，但错误信息通常会很快被捕获并删除，使cppreference成为可靠的来源。

C++的唯一官方来源是官方标准（ https://isocpp.org/std/the-standard ），这是一个正式的文档，不容易用作参考。

***

{{< prevnext prev="/basic/chapter13/summary/" next="/basic/chapter14/intro-oop/" >}}
13.13 第13章总结
<--->
14.0 面向对象编程简介
{{< /prevnext >}}
