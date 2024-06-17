---
title: "委托构造函数"
date: 2024-04-09T13:02:20+08:00
---

只要可能，我们都希望减少冗余代码（遵循DRY原则——不要重复自己）。

考虑以下功能：

```C++
void A()
{
    // 完成任务 A 的语句
}

void B()
{
    // 完成任务 A 的语句
    // 完成任务 B 的语句
}
```

这两个函数都有一组执行完全相同的操作的语句（任务A）。在这种情况下，可以这样重构：

```C++
void A()
{
    // 完成任务 A 的语句
}

void B()
{
    A();
    // 完成任务 B 的语句
}
```

通过这种方式，删除了函数A() 和B() 中存在的冗余代码。这使得代码更容易维护，因为更改只需要在一个地方进行。

当一个类包含多个构造函数时，每个构造函数中的代码即使不相同，也很相似，并且有大量重复。类似地，希望在可能的情况下删除构造函数的冗余。

考虑以下示例：

```C++
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
private:
    std::string m_name{};
    int m_id{ 0 };

public:
    Employee(std::string_view name)
        : m_name{ name }
    {
        std::cout << "Employee " << m_name << " created\n";
    }

    Employee(std::string_view name, int id)
        : m_name{ name }, m_id{ id }
    {
        std::cout << "Employee " << m_name << " created\n";
    }
};

int main()
{
    Employee e1{ "James" };
    Employee e2{ "Dave", 42 };
}
```

每个构造函数的主体打印相同的内容。

构造函数可以调用其他函数，包括类的其他成员函数。因此，可以这样重构：

```C++
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
private:
    std::string m_name{};
    int m_id{ 0 };

    void printCreated() const
    {
        std::cout << "Employee " << m_name << " created\n";
    }

public:
    Employee(std::string_view name)
        : m_name{ name }
    {
        printCreated();
    }

    Employee(std::string_view name, int id)
        : m_name{ name }, m_id{ id }
    {
        printCreated();
    }
};

int main()
{
    Employee e1{ "James" };
    Employee e2{ "Dave", 42 };
}
```

虽然这比以前的版本更好，但它需要引入一个新函数，这并不理想。

能做得更好吗？

***
## 明显的解决方案不起作用

类似于上面的示例中如何让函数B() 调用函数A() ，显而易见的解决方案是让一个Employee构造函数调用另一个构造函数。但这不会按预期工作，因为构造函数不是设计为,可以直接从另一个函数体（包括其他构造函数）调用的！

例如，您可能会认为尝试以下操作：

```C++
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
private:
    std::string m_name{};
    int m_id{ 0 };

public:
    Employee(std::string_view name)
        : m_name{ name }
    {
        std::cout << "Employee " << m_name << " created\n";
    }

    Employee(std::string_view name, int id)
        : m_name{ name }, m_id{ id }
    {
        Employee(name); // 编译失败
    }
};

int main()
{
    Employee e1{ "James" };
    Employee e2{ "Dave", 42 };
}
```

这不起作用，并将导致编译错误。

当试图在没有任何参数的情况下显式调用构造函数时，会发生更危险的情况。这不会对默认构造函数执行函数调用——相反，它会创建一个临时（未命名）对象，并对其进行值初始化！下面是一个愚蠢的示例：

```C++
#include <iostream>
struct Foo
{
    int x{};
    int y{};

public:
    Foo()
    {
        x = 5;
    }

    Foo(int value): y { value }
    {
        // 期望: 调用 Foo() 函数
        // 实际: 值初始化了一个未命名的 Foo 临时对象 (马上又会被销毁)
        Foo(); // 注: 等价于 Foo{}
    }
};

int main()
{
    Foo f{ 9 };
    std::cout << f.x << ' ' << f.y; // 打印 0 9
}
```

在本例中，Foo(int) 构造函数里有语句Foo() ，期望调用Foo() 构造函数并将值5分配给成员x。然而，该语法实际上创建了一个未命名的临时Foo，然后对其进行值初始化（就像编写了Foo{}一样）。执行 x = 5语句时，为临时Foo的x成员分配一个值。由于未使用临时对象，因此一旦完成构造，就会丢弃它。

Foo(int) 构造函数的隐式对象的x成员从未被赋值。因此，当稍后在main（）中打印出它的值时，得到的是0，而不是预期的5。

注意，这种情况不会生成编译错误——相反，它只是默默地无法产生预期的结果！

{{< alert success >}}
**警告**

不应直接从另一个函数的主体调用构造函数。这样做要么会导致编译错误，要么会对临时对象进行值初始化，然后丢弃它（这可能不是您想要的）。

{{< /alert >}}

***
## 委托构造函数

允许构造函数将初始化委托（转移责任）给同一类类型的另一个构造函数。这个过程有时被称为构造函数链接，这样的构造函数被称为委托构造函数。

要将一个构造函数的初始化委托给另一个构造函数，只需将另一个构造函数放在成员初始化列表里。应用于我们上面的示例：

