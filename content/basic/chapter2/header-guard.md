---
title: "头文件保护"
date: 2023-10-09T20:06:10+08:00
---

***
## 重复定义问题

在第2.7课——前向声明和定义中，我们注意到变量或函数标识符只能有一个定义（一个定义规则）。因此，多次定义变量标识符的程序将导致编译错误：

```C++
int main()
{
    int x; // this is a definition for variable x
    int x; // compile error: duplicate definition

    return 0;
}
```

类似地，多次定义函数的程序也将导致编译错误：

```C++
#include <iostream>

int foo() // this is a definition for function foo
{
    return 5;
}

int foo() // compile error: duplicate definition
{
    return 5;
}

int main()
{
    std::cout << foo();
    return 0;
}
```

虽然这些程序很容易修复（删除重复的定义），但使用头文件，很容易导致头文件中的定义被多次包含。当头文件#包含另一个头文件（这是常见的）时，可能会发生这种情况。

考虑以下学术示例：

方形.h：

```C++
int getSquareSides()
{
    return 4;
}
```

波浪.h：

```C++
#include "square.h"
```

主.cpp：

```C++
#include "square.h"
#include "wave.h"

int main()
{
    return 0;
}
```

这个看似无辜的程序无法编译！下面是正在发生的事情。首先，main.cpp#包含square.h，它将函数getSquareSides的定义复制到main.cpp中。然后，main.copp#包含wave.h，其中#包含sqre.h本身。这会将square.h的内容（包括函数getSquareSides的定义）复制到wave.h中，然后将其复制到main.cpp中。

因此，在解析所有#Include之后，main.cpp最终如下所示：

```C++
int getSquareSides()  // from square.h
{
    return 4;
}

int getSquareSides() // from wave.h (via square.h)
{
    return 4;
}

int main()
{
    return 0;
}
```

重复的定义和编译错误。每个文件单独都可以。然而，由于main.cpp最后两次#包含square.h的内容，我们遇到了问题。如果wave.h需要getSquareSides（），而main.cpp需要wave.h和square.h，您将如何解决此问题？

{{< alert success >}}
**作者注释**

在接下来的例子中，我们将在头文件中定义一些函数。你通常不应该这样做。

我们之所以在这里这样做，是因为它是使用我们已经介绍的功能来演示一些概念的最有效方法。

{{< /alert >}}

***
## 收割台护罩

好消息是，我们可以通过一种称为头部保护（也称为包含保护）的机制来避免上述问题。标头保护是采用以下形式的条件编译指令：

```C++
#ifndef SOME_UNIQUE_NAME_HERE
#define SOME_UNIQUE_NAME_HERE

// your declarations (and certain types of definitions) here

#endif
```

当包含此头时，预处理器检查SOME_UNIQUE_NAME_HERE之前是否已定义。如果这是我们第一次包含头，SOME_UNIQUE_NAME_HERE将不会被定义。因此，它#定义SOME_UNIQUE_NAME_HERE并包含文件的内容。如果标头再次包含在同一文件中，则SOME_UNIQUE_NAME_HERE将从第一次包含标头的内容时起就已经定义，并且标头内容将被忽略（由于#ifndef）。

所有的头文件都应该有头保护。SOME_UNIQUE_NAME_HERE可以是您想要的任何名称，但根据惯例，它被设置为头文件的完整文件名，以所有大写字母键入，使用下划线表示空格或标点。例如，square.h将具有收割台护罩：

方形.h：

```C++
#ifndef SQUARE_H
#define SQUARE_H

int getSquareSides()
{
    return 4;
}

#endif
```

即使是标准库标头也使用标头保护。如果要查看Visual Studio中的iostream头文件，您将看到：

```C++
#ifndef _IOSTREAM_
#define _IOSTREAM_

// content here

#endif
```

{{< alert success >}}
**对于高级读者**

在大型程序中，可以有两个单独的头文件（包括在不同的目录中），它们最终具有相同的文件名（例如，directoryA\config.h和directory B\config.h.）。如果仅将文件名用于包含保护（例如，config_h），则这两个文件可能最终使用相同的保护名称。如果发生这种情况，任何包含（直接或间接）这两个config.h文件的文件都不会接收第二个要包含的包含文件的内容。这可能会导致编译错误。

