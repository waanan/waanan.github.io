---
title: "头文件保护"
date: 2023-10-09T20:06:10+08:00
---

***
## 重复定义问题

在前向声明一节中，我们注意到变量或函数标识符只能有一个定义（单定义规则）。因此，多次定义变量标识符的程序将导致编译错误：

```C++
int main()
{
    int x; // 变量 x 的定义
    int x; // 编译失败: 重复定义

    return 0;
}
```

类似地，多次定义相同函数的程序也将导致编译错误：

```C++
#include <iostream>

int foo() // 函数foo的定义
{
    return 5;
}

int foo() // 编译失败: 重复定义
{
    return 5;
}

int main()
{
    std::cout << foo();
    return 0;
}
```

虽然这些程序很容易修复（删除重复的定义），但使用头文件，很容易导致头文件中的定义被多次包含。当头文件#include另一个头文件（这是常见的）时，可能会发生这种情况。

考虑以下示例：

square.h：

```C++
int getSquareSides()
{
    return 4;
}
```

wave.h：

```C++
#include "square.h"
```

main.cpp：

```C++
#include "square.h"
#include "wave.h"

int main()
{
    return 0;
}
```

此程序看似正常其实无法编译！原因如下。首先，main.cpp包含square.h，它将函数getSquareSides的定义复制到main.cpp中。其次，main.cpp包含wave.h，间接包含square.h。将square.h的内容（包括函数getSquareSides的定义）复制到wave.h中，然后将其复制到main.cpp中。

因此，在解析所有#include之后，main.cpp最终如下所示：

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

重复定义导致编译错误。每个文件可以单独编译。然而，由于main.cpp包含两次square.h的内容，导致该问题。如果wave.h需要getSquareSides()，而main.cpp需要wave.h和square.h，如何解决此问题？

{{< alert success >}}
**注**

本节所举例子中，将在头文件中定义一些函数。通常不应这样做。

之所以这里这样做，是因为它是使用已经介绍的功能来演示一些概念的最有效方法。

{{< /alert >}}

***
## 头文件保护

好消息是，我们可通过头文件保护（也称包含保护）机制来避免上述问题。头文件保护采用如下形式条件编译指令：

```C++
#ifndef SOME_UNIQUE_NAME_HERE
#define SOME_UNIQUE_NAME_HERE

// 这里放置你的声明

#endif
```

当包含此头文件时，预处理器检查SOME_UNIQUE_NAME_HERE之前是否已定义。如果是第一次包含该头文件，SOME_UNIQUE_NAME_HERE不会被定义。因此，会定义SOME_UNIQUE_NAME_HERE并包含文件内容。如果头文件再次包含同一文件，则SOME_UNIQUE_NAME_HERE就已定义，且头文件内容将被忽略（由于#ifndef）。

头文件都应有头文件保护。SOME_UNIQUE_NAME_HERE可以起任何名称，但根据惯例，它会被设置为头文件的完整文件名，以大写字母命名，使用下划线表示空格或标点。例如，square.h将具有如下头文件保护：

square.h：

```C++
#ifndef SQUARE_H
#define SQUARE_H

int getSquareSides()
{
    return 4;
}

#endif
```

标准库头文件也使用头文件保护。比如，Visual Studio中的iostream头文件，将看到：

```C++
#ifndef _IOSTREAM_
#define _IOSTREAM_

// 对应的代码内容

#endif
```

{{< alert success >}}
**对于高级读者**

在大型程序中，可以有两个单独的头文件（在不同目录下），它们具有相同的文件名（例如，directoryA\config.h和directory B\config.h）。若仅用文件名命名（例如，config_h），则这两个文件将重名。会导致任何包含（直接或间接）包含这两个config.h文件都只会包含其中一个文件的内容。会导致编译错误。

为了减少名称冲突，建议在头文件保护中使用更复杂/唯一的名称。建议使用PROJECT_PATH_FILE_H、FILE_LARGE-RANDOM-NUMBER_H或FILE_CREATION-DATE_H为命名约定。

{{< /alert >}}

***
## 使用头文件保护更新开头示例

现在返回square.h示例，使用带有头文件保护的square.h。为了更好效果，还将在wave.h中添加头文件保护。

square.h

```C++
#ifndef SQUARE_H
#define SQUARE_H

int getSquareSides()
{
    return 4;
}

#endif
```

wave.h：

```C++
#ifndef WAVE_H
#define WAVE_H

#include "square.h"

#endif
```

main.cpp：

```C++
#include "square.h"
#include "wave.h"

int main()
{
    return 0;
}
```

预处理器解析所有#include指令后，该程序如下所示：

main.cpp：

```C++
// Square.h 引入
#ifndef SQUARE_H
#define SQUARE_H

int getSquareSides()
{
    return 4;
}

#endif // Square.h 引入到此为止

#ifndef WAVE_H // wave.h引入
#define WAVE_H
#ifndef SQUARE_H // 从wave.h引入的square.h, SQUARE_H 在之前已定义
#define SQUARE_H // 所以接下来的getSquareSides()不会被编译

int getSquareSides()
{
    return 4;
}

#endif // 
#endif // wave.h引入到此为止

int main()
{
    return 0;
}
```

程序会这样执行：

首先，预处理器执行#ifndef SQUARE_H。SQUARE_H尚未定义，因此从#ifndef到#endif的代码进行编译。该代码定义SQUARE_H，有getSquareSides函数定义。

