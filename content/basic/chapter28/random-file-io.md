---
title: "随机文件I/O"
date: 2025-03-02T00:53:53+08:00
---

***
## 文件指针

每个文件流类都包含一个文件指针，用于跟踪文件中的当前读/写位置。当从文件中读取或写入内容时，读取/写入发生在文件指针的当前位置。默认情况下，打开文件进行读取或写入时，文件指针设置为文件的开头。然而，如果以追加模式打开文件，则文件指针将移动到文件的末尾，以便写入不会覆盖文件的任何当前内容。

***
## 使用seekg()和seekp()随机访问文件

到目前为止，我们所做的所有文件访问都是顺序的——也就是说，我们按顺序读取或写入文件内容。然而，也可以进行随机文件访问——即跳过文件中的一部分，从后续位置开始进行读写。当文件中充满记录，并且您希望检索特定记录时，这很有用。您可以直接跳到要检索的记录，而不是读取所有记录。

随机文件访问是通过使用seekg()函数（用于输入）和seekp()函数（用于输出）来操作文件指针来完成的。g代表“get”，p代表“put”。对于某些类型的流，seekg()（更改读取位置）和seekp()（改变写入位置）是独立的操作——然而，对于文件流，读取和写入位置总是相同的，因此seekg和seekp.可以互换使用。

seekg()和seekp()函数采用两个参数。第一个参数是偏移量，它确定要移动文件指针的字节数。第二个参数是一个ios标志，指定偏移量参数的相对位置。

| Ios seek 标记 | 含义  |
|  ----  | ----  |
| beg | 偏移量，相对于文件开头（默认行为） |
| cur | 偏移量相对于当前文件指针的位置 |
| end | 偏移量，相对与文件结尾 |

正偏移量表示将文件指针移向文件末尾的方向，而负偏移量表示使文件指针移向文件开头的方向。

下面是一些示例：

```C++
inf.seekg(14, std::ios::cur); // 向前移动 14 bytes
inf.seekg(-18, std::ios::cur); // 向后移动 18 bytes
inf.seekg(22, std::ios::beg); // 移动到文件中的第22个byte
inf.seekg(24); // 移动到文件中的第22个byte
inf.seekg(-28, std::ios::end); // 移动到文件结尾前的倒数第28个byte
```

移动到文件的开头或结尾很容易：

```C++
inf.seekg(0, std::ios::beg); // 移动到文件开头
inf.seekg(0, std::ios::end); // 移动到文件结尾
```

{{< alert success >}}
**警告**

在文本文件中，查找文件开头以外的位置可能会导致意外行为。

在编程中，换行符（“\n”）实际上是一个抽象。

1. 在Windows上，新行表示为连续的CR（回车）和LF（换行）字符（因此需要2个字节的存储）。
2. 在Unix上，新行表示为LF（换行）字符（因此需要1个字节的存储）。


根据文件的编码方式，在任一方向上寻找超过新行所需的字节数是可变的，这意味着结果将因使用的编码而异。

同样在某些操作系统上，文件可以用尾随的‘零’（值为0的字节）填充。查找文件的结尾（或与文件结尾的偏移量）将在此类文件上产生不同的结果。

{{< /alert >}}

为了让您了解它们是如何工作的，让我们使用seekg()和在上一课中创建的输入文件来做一个示例。该输入文件如下所示：

```C++
This is line 1
This is line 2
This is line 3
This is line 4
```

下面是一个例子：

```C++
#include <fstream>
#include <iostream>
#include <string>

int main()
{
    std::ifstream inf{ "Sample.txt" };

    // 如果文件打开失败
    if (!inf)
    {
        // 打印错误并退出
        std::cerr << "Uh oh, Sample.txt could not be opened for reading!\n";
        return 1;
    }

    std::string strData;

    inf.seekg(5); // 移动到第5个字符
    // 获取当前一行，并打印，然后文件指针移动到第2行
    std::getline(inf, strData);
    std::cout << strData << '\n';

    inf.seekg(8, std::ios::cur); // 从当前位置，向前再移动8个byte
    // 获取当前行剩余的数据，并打印
    std::getline(inf, strData);
    std::cout << strData << '\n';

    inf.seekg(-14, std::ios::end); // 移动到文件结尾前的倒数第14个byte
    // 获取当前行剩余的数据，并打印
    std::getline(inf, strData); // 未定义的行为
    std::cout << strData << '\n';

    return 0;
}
```

这将产生以下结果：

```C++
is line 1
line 2
This is line 4
```

根据文件的编码方式，第三行可能会得到不同的结果。

seekg()和seekp()更适用于二进制文件。您可以通过以下方式以二进制模式打开上述文件：

