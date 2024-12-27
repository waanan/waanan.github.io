---
title: "纯虚函数、抽象基类和接口类"
date: 2024-11-04T13:14:53+08:00
---

到目前为止，我们编写的所有虚函数都有函数体（定义）。然而，C++允许您创建一种特殊的虚函数，称为完全没有函数体的纯虚函数（或抽象函数）！纯虚函数仅充当占位符，该占位符的目的是标明，这个函数需要由派生类重新定义。

为了创建纯虚函数，我们只需将值0赋值给函数。

```C++
#include <string_view>

class Base
{
public:
    std::string_view sayHi() const { return "Hi"; } // 普通非虚函数

    virtual std::string_view getName() const { return "Base"; } // 普通虚函数

    virtual int getValue() const = 0; // 纯虚函数

    int doSomething() = 0; // 编译失败: 无法将非虚函数设置为0
};
```

当我们向类中添加纯虚函数时，我们实际上是在说，“需要由派生类来实现该函数”。

使用纯虚函数有两个主要目标：首先，任何具有一个或多个纯虚函数的类都成为抽象基类，这意味着它不能被实例化！考虑如果我们想创建Base:

```C++
int main()
{
    Base base {}; // 不允许实例化抽象基类
    base.getValue(); // 这一行会发生什么呢?

    return 0;
}
```

因为没有getValue()的定义，所以base.getValue()无法解析。

其次，任何派生类都必须为此函数定义主体，否则该派生类也将被视为抽象基类。

## 一个纯虚函数的例子

让我们来看一个纯虚函数的例子。在上一课中，我们编写了一个简单的Animal基类，并从中派生了一个Cat和一个Dog类。下面是我们留下的代码：

```C++
#include <string>
#include <string_view>

class Animal
{
protected:
    std::string m_name {};

    // 将构造函数设置为 protected
    // 因为不想任何人可以直接创建Animal对象
    // 但是派生类可以使用这个构造函数
    Animal(std::string_view name)
        : m_name{ name }
    {
    }

public:
    const std::string& getName() const { return m_name; }
    virtual std::string_view speak() const { return "???"; }

    virtual ~Animal() = default;
};

class Cat: public Animal
{
public:
    Cat(std::string_view name)
        : Animal{ name }
    {
    }

    std::string_view speak() const override { return "Meow"; }
};

class Dog: public Animal
{
public:
    Dog(std::string_view name)
        : Animal{ name }
    {
    }

    std::string_view speak() const override { return "Woof"; }
};
```

我们通过protected构造函数来防止人们分配Animal类型的对象。然而，仍然可以创建不重新定义函数speak()的派生类。

例如：

```C++
#include <iostream>
#include <string>
#include <string_view>

class Animal
{
protected:
    std::string m_name {};

    // 将构造函数设置为 protected
    // 因为不想任何人可以直接创建Animal对象
    // 但是派生类可以使用这个构造函数
    Animal(std::string_view name)
        : m_name{ name }
    {
    }

public:
    const std::string& getName() const { return m_name; }
    virtual std::string_view speak() const { return "???"; }

    virtual ~Animal() = default;
};

class Cow : public Animal
{
public:
    Cow(std::string_view name)
        : Animal{ name }
    {
    }

    // 这里忘记重新定义 speak
};

int main()
{
    Cow cow{"Betsy"};
    std::cout << cow.getName() << " says " << cow.speak() << '\n';

    return 0;
}
```

这将打印：

```C++
Betsy says ???
```

发生了什么事？我们忘了重新定义函数speak()。cow.speak()解析为Animal.Speak()，这不是我们想要的。

这个问题的更好的解决方案是使用纯虚函数：

```C++
#include <string>
#include <string_view>

class Animal // This Animal is an abstract base class
{
protected:
    std::string m_name {};

public:
    Animal(std::string_view name)
        : m_name{ name }
    {
    }

    const std::string& getName() const { return m_name; }
    virtual std::string_view speak() const = 0; // 注意speak现在是纯虚函数

    virtual ~Animal() = default;
};
```

这里有几点需要注意。首先，speak()现在是一个纯虚函数。这意味着Animal现在是一个抽象基类，不能被实例化。因此，我们不需要再保护构造函数（尽管它不会造成伤害）。其次，因为我们的Cow类是从Animal派生的，但我们没有定义Cow::speak（），所以Cow也是一个抽象基类。现在，当我们试图编译这段代码时：