由于保护名称冲突的可能性，许多开发人员建议在头保护中使用更复杂/唯一的名称。一些好的建议是PROJECT_PATH_FILE_H、FILE_LARGE-RANDOM-NUMBER_H或FILE_CREATION-DATE_H的命名约定。

{{< /alert >}}

***
## 使用页眉护板更新前面的示例

让我们返回到square.h示例，使用带有标题保护的square.h。为了获得好的形式，我们还将在wave.h中添加头部保护。

平方.h

```C++
#ifndef SQUARE_H
#define SQUARE_H

int getSquareSides()
{
    return 4;
}

#endif
```

波浪.h：

```C++
#ifndef WAVE_H
#define WAVE_H

#include "square.h"

#endif
```

主.cpp：

```C++
#include "square.h"
#include "wave.h"

int main()
{
    return 0;
}
```

预处理器解析所有#include指令后，该程序如下所示：

主.cpp：

```C++
// Square.h included from main.cpp
#ifndef SQUARE_H // square.h included from main.cpp
#define SQUARE_H // SQUARE_H gets defined here

// and all this content gets included
int getSquareSides()
{
    return 4;
}

#endif // SQUARE_H

#ifndef WAVE_H // wave.h included from main.cpp
#define WAVE_H
#ifndef SQUARE_H // square.h included from wave.h, SQUARE_H is already defined from above
#define SQUARE_H // so none of this content gets included

int getSquareSides()
{
    return 4;
}

#endif // SQUARE_H
#endif // WAVE_H

int main()
{
    return 0;
}
```

让我们看看这是如何计算的。

首先，预处理器计算#ifndef SQUARE_H。SQUARE_H尚未定义，因此包含从#ifndef到后续#endif的代码以进行编译。该代码定义SQUARE_H，并具有getSquareSides函数的定义。

稍后，计算下一个#ifndef SQUARE_H。这一次，SQUARE_H被定义了（因为它是在上面定义的），因此从#ifndef到后续#endif的代码被排除在编译之外。

标题保护防止重复包含，因为第一次遇到保护时，未定义保护宏，因此包含保护的内容。超过该点后，将定义保护宏，因此将排除保护内容的任何后续副本。

***
## 标头保护不会阻止标头被包含在不同的代码文件中一次

请注意，标头保护的目标是防止代码文件接收保护标头的多个副本。根据设计，头文件保护不会阻止给定的头文件被包含（一次）到单独的代码文件中。这也可能导致意外问题。考虑：

方形.h：

```C++
#ifndef SQUARE_H
#define SQUARE_H

int getSquareSides()
{
    return 4;
}

int getSquarePerimeter(int sideLength); // forward declaration for getSquarePerimeter

#endif
```

平方.cpp：

```C++
#include "square.h"  // square.h is included once here

int getSquarePerimeter(int sideLength)
{
    return sideLength * getSquareSides();
}
```

主.cpp：

```C++
#include "square.h" // square.h is also included once here
#include <iostream>

int main()
{
    std::cout << "a square has " << getSquareSides() << " sides\n";
    std::cout << "a square of length 5 has perimeter length " << getSquarePerimeter(5) << '\n';

    return 0;
}
```

请注意，square.h同时包含在main.cpp和square.cpp中。这意味着square.h的内容将一次包含在square.cpp中，一次包含到main.cpp中。

让我们更详细地研究一下为什么会发生这种情况。当square.h从square.cpp中包含时，square_h被定义为square.cpp的末尾。此定义防止square.h再次包含在square.copp中（这是收割台保护的点）。然而，一旦square.cpp完成，square_H就不再被认为是定义的。这意味着当预处理器在main.cpp上运行时，SQUARE_H最初不是在main.copp中定义的。

最终结果是square.cpp和main.cpp都获得了getSquareSides定义的副本。该程序将编译，但链接器将抱怨您的程序具有标识符getSquareSides的多个定义！

解决此问题的最佳方法是将函数定义放在其中一个.cpp文件中，以便标头仅包含向前声明：

