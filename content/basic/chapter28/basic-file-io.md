---
title: "基本文件I/O"
date: 2025-03-02T00:53:53+08:00
---

C++中的文件I/O的工作方式与普通I/O非常相似（只是稍微增加了一些复杂性）。C++中有3个基本的文件I/O类：ifstream（从istream派生）、ofstream（从ostream派生）和fstream（从iostream派生）。这些类分别进行文件输入、输出和输入/输出。要使用文件I/O类，需要引用fstream头文件。

与cout、cin、cerr和clog流不同，文件流必须由程序员显式设置。然而，这非常简单：要打开文件进行读取和/或写入，只需实例化适当文件I/O类的对象，并将文件名作为参数。然后使用插入（\<\<）或提取（\>\>）操作符写入或读取文件中的数据。完成后，有几种方法可以关闭文件：显式调用close()函数，或者只是让文件I/O变量超出作用域（文件I/O类析构函数将为您关闭文件）。

***
## 输出到文件

为了在下面的示例中进行文件输出，我们将使用ofstream类。这非常简单：

```C++
#include <fstream>
#include <iostream>
 
int main()
{
    // ofstream 被用来输出数据到文件
    // 这里打开一个文件 Sample.txt
    std::ofstream outf{ "Sample.txt" };

    // 如果打开文件失败
    if (!outf)
    {
        // 打印错误并退出
        std::cerr << "Uh oh, Sample.txt could not be opened for writing!\n";
        return 1;
    }

    // 写入两行数据
    outf << "This is line 1\n";
    outf << "This is line 2\n";

    return 0;
	
    // 当 outf 超出作用域, ofstream 析构函数会自动关闭文件
}
```

如果查看项目目录，应该会看到一个名为Sample.txt的文件。如果使用文本编辑器打开它，您将看到它确实包含我们写入文件的两行。

也可以使用put()函数将单个字符写入文件。

***
## 读取文件中的数据

现在，我们将获取在上一个示例中编写的文件，并将其从磁盘读回。请注意，如果到达文件末尾（EOF），ifstream将返回0。我们将使用这个事实来确定是否读取完成。

```C++
#include <fstream>
#include <iostream>
#include <string>

int main()
{
    // ifstream 被用来读取文件
    // 读取的文件名称为 Sample.txt
    std::ifstream inf{ "Sample.txt" };

    // 如果文件打开失败
    if (!inf)
    {
        // 打印错误并退出
        std::cerr << "Uh oh, Sample.txt could not be opened for reading!\n";
        return 1;
    }

    // 如果有可以读取的数据
    std::string strInput{};
    while (inf >> strInput)
        std::cout << strInput << '\n';
    
    return 0;
	
    // 当 inf 超出作用域, ifstream 析构函数会自动关闭文件
}
```

这将产生以下结果：

```C++
This
is
line
1
This
is
line
2
```

嗯，那不是我们想要的。请记住，提取操作符在空白字符处停止处理。为了读入整行，我们必须使用getline()函数。

```C++
#include <fstream>
#include <iostream>
#include <string>

int main()
{
    // ifstream 被用来读取文件
    // 读取的文件名称为 Sample.txt
    std::ifstream inf{ "Sample.txt" };

    // 如果文件打开失败
    if (!inf)
    {
        // 打印错误并退出
        std::cerr << "Uh oh, Sample.txt could not be opened for reading!\n";
        return 1;
    }

    // 如果有可以读取的数据
    std::string strInput{};
    while (std::getline(inf, strInput))
	std::cout << strInput << '\n';
    
    return 0;
	
    // 当 inf 超出作用域, ifstream 析构函数会自动关闭文件
}
```

这将产生以下结果：

```C++
This is line 1
This is line 2
```

***
## 缓冲输出

