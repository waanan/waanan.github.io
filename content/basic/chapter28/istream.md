---
title: "使用istream处理输入"
date: 2025-03-02T00:53:53+08:00
---

iostream库相当复杂——因此我们无法在这些教程中完整地介绍它。这里，将向您展示最常用的功能。在本节中，将研究输入类（istream）的各个方面。

***
## 提取操作符

在许多课程中都可以看到，可以使用提取操作符（>>）从输入流中读取信息。C++为所有内置数据类型预定义了提取操作，并且之前我们也介绍了如何为自定义的类重载提取操作符。

读取字符串时，提取操作符的一个常见问题是如何防止输入溢出缓冲区。以下示例：

```C++
char buf[10]{};
std::cin >> buf;
```

如果用户输入18个字符会怎么样？缓冲区溢出，导致的非预期行为没人能预料到了。一般来说，假设用户将输入字符的格式是有问题。

处理此问题的一种方法是使用操纵器。操纵器是与提取（\>\>）或插入（\<\<）操作符一起应用时，用于修改stream行为的对象。您已经使用过的一个操纵器是“std::endl”，它既打印换行符，又清空缓冲区。C++提供了一个称为setw（在iomanip头文件中）的操纵器，可用于限制从流中读入的字符数。要使用setw()，只需提供读取的最大字符数作为参数，并将其插入到输入语句中，如下所示：

```C++
#include <iomanip>
char buf[10]{};
std::cin >> std::setw(10) >> buf;
```

该程序现在将仅从流中读取前9个字符（为终止符留出空间）。任何剩余的字符都将保留在流中，直到下一次提取。

***
## 提取和空白

作为提示，提取操作符跳过空白（空格、制表符和换行符）。

看看下面的程序：

```C++
int main()
{
    char ch{};
    while (std::cin >> ch)
        std::cout << ch;

    return 0;
}
```

当用户输入以下内容时：

```C++
Hello my name is Alex
```

提取操作符跳过空格和换行。因此，输出是：

```C++
HellomynameisAlex
```

通常，希望获得用户输入，不应该丢弃空白。

为此，istream类提供了许多可以用于此目的的函数。最有用的一个是get()函数，它从输入流中获取原始字符。

下面是与上面相同的程序，使用get()：

```C++
int main()
{
    char ch{};
    while (std::cin.get(ch))
        std::cout << ch;

    return 0;
}
```

现在，当我们使用输入时：

```C++
Hello my name is Alex
```

输出是：

```C++
Hello my name is Alex
```

还有一个字符串版本，它需要设置读取的最大字符数量：

```C++
int main()
{
    char strBuf[11]{};
    std::cin.get(strBuf, 11);
    std::cout << strBuf << '\n';

    return 0;
}
```

如果我们输入：

```C++
Hello my name is Alex
```

输出是：

```C++
Hello my n
```

注意，我们只读取前10个字符（必须为终止符保留一个字符）。其余字符留在输入流中。

关于get()需要注意的一件重要事情是，它不读取换行符！这可能会导致一些意外的结果：

```C++
int main()
{
    char strBuf[11]{};
    // 最多读取10个字符
    std::cin.get(strBuf, 11);
    std::cout << strBuf << '\n';

    // 再最多读取10个字符
    std::cin.get(strBuf, 11);
    std::cout << strBuf << '\n';
    return 0;
}
```

如果用户输入：

```C++
Hello!
```

程序将打印：

```C++
Hello!
```

然后终止！它为什么不多再读取10个字符？答案是因为第一个get()读取到换行，然后停止。第二个get()看到cin流中仍然有输入，并试图读取它。但第一个字符是换行符，因此它立即停止。

因此，还有一个名为getline()的函数，其工作方式类似于get()，但将提取（并丢弃）分隔符。

```C++
int main()
{
    char strBuf[11]{};
    // 最多读取10个字符
    std::cin.getline(strBuf, 11);
    std::cout << strBuf << '\n';

    // 再最多读取10个字符
    std::cin.getline(strBuf, 11);
    std::cout << strBuf << '\n';
    return 0;
}
```

此代码将按预期执行，即使用户输入的字符串中包含换行符。

如果需要知道上次调用getline()提取了多少字符，请使用gcount():

```C++
int main()
{
    char strBuf[100]{};
    std::cin.getline(strBuf, 100);
    std::cout << strBuf << '\n';
    std::cout << std::cin.gcount() << " characters were read" << '\n';

    return 0;
}
```

gcount()包括任何提取和丢弃的分隔符。

***
## 用于std::string的getline()的特殊版本

getline()有一个特殊版本，位于istream类之外，用于读取数据到std::string。此特殊版本不是ostream或istream的成员，并包含在string头文件中。下面是它的用法示例：

```C++
#include <string>
#include <iostream>

int main()
{
    std::string strBuf{};
    std::getline(std::cin, strBuf);
    std::cout << strBuf << '\n';

    return 0;
}
```

***
## 几个更有用的istream函数

有几个您可能想使用的更有用的输入函数：

1. ignore() 丢弃流中的第一个字符。
2. ignore(int nCount) 丢弃前nCount字符。
3. peek() 允许您从流中读取字符，而不将其从流中删除。
4. unget() 将流中的最后读取一个字符塞回去，以便下次调用可以再次读取它。
5. putback(char ch) 允许您将所选的字符放回流中，以便下一次调用读取。

istream包含许多其他函数和上述函数的变体，这些函数可能有用，具体取决于您需要执行的操作。您可以在[这里](https://en.cppreference.com/w/cpp/io/basic_istream)找到对应的文档。

***