```C++
#include <iostream>
#include <string>
#include <string_view>

class Animal // Animal 现在是一个抽象基类
{
protected:
    std::string m_name {};

public:
    Animal(std::string_view name)
        : m_name{ name }
    {
    }

    const std::string& getName() const { return m_name; }
    virtual std::string_view speak() const = 0; // 注意 speak 现在是一个纯虚函数

    virtual ~Animal() = default;
};

class Cow: public Animal
{
public:
    Cow(std::string_view name)
        : Animal{ name }
    {
    }

    // 这里忘记重新定义 speak
};

int main()
{
    Cow cow{ "Betsy" };
    std::cout << cow.getName() << " says " << cow.speak() << '\n';

    return 0;
}
```

编译器将给出错误，因为Cow是抽象基类，我们无法创建抽象基类的实例：

```C++
prog.cc:35:9: error: variable type 'Cow' is an abstract class
   35 |     Cow cow{ "Betsy" };
      |         ^
prog.cc:17:30: note: unimplemented pure virtual method 'speak' in 'Cow'
   17 |     virtual std::string_view speak() const = 0; // 注意 speak 现在是一个纯虚函数
      |                              ^
```

这告诉我们，只有当Cow为speak()提供函数体时，我们才能实例化Cow。

让我们继续修改：

```C++
#include <iostream>
#include <string>
#include <string_view>

class Animal // Animal 现在是一个抽象基类
{
protected:
    std::string m_name {};

public:
    Animal(std::string_view name)
        : m_name{ name }
    {
    }

    const std::string& getName() const { return m_name; }
    virtual std::string_view speak() const = 0; // 注意 speak 现在是一个纯虚函数

    virtual ~Animal() = default;
};

class Cow: public Animal
{
public:
    Cow(std::string_view name)
        : Animal(name)
    {
    }

    std::string_view speak() const override { return "Moo"; }
};

int main()
{
    Cow cow{ "Betsy" };
    std::cout << cow.getName() << " says " << cow.speak() << '\n';

    return 0;
}
```

现在，这个程序将编译和打印：

```C++
Betsy says Moo
```

当我们有一个要放入基类的函数，但只有派生类知道具体的行为时，纯虚函数是有用的。纯虚函数使我们无法实例化基类，并且派生类在实例化之前必须定义这些函数。这有助于确保派生类不会忘记定义这些函数。

就像普通虚函数一样，可以使用基类的引用（或指针）来调用纯虚函数：

```C++
int main()
{
    Cow cow{ "Betsy" };
    Animal& a{ cow };

    std::cout << a.speak(); // 指向 to Cow::speak(), 打印 "Moo"

    return 0;
}
```

在上面的示例中，a.speak() 通过虚函数解析为Cow::speak()。

注意，具有纯虚函数的任何类也应该具有虚析构函数。

## 带定义的纯虚函数

我们可以创建具有定义的纯虚函数：

```C++
#include <string>
#include <string_view>

class Animal // Animal 是抽象基类
{
protected:
    std::string m_name {};

public:
    Animal(std::string_view name)
        : m_name{ name }
    {
    }

    const std::string& getName() { return m_name; }
    virtual std::string_view speak() const = 0; // = 0 意味着这个函数是纯虚函数

    virtual ~Animal() = default;
};

std::string_view Animal::speak() const  // 但是它仍然有一个函数定义
{
    return "buzz";
}
```

在这种情况下，由于“=0”（即使它已经给出了一个定义），speak()仍然被认为是纯虚函数，Animal仍然被视为抽象基类（因此不能被实例化）。从Animal继承的任何类都需要为speak()提供自己的定义，否则它也将被视为抽象基类。

为纯虚函数提供定义时，必须单独提供定义（而不是放在类内部）。

当您希望基类为函数提供默认实现，但仍然强制任何派生类提供自己的实现时，此范例可能很有用。如果派生类对基类提供的默认实现满意，它可以直接调用基类实现。例如：

