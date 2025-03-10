---
title: "针对字符串的stream类"
date: 2025-03-02T00:53:53+08:00
---

到目前为止，您看到的所有I/O示例都是向cout写入或从cin读取的。然而，还有一组针对字符串的stream类，允许您使用熟悉的插入（\<\<）和提取（\>\>）操作符来处理字符串。与istream和ostream一样，字符串stream提供基于保存数据的缓冲区。然而，与cin和cout不同，这些stream不连接到外部I/O通道（例如键盘、监视器等）。字符串流的主要用途之一是缓冲输出以供以后显示，或者逐行处理输入。

字符串有六个stream类：istringstream（从istream派生）、ostringstream（从ostream派生）和stringstream（从iostream派生）用于读取和写入字符串。wistringstream、wostringstreem和wstringstream用于读取和写入宽字符串。要使用这些，需要引用 \<sstream\> 头文件。

有两种方法可以将数据写入到stringstream中：

使用插入（<<）操作符：

```C++
std::stringstream os {};
os << "en garde!\n"; // 将 "en garde!" 插入到 stringstream
```

或者使用 str(string) 函数来设置buffer：

```C++
std::stringstream os {};
os.str("en garde!"); // 将 stringstream 的 buffer 设置为 "en garde!"
```

类似地，有两种方法可以从stringstream中获取数据：

使用 str() 函数，从buffer中获取数据：

```C++
std::stringstream os {};
os << "12345 67.89\n";
std::cout << os.str();
```

这将打印：

```C++
12345 67.89
```

或者使用提取（>>）操作符： 

```C++
std::stringstream os {};
os << "12345 67.89"; // 将数字组成的字符串写入 os

std::string strValue {};
os >> strValue;

std::string strValue2 {};
os >> strValue2;

// 打印提取结果
std::cout << strValue << " - " << strValue2 << '\n';
```

该程序打印：

```C++
12345 - 67.89
```

注意 >> 操作符迭代字符串——每次连续使用 >> 都返回stream中的下一个可提取值。另一方面，str()返回stream的整个值。

***
## 字符串和数字之间的转换

因为插入和提取操作符知道如何处理所有基本数据类型，所以我们可以使用它们将字符串转换为数字，反之亦然。

首先，让我们看看如何将数字转换为字符串：

```C++
std::stringstream os {};

constexpr int nValue { 12345 };
constexpr double dValue { 67.89 };
os << nValue << ' ' << dValue;

std::string strValue1, strValue2;
os >> strValue1 >> strValue2;

std::cout << strValue1 << ' ' << strValue2 << '\n';
```

此代码段打印：

```C++
12345 67.89
```

现在，让我们将字符串转换为数字：

```C++
std::stringstream os {};
os << "12345 67.89"; // 将字符串写入到 stringstream 中
int nValue {};
double dValue {};

os >> nValue >> dValue;

std::cout << nValue << ' ' << dValue << '\n';
```

该程序打印：

```C++
12345 67.89
```

***
## 清空stringstream

有几种方法可以清空stringstream的缓冲区。

使用 str() 设置一个空的C样式字符串:

```C++
std::stringstream os {};
os << "Hello ";

os.str(""); // 清空 buffer

os << "World!";
std::cout << os.str();
```

使用 str() 设置一个空的 std::string 对象:

```C++
std::stringstream os {};
os << "Hello ";

os.str(std::string{}); // 清空 buffer

os << "World!";
std::cout << os.str();
```

这两个程序都会产生以下结果：

```C++
World!
```

设置为空后，调用clear()函数通常是一个好主意：

```C++
std::stringstream os {};
os << "Hello ";

os.str(""); // 清空 buffer
os.clear(); // 重置错误标志

os << "World!";
std::cout << os.str();
```

clear()重置可能已设置的任何错误标志，并将stream设置回ok状态。在下一课中，我们将详细讨论流的状态和错误标志。

***

{{< prevnext prev="/basic/chapter28/ostream/" next="/basic/chapter28/stream-state-validate-input/" >}}
28.2 使用ostream和ios输出
<--->
28.4 流的状态和输入验证
{{< /prevnext >}}