```C++
    std::ifstream inf {"Sample.txt", std::ifstream::binary};
```

其他两个有用的函数是tellg()和tellp()，它们返回文件指针的绝对位置。这可以用于确定文件的大小：

```C++
std::ifstream inf {"Sample.txt"};
inf.seekg(0, std::ios::end); // 移动到文件结尾
std::cout << inf.tellg();
```

在作者的机器上，此命令打印：

```C++
64
```

这是sample.txt的长度，以字节为单位（假设最后一行后面有一个新行）。

{{< alert success >}}
**注**

上一示例中的结果64发生在Windows上。如果在Unix上运行该示例，则会得到60，因为换行符更小。如果文件用尾随的零字节填充，则可能会得到其他内容。

{{< /alert >}}

***
## 使用fstream同时读取和写入文件

fstream类能够同时读取和写入文件！这里最大的警告是，不能在读取和写入之间任意切换。一旦发生读取或写入，在两者之间切换的唯一方法是执行修改文件指针位置的操作（seek）。如果您实际上不想移动文件指针（因为它已经在您想要的位置），则可以始终seek到当前位置：

```C++
// 假定 iofile 是一个 fstream 对象
iofile.seekg(iofile.tellg(), std::ios::beg); // seek 到当前位置
```

如果不这样做，可能会发生许多奇怪的事情。

（注意：尽管“iofile.seekg(0, std::ios::cur)”似乎也可以工作，但似乎有些编译器可能会对此进行优化）。

还有一点小技巧：与ifstream不同，我们可以用“while (inf)”来确定是否有更多的内容要读，这对fstream不起作用。

让我们使用fstream做一个文件I/O示例。我们将编写一个程序，打开一个文件，读取其内容，并将它找到的任何元音更改为“#”符号。

```C++
#include <fstream>
#include <iostream>
#include <string>

int main()
{
    // 因为使用的是 fstream，所以声明需要同时读写改文件
    std::fstream iofile{ "Sample.txt", std::ios::in | std::ios::out };

    // 打开文件失败
    if (!iofile)
    {
        // 打印错误并退出
        std::cerr << "Uh oh, Sample.txt could not be opened!\n";
        return 1;
    }

    char chChar{}; // 逐字符的处理文件

    // 当文件中仍然有数据
    while (iofile.get(chChar))
    {
        switch (chChar)
        {
            // 如果找到一个元音字符
            case 'a':
            case 'e':
            case 'i':
            case 'o':
            case 'u':
            case 'A':
            case 'E':
            case 'I':
            case 'O':
            case 'U':

                // 往后退一个字符
                iofile.seekg(-1, std::ios::cur);

                // 因为做了seek，所以可以安全的写入
                // 这里将元音替换为 #
                iofile << '#';

                // 现在需要切换为读模式
                // 使用 seekg() 移动到当前位置，因为这里不需要改变文件指针的位置
                iofile.seekg(iofile.tellg(), std::ios::beg);

                break;
        }
    }

    return 0;
}
```

运行上述程序后，Sample.txt文件将如下所示：

```C++
Th#s #s l#n# 1
Th#s #s l#n# 2
Th#s #s l#n# 3
Th#s #s l#n# 4
```

***
## 其他有用的文件功能

要删除文件，只需使用remove()函数。

此外，如果流当前处于打开状态，is_open()函数将返回true，否则返回false。

***
## 关于将指针写入磁盘的警告

虽然将变量流式传输到文件相当容易，但当您处理指针时，事情变得更加复杂。请记住，指针只是保存它所指向的变量的地址。尽管可以将地址读写到磁盘，但这样做是极其危险的。这是因为变量的地址可能因执行而异。因此，尽管在将地址写入磁盘时，变量可能存在于地址0x0012FF7C，但当您读回该地址时，它可能不再存在于该地址！

例如，假设您有一个名为nValue的整数，其地址为0x0012FF7C。您将nValue赋值为5。您还声明了一个名为*pnValue的指针，该指针指向nValue。pnValue保存nValue的地址0x0012FF7C。您希望保存这些内容以备以后使用，因此将值5和地址0x0012FF7C写入磁盘。

几周后，再次运行该程序，并从磁盘读取这些值。将值5读入另一个名为nValue的变量，该变量的值为0x0012FF78。将地址0x0012FF7C读取到名为*pnValue的新指针中。由于当前nValue生存在0x0012FF78，pnValue现在指向0x0012FF7C，因此pnValue不再指向nValue，尝试访问pnValue将导致问题。


{{< alert success >}}
**警告**

不要将内存地址写入文件。当您从磁盘读回它们时，最初位于这些地址的变量可能位于不同的地址，该地址是无效的。

{{< /alert >}}

***