```C++
#include <iostream>
#include <string>
#include <string_view>

class Animal // Animal 是抽象基类
{
protected:
    std::string m_name {};

public:
    Animal(std::string_view name)
        : m_name(name)
    {
    }

    const std::string& getName() const { return m_name; }
    virtual std::string_view speak() const = 0; // 注意speak是纯虚函数

    virtual ~Animal() = default;
};

std::string_view Animal::speak() const
{
    return "buzz"; // 默认的一些实现
}

class Dragonfly: public Animal
{

public:
    Dragonfly(std::string_view name)
        : Animal{name}
    {
    }

    std::string_view speak() const override // 因为有定义，所以不再是纯虚函数
    {
        return Animal::speak(); // 使用 Animal 的默认实现
    }
};

int main()
{
    Dragonfly dfly{"Sally"};
    std::cout << dfly.getName() << " says " << dfly.speak() << '\n';

    return 0;
}
```

上面的代码打印：

```C++
Sally says buzz
```

这个功能并不常用。

析构函数可以成为纯虚拟的，但必须给出定义，以便在派生对象被析构时可以调用它。


## 接口类

接口类是一个没有成员变量的类，其中所有函数都是纯虚函数！当您想要定义派生类必须实现的功能时，接口非常有用，将派生类如何实现该功能的细节完全留给派生类。

接口类通常以I开头命名。下面是一个示例接口类：

```C++
#include <string_view>

class IErrorLog
{
public:
    virtual bool openLog(std::string_view filename) = 0;
    virtual bool closeLog() = 0;

    virtual bool writeError(std::string_view errorMessage) = 0;

    virtual ~IErrorLog() {} // 有virtual函数的类，析构函数也必需是virtual
};
```

从IErrorLog继承的任何类都必须为所有三个函数提供实现，才能被实例化。您可以派生一个名为FileErrorLog的类，其中openLog()在磁盘上打开一个文件，closeLog()关闭该文件，writeError()将消息写入该文件。您可以派生另一个名为ScreenErrorLog的类，其中openLog()和closeLog()什么也不做，writeError()将消息打印到屏幕上。

现在，假设您需要编写一些使用错误日志的代码。如果您编写的代码直接包含FileErrorLog或ScreenErrorLog。那么实际上，您将难以替换使用另一个Log类（至少在不重新编写程序的情况下）。例如，下面的函数强制mySqrt()的调用方使用FileErrorLog，这可能是他们想要的，也可能不是他们想要的。

```C++
#include <cmath> // for sqrt()

double mySqrt(double value, FileErrorLog& log)
{
    if (value < 0.0)
    {
        log.writeError("Tried to take square root of value less than 0");
        return 0.0;
    }

    return std::sqrt(value);
}
```

实现该函数的一种更好的方法是使用IErrorLog:

```C++
#include <cmath> // for sqrt()
double mySqrt(double value, IErrorLog& log)
{
    if (value < 0.0)
    {
        log.writeError("Tried to take square root of value less than 0");
        return 0.0;
    }

    return std::sqrt(value);
}
```

现在，调用者可以传入符合IErrorLog接口的任何类。如果他们希望错误转到文件，则可以传入FileErrorLog的实例。如果他们希望它转到屏幕，则可以传入ScreenErrorLog的实例。或者，如果他们想做一些您甚至没有想到的事情，例如在出现错误时向某人发送电子邮件，他们可以从IErrorLog派生一个新类（例如EmailErrorLog），并使用该类的实例！通过使用IErrorLog，您的函数变得更加独立和灵活。

不要忘记为接口类添加虚析构函数，以便在删除指针时调用适当的派生析构函数。

接口类非常流行，因为它们易于使用、易于扩展和易于维护。事实上，一些现代语言（如Java和C#）添加了“interface”关键字，允许程序员直接定义接口类，而不必将所有成员函数显式标记为纯虚函数。此外，尽管Java和C#不允许在普通类上使用多重继承，但它们将允许您根据需要，继承任意多个接口。因为接口并没有数据和函数体，所以它们避免了许多多重继承的传统问题，同时仍然提供了很大的灵活性。

## 纯虚函数和虚函数表

为了一致性，抽象类仍然具有虚函数表。抽象类的构造函数或析构函数可以调用虚函数，它需要解析为适当的函数（因为派生类可能尚未构造或已被销毁）。

只有纯虚函数的类的虚函数表条目通常要么包含空指针，要么指向打印错误的函数（有时该函数名为__purecall）。

***

{{< prevnext prev="/basic/chapter25/virtual-table/" next="/" >}}
25.5 虚函数表
<--->
主页
{{< /prevnext >}}
