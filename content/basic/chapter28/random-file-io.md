---
title: "随机文件I/O"
date: 2025-03-02T00:53:53+08:00
---

文件指针

每个文件流类都包含一个文件指针，用于跟踪文件中的当前读/写位置。当从文件中读取或写入内容时，读取/写入发生在文件指针的当前位置。默认情况下，打开文件进行读取或写入时，文件指针设置为文件的开头。然而，如果以追加模式打开文件，则文件指针将移动到文件的末尾，以便写入不会覆盖文件的任何当前内容。

使用seekg（）和seekp（）随机访问文件

到目前为止，我们所做的所有文件访问都是顺序的——也就是说，我们已经按顺序读取或写入了文件内容。然而，也可以进行随机文件访问——即跳过文件中的各个点来读取其内容。当文件中充满记录，并且您希望检索特定记录时，这可能很有用。您可以直接跳到要检索的记录，而不是读取所有记录，直到找到所需的记录。

随机文件访问是通过使用seekg（）函数（用于输入）和seekp（）函数来操作文件指针（用于输出）来完成的。如果您想知道，g代表“get”，p代表“put”。对于某些类型的流，seekg（）（更改读取位置）和seekp（）（改变写入位置）独立操作——然而，对于文件流，读取和写入位置总是相同的，因此seekg和seekp.可以互换使用。

seekg（）和seekp（）函数采用两个参数。第一个参数是偏移量，它确定要移动文件指针的字节数。第二个参数是一个ios标志，指定偏移量参数的偏移量。

正偏移量表示将文件指针移向文件末尾，而负偏移量表示使文件指针移到文件开头。

下面是一些示例：

```C++
inf.seekg(14, std::ios::cur); // move forward 14 bytes
inf.seekg(-18, std::ios::cur); // move backwards 18 bytes
inf.seekg(22, std::ios::beg); // move to 22nd byte in file
inf.seekg(24); // move to 24th byte in file
inf.seekg(-28, std::ios::end); // move to the 28th byte before end of the file
```

移动到文件的开头或结尾很容易：

```C++
inf.seekg(0, std::ios::beg); // move to beginning of file
inf.seekg(0, std::ios::end); // move to end of file
```

为了让您了解它们是如何工作的，让我们使用seekg（）和在上一课中创建的输入文件来做一个示例。该输入文件如下所示：

下面是一个例子：

```C++
#include <fstream>
#include <iostream>
#include <string>

int main()
{
    std::ifstream inf{ "Sample.txt" };

    // If we couldn't open the input file stream for reading
    if (!inf)
    {
        // Print an error and exit
        std::cerr << "Uh oh, Sample.txt could not be opened for reading!\n";
        return 1;
    }

    std::string strData;

    inf.seekg(5); // move to 5th character
    // Get the rest of the line and print it, moving to line 2
    std::getline(inf, strData);
    std::cout << strData << '\n';

    inf.seekg(8, std::ios::cur); // move 8 more bytes into file
    // Get rest of the line and print it
    std::getline(inf, strData);
    std::cout << strData << '\n';

    inf.seekg(-14, std::ios::end); // move 14 bytes before end of file
    // Get rest of the line and print it
    std::getline(inf, strData); // undefined behavior
    std::cout << strData << '\n';

    return 0;
}
```

这将产生以下结果：

根据文件的编码方式，第三行可能会得到不同的结果。

seekg（）和seekp（）更好地用于二进制文件。您可以通过以下方式以二进制模式打开上述文件：

```C++
    std::ifstream inf {"Sample.txt", std::ifstream::binary};
```

其他两个有用的函数是tellg（）和tellp（），它们返回文件指针的绝对位置。这可以用于确定文件的大小：

```C++
std::ifstream inf {"Sample.txt"};
inf.seekg(0, std::ios::end); // move to end of file
std::cout << inf.tellg();
```

在作者的机器上，此命令打印：

这是sample.txt的长度，以字节为单位（假设最后一行后面有一个新行）。

使用fstream同时读取和写入文件

fstream类能够同时读取和写入文件——几乎！这里最大的警告是，不可能在阅读和写作之间任意切换。一旦发生读取或写入，在两者之间切换的唯一方法是执行修改文件位置的操作（例如查找）。如果您实际上不想移动文件指针（因为它已经在您想要的位置），则可以始终搜索到当前位置：

