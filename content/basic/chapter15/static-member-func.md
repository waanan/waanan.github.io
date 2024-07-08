---
title: "静态成员函数"
date: 2024-06-24T18:56:16+08:00
---

在上一课中，我们了解到静态成员变量是属于类的成员变量，而不属于类的对象。如果静态成员变量是public的，则可以使用类名和域解析操作符直接访问它：

```C++
#include <iostream>

class Something
{
public:
    static inline int s_value { 1 };
};

int main()
{
    std::cout << Something::s_value; // s_value 是 public, 可以直接访问
}
```

但如果静态成员变量是私有的呢？考虑以下示例：

```C++
#include <iostream>

class Something
{
private: // 现在是 private
    static inline int s_value { 1 };
};

int main()
{
    std::cout << Something::s_value; // error: s_value 是 private，无法在类的外部直接访问
}
```

在这种情况下，不能直接从 main() 访问Something::s_value，因为它是私有的。通常，通过公共成员函数访问私有成员。虽然可以创建一个普通的公共成员函数来访问s_value，但这需要实例化类类型的对象才能使用该函数！

```C++
#include <iostream>

class Something
{
private:
    static inline int s_value { 1 };

public:
    int getValue() { return s_value; }
};

int main()
{
    Something s{};
    std::cout << s.getValue(); // 可以, 但必须先实例化一个对象才能调用 getValue()
}
```

可以做得更好。

***
## 静态成员函数

成员变量不是唯一可以设置为静态的成员类型。成员函数也可以设置为静态。下面是具有静态成员函数访问器的示例：

```C++
#include <iostream>

class Something
{
private:
    static inline int s_value { 1 };

public:
    static int getValue() { return s_value; } // static 成员函数
};

int main()
{
    std::cout << Something::getValue() << '\n';
}
```

由于静态成员函数不与特定对象关联，因此可以使用类名和域解析操作符（ 例如Something::getValue() ）直接调用它们。与静态成员变量一样，它们也可以通过类类型的对象调用，但不建议这样做。

***
## 静态成员函数没有this指针

静态成员函数有两个值得注意的奇怪之处。首先，因为静态成员函数没有附加到对象，所以它们没有this指针！这是有意义的——this指针始终指向成员函数正在处理的对象。静态成员函数不在对象上工作，因此不需要this指针。

其次，静态成员函数可以直接访问其他静态成员（变量或函数），但不能访问非静态成员。这是因为非静态成员必须属于类对象，并且静态成员函数没有可使用的类对象！

***
## 在类定义外部定义的静态成员

静态成员函数也可以在类声明之外定义。这与普通成员函数的工作方式相同。

```C++
#include <iostream>

class IDGenerator
{
private:
    static inline int s_nextID { 1 };

public:
     static int getNextID(); // 这里是静态成员函数声明
};

// 这里是类外部的静态成员函数定义，注意这里没有加 static 关键字
int IDGenerator::getNextID() { return s_nextID++; } 

int main()
{
    for (int count{ 0 }; count < 5; ++count)
        std::cout << "The next ID is: " << IDGenerator::getNextID() << '\n';

    return 0;
}
```

该程序打印：

```C++
The next ID is: 1
The next ID is: 2
The next ID is: 3
The next ID is: 4
The next ID is: 5
```

注意，因为这个类中的所有数据和函数都是静态的，所以不需要实例化类的对象来使用它的函数！该类使用静态成员变量来保存要分配的下一个ID的值，并提供一个静态成员函数来返回该ID并对其进行递增。

在类定义中定义的成员函数隐式内联。在类定义外部定义的成员函数不是隐式内联的，但可以使用inline关键字内联。因此，在头文件中定义的静态成员函数应该内联，以便在随后将该头文件包含在多个翻译单元中时不违反“单定义规则”（ODR）。

***
## 关于具有所有静态成员的类的警告

编写全是静态成员的类时要小心。尽管这种“纯静态类”可能有用，但它们也有一些潜在的缺点。

首先，因为所有静态成员都只实例化一次，所以没有办法拥有纯静态类的多个副本（无法拷贝类对象并重命名它）。例如，如果您需要两个独立的IDGenerator，这对于纯静态类是不可能的。

其次，在关于全局变量的课程中，了解到全局变量是危险的，因为任何代码片段都可以更改全局变量的值，并最终破坏另一段看似无关的代码。对于纯静态类也是如此。由于所有成员都属于类（而不是类的对象），并且类声明通常具有全局范围，因此纯静态类本质上相当于在全局可访问的命名空间中声明函数和全局变量，具有全局变量所具有的所有缺点。

与其编写全是静态成员的类，不如考虑编写一个普通类并实例化它的全局实例（全局变量具有静态存储期）。这样，可以在适当的时候使用全局实例，但仍然可以进行实例化其它实例。

***
## 纯静态类与命名空间

纯静态类与命名空间有许多重叠。两者都允许您定义具有静态存储期变量，并在其作用域内定义函数。然而，一个显著的区别是类具有访问控制，而命名空间没有。

通常，当您有静态数据成员和/或需要访问控制时，最好使用静态类。否则，首选命名空间。

***
## C++不支持静态构造函数

如果可以通过构造函数初始化普通成员变量，那么您应该能够通过静态构造函数初始化静态成员变量。虽然一些现代语言确实支持静态构造函数来实现这一目的，但不幸的是C++不是其中之一。

如果可以直接初始化静态变量，则不需要构造函数：您可以在定义点初始化静态成员变量（即使它是私有的）。在上面的IDGenerator示例中这样做。下面是另一个示例：

```C++
#include <iostream>

struct Chars
{
    char first{};
    char second{};
    char third{};
    char fourth{};
    char fifth{};
};

struct MyClass
{
	static inline Chars s_mychars { 'a', 'e', 'i', 'o', 'u' }; // 在定义点初始化静态成员变量
};

int main()
{
    std::cout << MyClass::s_mychars.third; // 打印 i

    return 0;
}
```

如果初始化静态成员变量需要执行代码（例如循环），那么有许多不同的、有些迟钝的方法可以做到这一点。处理所有变量（静态或非静态）的一种方法是使用函数创建对象，用数据填充它，并将其返回给调用方。该返回值可以拷贝到正在初始化的对象中。

```C++
#include <iostream>

struct Chars
{
    char first{};
    char second{};
    char third{};
    char fourth{};
    char fifth{};
};

class MyClass
{
private:
    static Chars generate()
    {
        Chars c{}; // 创建一个对象
        c.first = 'a'; // 填充值
        c.second = 'e';
        c.third = 'i';
        c.fourth = 'o';
        c.fifth = 'u';
        
        return c; // 返回对象
    }

public:
	static inline Chars s_mychars { generate() }; // 将返回的对象填充到 s_mychars
};

int main()
{
    std::cout << MyClass::s_mychars.third; // 打印 i

    return 0;
}
```

在前面讲解随机数时，我们展示过这样的技巧（尽管我们使用命名空间而不是静态类来实现，但它的工作方式相同）

{{< alert success >}}
**相关内容**

lambda也可以用于此。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter15/static-member-var/" next="/basic/chapter15/friend-no-member-func/" >}}
15.5 静态成员变量
<--->
15.7 友元非成员函数
{{< /prevnext >}}
