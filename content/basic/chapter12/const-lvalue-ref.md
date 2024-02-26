---
title: "const的左值引用"
date: 2024-02-19T14:35:47+08:00
---

在上一课中，我们讨论了左值引用只能绑定到可修改的左值。这意味着以下内容是非法的：

```C++
int main()
{
    const int x { 5 }; // x 是不可修改的（const）左值
    int& ref { x }; // error: ref 不能绑定到 不可修改的左值

    return 0;
}
```

这是不允许的，因为我们试图通过非常量引用（ref）修改常量变量（x）。

但如果我们想要为一个常量变量来创建引用，该怎么办呢？正常的左值引用（到非常量值）是行不通的。

***
## 常量的左值引用

通过在声明左值引用时使用const关键字，我们告诉左值引用将其引用的对象视为const。这样的引用称为对常量值的左值引用（有时称为常量引用）。

对常量的左值引用可以绑定到不可修改的左值：

```C++
int main()
{
    const int x { 5 };    // x 是不可修改的左值
    const int& ref { x }; // okay: ref 可以引用到x

    return 0;
}
```

由于对常量的左值引用将它们引用的对象视为常量，因此它们可以用于访问不能修改的常量值：

```C++
#include <iostream>

int main()
{
    const int x { 5 };    // x 是不可修改的左值
    const int& ref { x }; // okay: ref 可以引用到x

    std::cout << ref << '\n'; // okay: 我们可以访问到const 变量
    ref = 6;                  // error: 不能通过常量引用修改对象
    
    return 0;
}
```

***
## 使用可修改的左值初始化对常量的左值引用

对常量的左值引用也可以绑定到可修改的左值。在这种情况下，当通过引用访问时，被引用的对象被视为常量（即使底层对象是非常量）：

```C++
#include <iostream>

int main()
{
    int x { 5 };          // x 是可修改的左值
    const int& ref { x }; // okay: ref 可以引用到x

    std::cout << ref << '\n'; // okay: 可以通过常量引用访问到 x
    ref = 7;                  // error: 不能通过常量引用修改对象

    x = 6;                // okay: x 是可修改的左值, 可以通过原始的标识符进行修改

    return 0;
}
```

在上面的程序中，我们将常量引用ref绑定到可修改的左值x。然后，我们可以使用ref访问x，但由于ref是常量，我们不能通过ref修改x的值。然而，我们仍然可以直接修改x的数值（使用标识符x）。

{{< alert success >}}
**最佳实践**

尽量使用常量引用，除非您需要修改正被引用的对象。

{{< /alert >}}

***
## 使用右值初始化对const的左值引用

也许令人惊讶的是，对常量的左值引用也可以绑定到右值：

```C++
#include <iostream>

int main()
{
    const int& ref { 5 }; // okay: 5 是一个 右值

    std::cout << ref << '\n'; // 打印 5

    return 0;
}
```

当这种情况发生时，将创建一个临时对象并用右值初始化，并且将常量引用绑定到该临时对象。

***
## 绑定到临时对象的常量引用延长了临时对象的生命周期

临时对象通常在创建它们的表达式末尾销毁。

然而，考虑一下上例，如果为右值5创建的临时对象在初始化ref的表达式的末尾被销毁，会发生什么。ref将进入悬空状态（引用已被破坏的对象），并且当我们试图访问ref时，会得到未定义的行为。

为了避免在这种情况下出现悬空引用，C++有一个特殊的规则：当常量值引用直接绑定到临时对象时，临时对象的生命周期将被扩展以匹配引用的生命周期。

```C++
#include <iostream>

int main()
{
    const int& ref { 5 }; // 值是5的临时对象，声明周期匹配 ref

    std::cout << ref << '\n'; // 因此这里可以安全的使用ref

    return 0;
} // ref和临时对象在这里被销毁
```

在上面的示例中，当使用右值5初始化ref时，将创建一个临时对象，并将ref绑定到该临时对象。临时对象的生命周期与ref的生命周期匹配。因此，我们可以在下一个语句中安全地打印ref的值。然后ref和临时对象都超出作用域，并在块的末尾被销毁。

那么，为什么C++允许常量引用绑定到右值呢？我们将在下一课中回答这个问题！

{{< alert success >}}
**关键点**

左值引用只能绑定到可修改的左值。

对常量的左值引用可以绑定到可修改的左值、不可修改的左值和右值。这使得它们成为更灵活的引用类型。

{{< /alert >}}

{{< alert success >}}
**对于高级读者**

生命周期扩展仅在常量引用直接绑定到临时对象时有效。从函数返回的临时对象（即使是常量引用返回的临时对象）不符合生命周期扩展的条件。

{{< /alert >}}

***
## Constexpr左值引用（可选阅读）

当应用于引用时，constexpr允许在常量表达式中使用引用。Constexpr引用有一个特定的限制：它们只能绑定到具有静态存储期的对象（全局或静态局部变量）。这是因为编译器知道静态对象在内存中的实例化位置，因此它可以将该地址视为编译时常量。

constexpr引用无法绑定到（非静态）局部变量。这是因为在实际调用定义局部变量的函数之前，局部变量的地址是未知的。

```C++
int g_x { 5 };

int main()
{
    [[maybe_unused]] constexpr int& ref1 { g_x }; // ok, 可以绑定到全局变量

    static int s_x { 6 };
    [[maybe_unused]] constexpr int& ref2 { s_x }; // ok, 可以绑定到静态局部变量

    int x { 6 };
    [[maybe_unused]] constexpr int& ref3 { x }; // 编译失败: 不能绑定到非静态存储期的变量

    return 0;
}
```

在将constexpr引用设置为const变量时，我们需要同时应用constexpr（适用于引用）和const（适用于被引用的类型）。

```C++
int main()
{
    static const int s_x { 6 }; // a const int
    [[maybe_unused]] constexpr const int& ref2 { s_x }; // 同时需要 constexpr 和 const

    return 0;
}
```

考虑到这些限制，constexpr引用通常没有太多用处。

***

{{< prevnext prev="/basic/chapter12/lvalue-ref/" next="/basic/chapter12/lvalue-ref-func-arg/" >}}
12.2 左值引用
<--->
12.4 通过左值引用传递函数参数
{{< /prevnext >}}
