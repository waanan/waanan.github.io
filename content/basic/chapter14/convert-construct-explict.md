---
title: "转换构造函数和explicit关键字"
date: 2024-04-09T13:02:20+08:00
---

在前面，我们介绍了类型转换和隐式类型转化的概念，编译器将根据需要隐式地将一种类型的值转换为另一种类型（如果存在这样的转换方式）的值。

这允许这样做：

```C++
#include <iostream>

void printDouble(double d) // 参数为 double
{
    std::cout << d;
}

int main()
{
    printDouble(5); // 使用 int 来调用

    return 0;
}
```

在上面的示例中，printDouble函数有一个double参数，但传入了一个int类型的值。由于参数的类型和传入值的类型不匹配，编译器将查看是否可以隐式地将int值转换为double值。在这种情况下，使用数值转换规则，int值5将被转换为double值5.0，因为是通过值传递的，所以参数d将用该值进行拷贝初始化。

***
## 用户定义的转换

现在考虑以下类似的示例：

```C++
#include <iostream>

class Foo
{
private:
    int m_x{};
public:
    Foo(int x)
        : m_x{ x }
    {
    }

    int getX() const { return m_x; }
};

void printFoo(Foo f) // 参数为 Foo
{
    std::cout << f.getX();
}

int main()
{
    printFoo(5); // 输入为 int

    return 0;
}
```

在此版本中，printFoo有一个Foo参数，但传入了一个int类型的数据。由于类型不匹配，编译器将尝试将int值5隐式转换为Foo对象，以便可以调用函数。

上一个示例中的参数和传入数据的类型都是基本类型（因此可以使用内置的数值提升/转换规则进行转换），在当前情况下，参数类型是程序定义的类型。C++没有特定的规则来告诉编译器如何将基本类型的值转换为程序定义的类型。

相反，编译器将查看是否定义了一些函数，可以使用这些函数来执行这种转换。这样的函数称为用户定义的转换。

***
## 转换构造函数

在上面的示例中，编译器将找到一个函数，该函数允许它将int值5转换为Foo对象。该函数是 Foo(int) 构造函数。

到目前为止，通常使用构造函数来显式构造对象：

```C++
    Foo x { 5 }; // 显式将 int 值 5 转换为 Foo
```

考虑一下它的作用：提供一个int值（5），并获得一个Foo对象作为返回。

在函数调用的上下文中，试图解决相同的问题：

```C++
    printFoo(5); // 隐式将 int 值 5 转换为 Foo
```

提供了一个int值（5），并且希望返回一个Foo对象。Foo(int) 构造函数就是为此而设计的！

因此，在这种情况下，当调用 printFoo(5) 时，使用 Foo(int) 构造函数，并将5作为参数f！

可以用于执行隐式转换的构造函数称为转换构造函数。默认情况下，所有构造函数都是转换构造函数。

***
## 只能应用一次用户定义的转换

现在考虑以下示例：

```C++
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
private:
    std::string m_name{};

public:
    Employee(std::string_view name)
        : m_name{ name }
    {
    }

    const std::string& getName() const { return m_name; }
};

void printEmployee(Employee e) // 参数为 Employee
{
    std::cout << e.getName();
}

int main()
{
    printEmployee("Joe"); // 提供的是一个字符串字面值

    return 0;
}
```

在这个版本中，将Foo类替换为Employee类。printEmployee有一个Employme参数，传入一个C样式的字符串文本。同时有一个转换构造函数：Employee(std::string_view)。

您可能会惊讶地发现，这个版本不能编译。原因很简单：只能应用一次用户定义的转换来执行隐式转换，而这个示例需要两次。首先，必须将C样式的字符串文本转换为std::string_view（使用std:∶string_view转换构造函数），然后必须将std::string_view转换为Employee（使用 Employer(std:；string_view) 转换构造函数）。

有两种方法可以使此示例工作：

```C++
int main()
{
    using namespace std::literals;
    printEmployee( "Joe"sv); // 现在是 std::string_view 字面值了

    return 0;
}
```

这是可行的，因为现在只需要一个用户定义的转换（从std::string_view到Employee）。

```C++
int main()
{
    printEmployee(Employee{ "Joe" });

    return 0;
}
```

这也可以工作，因为现在只需要一个用户定义的转换（从字符串文本到用于初始化Employee对象的std::string_view）。将显式构造的Employee对象传递给函数不需要进行第二次转换。

后一个示例提供了一种有用的技术：将隐式转换替换为显式定义。在本课后面的部分中，将看到更多的例子。

{{< alert success >}}
**关键点**

通过使用直接列表初始化（或直接初始化），可以将隐式转换替换为显式定义。

{{< /alert >}}

***
## 转换构造函数导致的预期外的行为

考虑以下程序：

```C++
#include <iostream>

class Dollars
{
private:
    int m_dollars{};

public:
    Dollars(int d)
        : m_dollars{ d }
    {
    }

    int getDollars() const { return m_dollars; }
};

void print(Dollars d)
{
    std::cout << "$" << d.getDollars();
}

int main()
{
    print(5);

    return 0;
}
```

当调用print(5) 时，Dollars(int) 转换构造函数将5转换为Dollars对象。因此，该程序打印：

```C++
$5
```