稍后，处理下一个#ifndef SQUARE_H。这次，SQUARE_H被定义了，从#ifndef到#endif的代码不会被编译。

头文件保护防止重复包含，因为第一次遇到保护时，引入要保护的内容并定义保护宏，后续将排除被保护内容的任何副本。

***
## 头文件保护不会阻止头文件在不同文件只出现一次

注意，头文件保护的目标是防止代码文件引入头文件的多个副本。根据设计，头文件保护不会阻止不同的代码文件包含给定的头文件。可能导致如下问题：

square.h：

```C++
#ifndef SQUARE_H
#define SQUARE_H

int getSquareSides()
{
    return 4;
}

int getSquarePerimeter(int sideLength); // getSquarePerimeter 前向声明

#endif
```

square.cpp：

```C++
#include "square.h"  // square.h 这里被包含

int getSquarePerimeter(int sideLength)
{
    return sideLength * getSquareSides();
}
```

main.cpp：

```C++
#include "square.h" // square.h 这里又被包含
#include <iostream>

int main()
{
    std::cout << "a square has " << getSquareSides() << " sides\n";
    std::cout << "a square of length 5 has perimeter length " << getSquarePerimeter(5) << '\n';

    return 0;
}
```

请注意，square.h同时包含在main.cpp和square.cpp中。这意味着square.h的内容将既包含在square.cpp中，又包含main.cpp中。

让我们更详细地研究一下发生这种情况的原因。当square.h被square.cpp包含时，SQUARE_H的定义只到square.cpp的末尾，一旦square.cpp完成，SQUARE_H就不再被认为是已定义的。这意味着当预处理器在main.cpp上运行时，SQUARE_H仍然未被定义。

最终结果是square.cpp和main.cpp都获得了getSquareSides定义的副本。该程序能通过编译，但链接时报错，程序具有getSquareSides的多个定义！

解决此问题的最佳方法是将函数定义放在其中一个.cpp文件中，以便头文件仅包含向前声明：

square.h：

```C++
#ifndef SQUARE_H
#define SQUARE_H

int getSquareSides(); // 前向声明 getSquareSides
int getSquarePerimeter(int sideLength); // 前向声明 getSquarePerimeter

#endif
```

square.cpp：

```C++
#include "square.h"

int getSquareSides() // 实际定义 getSquareSides
{
    return 4;
}

int getSquarePerimeter(int sideLength)
{
    return sideLength * getSquareSides();
}
```

main.cpp：

```C++
#include "square.h" // square.h 这里只被引入一次
#include <iostream>

int main()
{
    std::cout << "a square has " << getSquareSides() << " sides\n";
    std::cout << "a square of length 5 has perimeter length " << getSquarePerimeter(5) << '\n';

    return 0;
}
```

现在，当编译程序时，函数getSquareSides将只有一个定义（通过square.cpp），因此链接时不会报错。文件main.cpp能够调用该函数（即使它位于square.cpp中），因为它引用了square.h，该文件具有对应函数的前向声明（链接器将从main.cpp对getSquareSides的调用连接到square.cpp中getSquareSides定义）。

***
## 不能避免头文件中的定义吗？

通常不要在头文件中包含函数定义。如果这么做了，为什么还需要头文件保护呢？

后续，将展示许多情况，其中需要将非函数的定义放在头文件中。例如，C++允许创建自己的类型。这些自定义类型通常在头文件中定义，因此类型定义可以传播到需要使用它们的代码文件。如果没有头文件保护，代码文件可能会以给一个类型多个（相同）副本，编译器会将其标记为错误。

因此，在本节教程中，严格来说没必要在此时配置头文件保护，之所以如此是出于建立良好习惯的需要。

***
## #pragma once

现代编译器使用#pragma预处理器指令支持更简单的替代形式的头文件保护：

```C++
#pragma once

// your code here
```

#pragma once与头文件保护具有相同的用途：避免头文件被多次包含。使用传统的头文件保护，开发人员负责保护头文件（通过使用预处理器指令#ifndef、#define和#endif）。使用#pragma once，我们请求编译器保护头文件。它究竟如何做到，取决于实现的细节。

对于大多数项目，#pragma once工作得很好，许多开发人员更喜欢它，因为更容易，且不容易出错。许多IDE还在通过IDE生成的新头文件的顶部自动包含#pragma once。

由于#pragma once不是由C++标准定义的，因此一些编译器可能不会实现它。因此，一些开发公司（如Google）建议使用传统的头文件保护。在本教程系列中，介绍头文件保护，因为它们是保护头文件的最传统方法。

目前对#pragma once的支持是相当普遍的，如果使用#pragma once，在现代C++中是普遍接受的。

{{< alert success >}}
**警告**

#pragma指令是编译器实现者设计的，用于他们想要的目的。因此，支持哪些#pragma指令以及对应的含义完全取决于实现。除了#pragma once外，不要期望在一个编译器上工作的#pragma被另一个编译器支持。

{{< /alert >}}

***
## 总结

头文件保护旨在确保给定头文件的内容不会多次复制到单个文件中，防止重复定义。

重复声明是可以的——但即使头文件只由声明（没有定义）组成，也最好使用头文件保护。

请注意，头文件保护不会阻止将头文件的内容复制到多个文件中。

***

{{< prevnext prev="/basic/chapter2/header-file/" next="/basic/chapter2/design-first-program/" >}}
2.10 头文件
<--->
2.12 设计第一个程序
{{< /prevnext >}}
