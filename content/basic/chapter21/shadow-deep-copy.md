---
title: "浅拷贝与深拷贝"
date: 2024-08-20T12:01:51+08:00
---

## 浅拷贝

由于C++不太了解用户定义的类，因此它提供的默认拷贝构造函数和默认赋值操作符使用一种称为成员级复制（也称为浅拷贝）的复制方法。这意味着C++复制类的每个成员（对重载运算符=使用赋值运算符，对拷贝构造函数使用直接初始化）。当类很简单时（例如，不包含任何动态分配的内存），这工作得很好。

例如，让我们来看一下Fraction类：

```C++
#include <cassert>
#include <iostream>
 
class Fraction
{
private:
    int m_numerator { 0 };
    int m_denominator { 1 };
 
public:
    // 默认构造函数
    Fraction(int numerator = 0, int denominator = 1)
        : m_numerator{ numerator }
        , m_denominator{ denominator }
    {
        assert(denominator != 0);
    }
 
    friend std::ostream& operator<<(std::ostream& out, const Fraction& f1);
};
 
std::ostream& operator<<(std::ostream& out, const Fraction& f1)
{
	out << f1.m_numerator << '/' << f1.m_denominator;
	return out;
}
```

编译器为此类提供的默认拷贝构造函数和默认赋值运算符如下所示：

```C++
#include <cassert>
#include <iostream>
 
class Fraction
{
private:
    int m_numerator { 0 };
    int m_denominator { 1 };
 
public:
    // 默认构造函数
    Fraction(int numerator = 0, int denominator = 1)
        : m_numerator{ numerator }
        , m_denominator{ denominator }
    {
        assert(denominator != 0);
    }
 
    // 可能得隐式拷贝构造函数
    Fraction(const Fraction& f)
        : m_numerator{ f.m_numerator }
        , m_denominator{ f.m_denominator }
    {
    }

    // 可能的隐式赋值操作符
    Fraction& operator= (const Fraction& fraction)
    {
        // 自我赋值检查
        if (this == &fraction)
            return *this;
 
        // 进行拷贝
        m_numerator = fraction.m_numerator;
        m_denominator = fraction.m_denominator;
 
        // 返回当前对象，以便可以链式操作
        return *this;
    }

    friend std::ostream& operator<<(std::ostream& out, const Fraction& f1)
    {
	out << f1.m_numerator << '/' << f1.m_denominator;
	return out;
    }
};
```

请注意，因为这些默认版本对于复制这个类工作的很好，所以在这种情况下，确实没有理由编写这些函数的自定义版本。

然而，在设计处理动态分配内存的类时，成员级（浅层）复制会给我们带来许多麻烦！这是因为指针的副本只是复制指针的地址——它不会分配任何内存或复制所指向的内容！

让我们看一个例子：

```C++
#include <cstring> // for strlen()
#include <cassert> // for assert()

class MyString
{
private:
    char* m_data{};
    int m_length{};
 
public:
    MyString(const char* source = "" )
    {
        assert(source); // 确保source不是空指针

        // 查看 string 的长度
        // 再加一个结尾的终止符
        m_length = std::strlen(source) + 1;
        
        // 分配合适的长度
        m_data = new char[m_length];
        
        // 将输入拷贝过来
        for (int i{ 0 }; i < m_length; ++i)
            m_data[i] = source[i];
    }
 
    ~MyString() // 析构函数
    {
        // 需要清理内存
        delete[] m_data;
    }
 
    char* getString() { return m_data; }
    int getLength() { return m_length; }
};
```

上面是一个简单的字符串类，它分配内存来保存我们传入的字符串。请注意，我们没有定义拷贝构造函数或重载赋值运算符。因此，C++将提供执行浅拷贝的默认拷贝构造函数和默认赋值运算符。拷贝构造函数将如下所示：

```C++
MyString::MyString(const MyString& source)
    : m_length { source.m_length }
    , m_data { source.m_data }
{
}
```

请注意，m_data只是source.m_data的指针副本，这意味着它们现在都指向同一事物。

现在，考虑以下代码片段：

```C++
#include <iostream>

int main()
{
    MyString hello{ "Hello, world!" };
    {
        MyString copy{ hello }; // 使用默认的拷贝构造函数
    } // copy 是局部变量, 在这里销毁. 析构函数删除copy内的 m_data, 会导致 hello对象内的 m_data现在是一个悬空指针

    std::cout << hello.getString() << '\n'; // 这里会导致未定义的行为

    return 0;
}
```

虽然这段代码看起来足够无害，但它包含一个潜在的问题，这将导致程序表现出未定义的行为！

让我们逐行分解这个示例：

```C++
    MyString hello{ "Hello, world!" };
```

这行是无害的。这将调用MyString构造函数，该构造函数分配一些内存，将hello.m_data设置为指向它，然后将字符串“hello，world！”复制到其中。