方形.h：

```C++
#ifndef SQUARE_H
#define SQUARE_H

int getSquareSides(); // forward declaration for getSquareSides
int getSquarePerimeter(int sideLength); // forward declaration for getSquarePerimeter

#endif
```

平方.cpp：

```C++
#include "square.h"

int getSquareSides() // actual definition for getSquareSides
{
    return 4;
}

int getSquarePerimeter(int sideLength)
{
    return sideLength * getSquareSides();
}
```

主.cpp：

```C++
#include "square.h" // square.h is also included once here
#include <iostream>

int main()
{
    std::cout << "a square has " << getSquareSides() << " sides\n";
    std::cout << "a square of length 5 has perimeter length " << getSquarePerimeter(5) << '\n';

    return 0;
}
```

现在，当编译程序时，函数getSquareSides将只有一个定义（通过square.cpp），因此链接器很高兴。文件main.cpp能够调用该函数（即使它位于square.cpp中），因为它包括square.h，该文件具有函数的前向声明（链接器将从main.cpp对getSquareSides的调用连接到square.cpp中getSquare Sides定义）。

***
## 我们不能避免头文件中的定义吗？

我们通常告诉您不要在头中包含函数定义。所以你可能想知道为什么你应该包括头部警卫，如果他们保护你从你不应该做的事情。

在将来，我们将向您展示许多情况，其中需要将非函数定义放在头文件中。例如，C++将允许您创建自己的类型。这些自定义类型通常在头文件中定义，因此类型定义可以传播到需要使用它们的代码文件。如果没有头保护，代码文件可能会以给定类型定义的多个（相同）副本结束，编译器会将其标记为错误。

因此，尽管在本系列教程中，严格来说没有必要在此时配备队长，但我们现在正在建立良好的习惯，因此您不必在以后忘记坏习惯。

***
## #杂注一次

现代编译器使用#pragma预处理器指令支持更简单的替代形式的头保护：

```C++
#pragma once

// your code here
```

#pragma曾经与头保护具有相同的用途：避免头文件被多次包含。使用传统的头保护，开发人员负责保护头（通过使用预处理器指令#ifndef、#define和#endif）。使用#pragma一次，我们请求编译器保护头。它究竟如何做到这一点是一个特定于实现的细节。

对于大多数项目，#pragma曾经工作得很好，许多开发人员现在更喜欢它，因为它更容易，更不容易出错。许多IDE还将在通过IDE生成的新头文件的顶部自动包含#pragma一次。

由于#pragma一次不是由C++标准定义的，因此一些编译器可能不会实现它。因此，一些开发公司（如Google）建议使用传统的头保护。在本教程系列中，我们将支持头部保护，因为它们是保护头部的最传统方法。然而，在这一点上，对#pragma once的支持是相当普遍的，如果您希望使用#pragam一次，这在现代C++中是普遍接受的。

{{< alert success >}}
**对于高级读者**

有一种已知的情况，#pragma一次通常会失败。如果复制头文件，使其存在于文件系统上的多个位置，则如果以某种方式包含头的两个副本，则头保护程序将成功地对相同的头进行重复数据消除，但#pragma一次不会这样做（因为编译器不会意识到它们实际上是相同的内容）。

{{< /alert >}}

{{< alert success >}}
**警告**

#pragma指令是为编译器实现者设计的，用于他们想要的任何目的。因此，支持哪些杂注以及这些杂注的含义完全特定于实现。除了#pragma一次外，不要期望在一个编译器上工作的pragma被另一个编译器支持。

{{< /alert >}}

***
## 总结

标头保护旨在确保给定标头文件的内容不会多次复制到任何单个文件中，以防止重复定义。

重复声明是可以的——但即使您的头文件由所有声明（没有定义）组成，也最好包括头保护。

请注意，页眉保护不会阻止将页眉文件的内容复制（一次）到单独的项目文件中。这是一件好事，因为我们经常需要引用来自不同项目文件的给定头的内容。

***

{{< prevnext prev="/basic/chapter2/header-file/" next="/" >}}
2.10 头文件
<--->
主页
{{< /prevnext >}}