```C++
// assume iofile is an object of type fstream
iofile.seekg(iofile.tellg(), std::ios::beg); // seek to current file position
```

如果不这样做，可能会发生许多奇怪的事情。

（注意：尽管iofile.seekg（0，std:：ios:：cur）似乎也可以工作，但似乎有些编译器可能会对此进行优化）。

还有一点小技巧：与ifstream不同，ifstream.我们可以说while（inf）来确定是否有更多的内容要读，这对fstream不起作用。

让我们使用fstream做一个文件I/O示例。我们将编写一个程序，打开一个文件，读取其内容，并将它找到的任何元音更改为“#”符号。

```C++
#include <fstream>
#include <iostream>
#include <string>

int main()
{
    // Note we have to specify both in and out because we're using fstream
    std::fstream iofile{ "Sample.txt", std::ios::in | std::ios::out };

    // If we couldn't open iofile, print an error
    if (!iofile)
    {
        // Print an error and exit
        std::cerr << "Uh oh, Sample.txt could not be opened!\n";
        return 1;
    }

    char chChar{}; // we're going to do this character by character

    // While there's still data to process
    while (iofile.get(chChar))
    {
        switch (chChar)
        {
            // If we find a vowel
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

                // Back up one character
                iofile.seekg(-1, std::ios::cur);

                // Because we did a seek, we can now safely do a write, so
                // let's write a # over the vowel
                iofile << '#';

                // Now we want to go back to read mode so the next call
                // to get() will perform correctly.  We'll seekg() to the current
                // location because we don't want to move the file pointer.
                iofile.seekg(iofile.tellg(), std::ios::beg);

                break;
        }
    }

    return 0;
}
```

运行上述程序后，Sample.txt文件将如下所示：

其他有用的文件功能

要删除文件，只需使用remove（）函数。

此外，如果流当前处于打开状态，is_open（）函数将返回true，否则返回false。

关于将指针写入磁盘的警告

虽然将变量流式传输到文件相当容易，但当您处理指针时，事情变得更加复杂。请记住，指针只是保存它所指向的变量的地址。尽管可以将地址读写到磁盘，但这样做是极其危险的。这是因为变量的地址可能因执行而异。因此，尽管在将地址写入磁盘时，变量可能存在于地址0x0012FF7C，但当您读回该地址时，它可能不再存在于该地址！

例如，假设您有一个名为nValue的整数，其地址为0x0012FF7C。您将nValue赋值为5。您还声明了一个名为*pnValue的指针，该指针指向nValue。pnValue保存nValue的地址0x0012FF7C。您希望保存这些内容以备以后使用，因此将值5和地址0x0012FF7C写入磁盘。

几周后，再次运行该程序，并从磁盘读取这些值。将值5读入另一个名为nValue的变量，该变量的值为0x0012FF78。将地址0x0012FF7C读取到名为*pnValue的新指针中。由于当nValue生存在0x0012FF78时，pnValue现在指向0x0012FF7C，因此pnValue不再指向nValue，尝试访问pnValue将导致麻烦。

{{< alert success >}}
**警告**

在文本文件中，查找文件开头以外的位置可能会导致意外行为。

在编程中，换行符（“\n”）实际上是一个抽象。

1. 在Windows上，新行表示为连续的CR（回车）和LF（换行）字符（因此需要2个字节的存储）。
2. 在Unix上，新行表示为LF（换行）字符（因此需要1个字节的存储）。


根据文件的编码方式，在任一方向上寻找超过新行所需的字节数是可变的，这意味着结果将因使用的编码而异。

同样在某些操作系统上，文件可以用尾随的零字节（值为0的字节）填充。查找文件的结尾（或与文件结尾的偏移量）将在此类文件上产生不同的结果。

{{< /alert >}}

{{< alert success >}}
**作者注释**

上一示例中的结果64发生在Windows上。如果在Unix上运行该示例，则会得到60，因为换行符表示更小。如果文件用尾随的零字节填充，则可能会得到其他内容。

{{< /alert >}}

{{< alert success >}}
**警告**

不要将内存地址写入文件。当您从磁盘读回它们的值时，最初位于这些地址的变量可能位于不同的地址，并且地址将无效。

{{< /alert >}}

