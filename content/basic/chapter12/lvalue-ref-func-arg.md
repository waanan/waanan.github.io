---
title: "通过左值引用传递函数参数"
date: 2024-02-19T14:35:47+08:00
---

在前面的课程中，我们介绍了左值引用。孤立地说，这些可能并不太有用——当可以使用变量本身时，为什么要创建变量的别名？

在本课中，将最终提供一些关于引用有用的原因。然后从本章后面开始，您将看到引用被经常使用。

首先，回忆一下函数参数传递，其中传递给函数的值被复制到函数的参数中:

```C++
#include <iostream>

void printValue(int y)
{
    std::cout << y << '\n';
} // y 在这里被销毁

int main()
{
    int x { 2 };

    printValue(x); // x 按值拷贝到 y (如果x是比较大的对象，会非常消耗资源)

    return 0;
}
```

在上面的程序中，当调用printValue(x)时，将x（2）的值复制到参数y中。然后，在函数的末尾，销毁对象y。

这意味着当我们调用函数时，我们复制了参数的值，只是简单地使用它，然后销毁它！幸运的是，因为基本类型的复制成本很低，所以这不是问题。

***
## 某些对象的复制成本很高

标准库提供的大多数类型（如std::string）都是类类型。类类型的复制成本通常很高。只要可能，我们都希望避免为复制成本高昂的对象制作不必要的副本，特别是当我们几乎要立即销毁这些副本时。

考虑以下程序来说明这一点:

```C++
#include <iostream>
#include <string>

void printValue(std::string y)
{
    std::cout << y << '\n';
} // y 在这里被销毁

int main()
{
    std::string x { "Hello, world!" }; // x 是 std::string

    printValue(x); // x 按值拷贝到 y (复制成本高)

    return 0;
}
```

打印:

```C++
Hello, world!
```

虽然该程序的行为与我们预期的一样，但它也是低效的。与前一个示例相同，当调用printValue()时，x被复制到printValue()的参数y中。然而，在这个示例中，参数是std::string而不是int，std::string是复制成本很高的类类型。每次调用printValue()时都会生成这个昂贵的副本！

可以做得更好。

***
## 引用传递参数

在调用函数时，避免生成参数的昂贵副本的一种方法是按引用传递参数，而不是按值传递。当使用按引用传递时，我们将函数参数声明为引用类型（或常量引用类型），而不是普通类型。调用函数时，每个引用参数都绑定到适当的实际值。因为引用充当参数的别名，所以不会制作参数的副本。

下面是与上面相同的示例，使用按引用传递而不是按值传递:

```C++
#include <iostream>
#include <string>

void printValue(std::string& y) // 类型更改为 std::string&
{
    std::cout << y << '\n';
} // 变量y这里被销毁

int main()
{
    std::string x { "Hello, world!" };

    printValue(x); // x 现在按引用传递给参数 y (代价小)

    return 0;
}
```

该程序与前一个程序相同，只是参数y的类型已从std::string更改为std::string&（左值引用）。现在，当调用printValue(x)时，左值引用参数y被绑定到x。绑定引用总是代价很小，不需要复制x。因为引用充当被引用对象的别名，所以当printValue()使用引用y时，它访问的是实际的x（而不是x的副本）。

{{< alert success >}}
**关键点**

通过引用，我们可以将原始对象的别名传递给函数，而无需在每次调用函数时复制它。

{{< /alert >}}

***
## 通过引用传递参数允许我们更改参数的值

通过值传递对象时，函数参数接收的是对象的副本。这意味着对参数值的任何更改都将对原始对象的副本而不是其本身进行:

```C++
#include <iostream>

void addOne(int y) // y 是 x 的拷贝
{
    ++y; // 修改的是 x 的拷贝, 而不是 x
}

int main()
{
    int x { 5 };

    std::cout << "value = " << x << '\n';

    addOne(x);

    std::cout << "value = " << x << '\n'; // x 未被修改

    return 0;
}
```

在上面的程序中，由于值参数y是x的副本，因此当我们增加y时，这仅影响y。该程序输出:

```C++
value = 5
value = 5
```


然而，由于引用的行为与被引用的对象相同，因此在使用按引用传递参数时，对引用参数所做的任何更改都将影响原始对象:

```C++
#include <iostream>

void addOne(int& y) // y 被绑定到原始的 x
{
    ++y; // 修改的实际是 x
}

int main()
{
    int x { 5 };

    std::cout << "value = " << x << '\n';

    addOne(x);

    std::cout << "value = " << x << '\n'; // x 被修改了

    return 0;
}
```

该程序输出:

```C++
value = 5
value = 6
```

在上面的示例中，x最初的值为5。当调用addOne(x)时，引用参数y绑定到x。当addOne()函数增加引用y时，它实际上是将x从5增加到6（不是x的副本）。即使在addOne()完成执行后，此更改的值仍然存在。

函数修改传入的参数值的功能可能很有用。假设您编写了一个函数来确定怪物是否成功攻击玩家。如果为true，怪物应该对玩家造成一定程度的伤害。如果通过引用传递玩家对象，则该函数可以直接修改传入的实际玩家对象的血量。如果通过值传递玩家对象，则只能修改玩家对象副本的血量，这没有那么有用。

{{< alert success >}}
**关键点**

通过传递非常量引用作为参数，允许我们在函数中修改原始对象的值。

{{< /alert >}}

***
## 按引用传递参数只能接受可修改的左值

由于对非常量值的引用只能绑定到可修改的左值（本质上是非常量变量）。在实践中，这大大限制了传递引用作为参数的实用性，因为这意味着我们不能传递常量或字面值。例如:

```C++
#include <iostream>

void printValue(int& y) // y 只能接受可修改的左值
{
    std::cout << y << '\n';
}

int main()
{
    int x { 5 };
    printValue(x); // ok: x 是可修改的左值

    const int z { 5 };
    printValue(z); // error: z 是不可修改的左值

    printValue(5); // error: 5 是右值

    return 0;
}
```

幸运的是，有一种简单的方法可以解决这个问题，我们将在下一课中讨论。同时还将研究何时按值传递与按引用传递。

***

{{< prevnext prev="/basic/chapter12/const-lvalue-ref/" next="/basic/chapter12/const-lvalue-ref-func-arg/" >}}
12.3 const的左值引用
<--->
12.5 通过常量左值引用传递函数参数
{{< /prevnext >}}