C++中的输出可以缓冲。这意味着输出到文件流的任何内容都可能不会立即写入磁盘。相反，可以对多个输出操作合并一起处理。这主要是出于性能原因。将缓冲区写入磁盘时，这称为刷新缓冲区。导致刷新缓冲区的一种方法是关闭文件——缓冲区的内容将被刷新到磁盘，然后文件将被关闭。

缓冲通常不是问题，但在某些情况下，它可能会给粗心大意的人带来麻烦。这种情况下的主要原因是缓冲区中存在数据，然后程序立即终止（通过崩溃或调用exit()）。在这些情况下，不会执行文件流类的析构函数，这意味着文件永远不会关闭，这意味著缓冲区永远不会刷新。在这种情况下，缓冲区中的数据不会写入磁盘，并且永远丢失。这就是为什么在调用exit()之前显式关闭任何打开的文件总是一个好主意。

可以使用ostream::flush()函数或向输出流发送std::flush来手动清空缓冲区。这两种方法都可以用于确保缓冲区的内容立即写入磁盘，以防程序崩溃后数据丢失。

一个有趣的注意是std::endl也刷新输出流。因此，过度使用std::endl（导致不必要的缓冲区刷新）在执行清空开销较大的缓冲区I/O（例如写入文件）时可能会影响性能。出于这个原因，注重性能的程序员通常使用“\n”而不是std::endl来表示换行。

***
## 文件模式

如果尝试写入已存在的文件，会发生什么情况？再次运行上面的输出示例表明，每次运行程序时，原始文件都会被完全覆盖。相反，如果我们想在文件末尾追加一些数据，该怎么办？文件流构造函数采用可选的第二个参数，该参数允许您指定有关如何打开文件的信息。该参数称为mode，它接受的有效标志在ios类标明。

| Ios 文件模式 | 含义  |
|  ----  | ----  |
| app | 以追加模式打开文件 |
| ate | 读写操作进行前，先移动到文件末尾 |
| binary | 以二进制模式打开文件（而不是文本模式）|
| in | 以读模式打开文件 (ifstream默认此模式) |
| out | 以写模式打开文件 (ofstream默认此模式) |
| trunc | 如果文件存在，进行删除 |

可以通过将多个标志按位“或”运算在一起来指定它们（使用‘|’运算符）。ifstream默认为std::ios::in。ofstream默认为std::ios::out文件模式。并且fstream默认为“std::ios::in | std::ios::out”文件模式，这意味着您在默认情况下既可以读取也可以写入。

让我们编写一个程序，将另外两行附加到之前创建的Sample.txt文件中：

```C++
#include <iostream>
#include <fstream>

int main()
{
    // 使用 ios:app 标志，标明需要在文件结尾进行追加
    // 这里不需要设置 std::ios::out，因为 ofstream 默认就是 std::ios::out
    std::ofstream outf{ "Sample.txt", std::ios::app };

    // 如果文件打开失败
    if (!outf)
    {
        // 打印错误并退出
        std::cerr << "Uh oh, Sample.txt could not be opened for writing!\n";
        return 1;
    }

    outf << "This is line 3\n";
    outf << "This is line 4\n";
    
    return 0;
	
    // 当 outf 超出作用域, ofstream 析构函数会自动关闭文件
}
```

现在，如果我们查看Sample.txt（使用上面的示例程序之一打印其内容，或将其加载到文本编辑器中），我们将看到以下内容：

```C++
This is line 1
This is line 2
This is line 3
This is line 4
```

***
## 使用open()显式打开文件

就像可以使用close()显式关闭文件流一样，也可以使用open()显式地打开文件流。open()的工作方式与文件流构造函数类似——它采用文件名和可选的文件模式。

例如：

```C++
std::ofstream outf{ "Sample.txt" };
outf << "This is line 1\n";
outf << "This is line 2\n";
outf.close(); // 显示关闭文件

// Oops, 这里以追加模式再打开文件
outf.open("Sample.txt", std::ios::app);
outf << "This is line 3\n";
outf.close();
```

***