```C++
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
private:
    std::string m_name{};
    int m_id{ 0 };

public:
    Employee(std::string_view name)
        : Employee{ name, 0 } // 委托给 Employee(std::string_view, int) 构造函数
    {
    }

    Employee(std::string_view name, int id)
        : m_name{ name }, m_id{ id } // 实际初始化成员
    {
        std::cout << "Employee " << m_name << " created\n";
    }

};

int main()
{
    Employee e1{ "James" };
    Employee e2{ "Dave", 42 };
}
```

初始化 e1{“James”} 时，将调用匹配的构造函数Employee(std::string_view) ，参数name设置为“James.”。该构造函数将初始化委托给其他构造函数，因此随后调用Employee(std::string_view, int) 。name（“James”）的值作为第一个参数传递，字面值0作为第二个参数传递。然后运行委托构造函数的主体执行cout语句。然后，返回到初始构造函数，其（空）主体运行。最后，控制权返回给调用者。

这种方法的缺点是，它有时需要重复初始化值。在对Employee(std::string_view, int) 构造函数的委托中，需要int参数的初始化值。必须硬编码字面值0，因为没有办法引用默认的成员初始值设定项。

关于委托构造函数的一些附加说明。首先，委托给另一个构造函数的构造函数不允许自己进行任何成员初始化。构造函数可以委托或执行初始化，但不能同时委托和初始化。

其次，一个构造函数可以委托给另一个构造函数，后者又委托回第一个构造函数。这形成了一个无限循环，并将导致程序耗尽堆栈空间并崩溃。通过确保所有构造函数都解析为非委托构造函数，可以避免这种情况。

{{< alert success >}}
**旁白**

请注意，我们将Employee(std::string_view)（参数较少的构造函数）委托给Employee(std::string_view, int)（具有更多参数的构造函数）。通常将参数较少的构造函数委托给参数较多的构造函数。

如果相反，那么这将使我们无法使用id初始化m_id，因为构造函数只能委托或初始化，而不能两者都初始化。

{{< /alert >}}

{{< alert success >}}
**最佳实践**

如果有多个构造函数，请考虑是否可以使用委托构造函数来减少重复代码。

{{< /alert >}}

***
## 使用默认参数减少构造函数

默认值有时也可以用于将多个构造函数减少为较少的构造函数。例如，通过在id参数上放置默认值，可以创建单个Employee构造函数，该构造函数需要name参数，但可以选择接受id参数：

```C++
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
private:
    std::string m_name{};
    int m_id{ 0 }; // 默认成员初始化

public:

    Employee(std::string_view name, int id = 0) // id 参数的默认值
        : m_name{ name }, m_id{ id }
    {
        std::cout << "Employee " << m_name << " created\n";
    }
};

int main()
{
    Employee e1{ "James" };
    Employee e2{ "Dave", 42 };
}
```

由于默认值必须附加到函数调用中最右侧的参数，因此定义类时的一个良好实践，是定义用户必须首先为其提供初始化值的成员（然后将这些参数设置为构造函数的最左侧参数）。有默认值的参数设置为构造函数的最右侧参数。

{{< alert success >}}
**最佳实践**

用户必须为其提供初始化值的成员应首先定义（并作为构造函数的最左侧参数）。用户可以选择为其提供初始化值（因为有默认值）的成员应其次定义（并作为构造函数的最右侧参数）。

{{< /alert >}}

***
## 一个难题：冗余构造函数与冗余默认值

在上面的例子中，使用委托构造函数，然后使用默认参数来减少构造函数冗余。但这两种方法都要求在不同的地方为成员复制初始化值。不幸的是，目前没有办法指定委托构造函数或默认参数应使用成员变量的默认值。

是使用较少的构造函数（具有重复的初始化值）还是使用较多的构造函数（不具有重复的初始值）更好，有各种各样的意见。我们的观点是，拥有较少的构造函数通常更简单，即使它会导致初始化值的重复。

{{< alert success >}}
**对于高级读者**

当有一个在多个位置使用的初始化值（例如，作为默认成员初始值设定项和构造函数参数的默认参数）时，可以改为定义一个命名常量，并在需要初始化值的地方使用它。这允许在一个位置定义初始化值。

最好的方法是在类中使用静态constexpr成员：

```C++
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
private:
    static constexpr int default_id { 0 }; // 为我们想预期的默认值定义一个命名常量
    
    std::string m_name{};
    int m_id{ default_id }; // 这里可以用

public:

    Employee(std::string_view name, int id = default_id) // 这里也可以用
        : m_name{ name }, m_id{ id }
    {
        std::cout << "Employee " << m_name << " created\n";
    }
};

int main()
{
    Employee e1{ "James" };
    Employee e2{ "Dave", 42 };
}
```

这里定义的是静态成员变量，后续进行讲解。

这种方法的缺点是，每个额外的命名常量都会添加另一个必须理解的名称，从而使类变得更加混乱和复杂。是否值得，这取决于需要多少这样的常量，以及在多少位置需要初始化值。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter14/default_construct/" next="/basic/chapter14/tmp_obj/" >}}
14.10 默认构造函数和默认参数
<--->
14.12 临时类对象
{{< /prevnext >}}