```C++
    MyString copy{ hello }; // 使用默认的拷贝构造函数
```

这句话似乎也足够无害，但它实际上是问题的根源！当运行这一行时，C++将使用默认的拷贝构造函数（因为我们没有提供自己的）。此拷贝构造函数将执行浅拷贝，将copy.m_data初始化为hello.m_data的相同地址。因此，copy.m_data和hello.m.data现在都指向同一块内存！

```C++
} // copy 是局部变量, 在这里销毁
```

当copy超出作用域时，调用MyString析构函数。析构函数删除copy.m_data和hello.m_data都指向的动态分配的内存！因此，通过删除copy，我们也（无意中）影响了hello。变量copy随后被销毁，但hello.m_data仍指向已删除（无效）的内存！

```C++
    std::cout << hello.getString() << '\n'; // 这里会导致未定义的行为
```

现在您可以看到为什么该程序具有未定义的行为。我们删除了hello指向的字符串，试图打印不再有效的内存值。

这个问题的根源是拷贝构造函数进行的浅拷贝——在拷贝构造函数或重载赋值运算符中对指针值进行浅拷贝几乎总是会带来麻烦。

***
## 深拷贝

这个问题的一个答案是对正在复制的任何非空指针进行深拷贝。深拷贝为副本分配内存，然后复制实际值，以便副本位于与源对象不同的内存中。这样，副本和源对象是不同的，不会以任何方式相互影响。进行深拷贝需要我们编写自己的拷贝构造函数和重载赋值运算符。

让我们继续展示如何为MyString类完成这一点：

```C++
// 假设 m_data 已经初始化了
void MyString::deepCopy(const MyString& source)
{
    // 首先删除之前保存的数据!
    delete[] m_data;

    // 因为 m_length 不是指针, 所以可以直接赋值
    m_length = source.m_length;

    // m_data 是指针, 需要进行深拷贝
    if (source.m_data)
    {
        // 分配内存
        m_data = new char[m_length];

        // 进行拷贝
        for (int i{ 0 }; i < m_length; ++i)
            m_data[i] = source.m_data[i];
    }
    else
        m_data = nullptr;
}

// 拷贝构造函数
MyString::MyString(const MyString& source)
{
    deepCopy(source);
}
```

正如您所看到的，这比简单的浅拷贝要复杂得多！首先，我们必须检查以确保source有值。如果有值，那么分配足够的内存来保存该字符串的副本。最后，必须手动复制字符串。

现在，让我们看下重载赋值运算符。重载赋值运算符稍微复杂一些：

```C++
// 赋值运算符
MyString& MyString::operator=(const MyString& source)
{
    // 做自赋值检查
    if (this != &source)
    {
        // 执行深拷贝
        deepCopy(source);
    }

    return *this;
}
```

请注意，我们的赋值运算符与拷贝构造函数非常相似，但有三个主要区别：

1. 添加了自我赋值检查。
2. 返回*this，这样就可以链接赋值运算符。
3. 需要显式地释放字符串已经持有的任何值（以便在稍后重新分配m_data时不会出现内存泄漏）。这在deepCopy（）中处理。


当调用重载赋值运算符时，被赋值的项可能已经包含以前的值，需要确保在为新值分配内存之前清理该值。对于非动态分配的变量（大小固定），我们不必费心，因为新值只是覆盖旧值。然而，对于动态分配的变量，需要在分配任何新内存之前显式地释放任何旧内存。如果不这样做，虽然代码将不会崩溃，但将有一个内存泄漏的地方，每次做一次赋值，都会吞噬一部分内存！

***
## 类的构造析构与赋值

如果类需要用户定义的析构函数、拷贝构造函数或复制赋值运算符的一个，则它可能需要所有的这三个运算符。为什么？如果用户定义这些函数中的任何一个，那可能是因为正在处理动态内存分配。需要拷贝构造函数和拷贝赋值来处理深拷贝，需要析构函数来释放内存。

***
## 更好的解决方案

标准库中有处理动态内存的类，如std::string和std::vector，它们负责其持有内存管理，并具有执行适当深拷贝的拷贝构造函数和重载赋值运算符。因此，您可以像普通的基本变量那样初始化或分配它们，而不是自己进行内存管理！这使得这些类更易于使用，不太容易出错，并且您不必花时间编写自己的重载函数！

***
## 总结

1. 默认拷贝构造函数和默认赋值运算符执行浅拷贝，这对于不包含动态分配的变量的类很好。
2. 具有动态分配变量的类需要有一个拷贝构造函数和赋值运算符来执行深拷贝。
3. 与自己进行内存管理相比，优先使用标准库中的类。

***

{{< prevnext prev="/basic/chapter21/assign-op-overload/" next="/basic/chapter21/op-overload-template/" >}}
21.11 重载赋值运算符
<--->
21.13 重载运算符和函数模板
{{< /prevnext >}}