尽管这可能是代码编写者的意图，但很难说清楚。调用者完全有可能假设这将打印5，并且不期望编译器以静默和隐式的方式将int值转换为Dollars对象，以便可以满足此函数调用。

虽然这个例子很简单，但在一个更大、更复杂的程序中，编译器执行一些您没有预料到的隐式转换，从而在运行时导致意外行为，这很容易让人感到惊讶。

如果 print(Dollars) 函数只能用Dollars对象调用，而不是用可以隐式转换为Dollars的任何值（特别是像int这样的基本类型），那就更好了。这将减少意外错误的可能性。

***
## explict关键字

为了解决这样的问题，可以使用explict关键字来告诉编译器，构造函数不应该用作转换构造函数。

使构造函数explict有两个显著的后果：

1. explict构造函数不能用于执行拷贝初始化或拷贝列表初始化。
2. explict构造函数不能用于执行隐式转换（因为它使用拷贝初始化或拷贝列表初始化）。


将上例中的Dollars(int) 构造函数更新为explict构造函数：

```C++
 #include <iostream>

class Dollars
{
private:
    int m_dollars{};

public:
    explicit Dollars(int d) // 现在是 explicit
        : m_dollars{ d }
    {
    }

    int getDollars() const { return m_dollars; }
};

void print(Dollars d)
{
    std::cout << "$" << d.getDollars();
}

int main()
{
    print(5); // 编译失败，因为 Dollars(int) 是 explicit

    return 0;
}
```

由于编译器不能再使用 Dollars(int) 作为转换构造函数，因此它无法找到将5转换为Dollars的方法。因此，它将生成编译错误。

***
## explict构造函数可用于直接初始化和列表初始化

explict构造函数仍然可以用于直接和直接列表初始化：

```C++
// 假设为 Dollars(int) 是 explicit
int main()
{
    Dollars d1(5); // ok
    Dollars d2{5}; // ok
}
```

现在，回到前面的示例，在那里创建了 explicit Dollars(int) 构造函数，因此下面生成了一个编译错误：

```C++
    print(5); // 编译失败，因为 Dollars(int) 是 explicit
```

如果确实想用int值5调用print()，但构造函数是explicit的，该怎么办？解决方法很简单：可以自己显式定义Dollars对象，而不是让编译器将5隐式转换为可以传递给print()的Dollars：

```C++
    print(Dollars{5}); // ok: 创建 Dollars 并传给 print() (不再需要转换)
```

这是允许的，因为仍然可以使用显式构造函数来列表初始化对象。由于现在已经显式构造了一个Dollars，因此参数类型与传入数据类型匹配，因此不需要转换！

这不仅可以编译和运行，还可以更好地记录意图，因为它明确了打算用Dollars对象调用该函数的事实。

***
## 按值返回和explict构造函数

当从函数中返回值时，如果该值与函数的返回类型不匹配，则将发生隐式转换。就像传递值一样，这种转换不能使用explict构造函数。

以下程序显示了返回值的一些变化及其结果：

```C++
#include <iostream>

class Foo
{
public:
    explicit Foo() // explicit
    {
    }

    explicit Foo(int x) // explicit
    {
    }
};

Foo getFoo()
{
    // explicit Foo()
    return Foo{ };   // ok
    return { };      // 错误: 不能隐式的列表初始化Foo

    // explicit Foo(int)
    return 5;        // 错误: 不能隐式的将 int 转换为 Foo
    return Foo{ 5 }; // ok
    return { 5 };    // 错误: 不能隐式的将初始化列表转换为 Foo
}

int main()
{
    return 0;
}
```

也许令人惊讶的是，返回{5}被认为是转换。

***
## 使用explict的最佳实践

现代最佳实践是使默认情况下接受单个参数的任何构造函数标记为explict。也包括大多数或全部参数有默认值的有多个参数的构造函数。

这将禁止编译器使用该构造函数进行隐式转换。

如果在特定情况下实际需要这样的转换，则使用列表初始化将隐式转换转换改写为显式定义是很容易的。

以下构造函数不应标记explict：

1. 复制（和移动）构造函数（因为它们不执行转换）。

以下构造函数通常不应标记explict：

1. 没有参数的默认构造函数（因为它们仅用于将{}转换为默认对象）。
2. 仅接受多个参数的构造函数。


在某些情况下，将单参数构造函数设置为非explict是有意义的。当以下所有条件都为真时，这可能很有用：

1. 转换的值在语义上等同于参数值。
2. 转换是性能更好的。

例如，接收C样式字符串，参数类型为std::string_view的构造函数不是explict的，因为不太可能出现这样的情况，即我们不同意将C样式字符串视为std::string_view。

相反，接收std::string_view，参数类型std::string构造函数需要标记为explict，因为虽然std:∶string值在语义上等同于std::string_view值，但构造std::string代价较高。

{{< alert success >}}
**最佳实践**

默认情况下，使任何接受单个参数的构造函数explict。如果类型之间的隐式转换在语义上等效，并且是性能更好的转换，则可以考虑使构造函数非explict。

不要标记拷贝或移动构造函数explict，因为它们不执行转换。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter14/class-init-copy-elision/" next="/basic/chapter14/summary/" >}}
14.14 类初始化和拷贝省略
<--->
14.16 第14章总结
{{< /prevnext >}}
