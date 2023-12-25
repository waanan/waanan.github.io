---
title: "变量名称遮挡（Variable shadowing）"
date: 2023-12-18T16:52:52+08:00
---

每个代码块有自己的变量命名的空间。那么，当我们在嵌套的内部块中有一个变量，该变量与外部块中的变量同名时，会发生什么呢？当这种情况发生时，嵌套块内的变量会“遮挡”外部变量。

***
## 局部变量名称遮挡

```C++
#include <iostream>

int main()
{ // 外围代码块
    int apples { 5 }; // 外围代码块中的 apples 变量

    { // 内层代码块
        // 这里的 apples 是外围的
        std::cout << apples << '\n'; // 打印外围的 apples 的值

        int apples{ 0 }; // 嵌套的代码块中的 apples 变量

        // apples 现在指代的是内层代码块里的变量
        // 外围的被遮挡住了

        apples = 10; // 内层的 apples 被赋值

        std::cout << apples << '\n'; // 打印内层的 apples的值
    } // 内层代码块中的apples被销毁


    std::cout << apples << '\n'; // 打印外围代码块中的 apples 变量

    return 0;
} // 外围代码块中的apples被销毁
```

如果运行此程序，它将打印：

```C++
5
10
5
```

在上面的程序中，我们首先在外部块中声明一个名为apples的变量。该变量在内部块中可见，我们可以通过打印其值（5）来查看。然后，我们在嵌套块中声明一个不同的变量（也称为apples）。从这一位置到块的末尾，名称apples是指嵌套块内的变量，而不是外部块。

因此，当我们将值10分配给apples时，我们将其分配给嵌套块内的apples。打印该值（10）后，嵌套块结束，嵌套块apples被销毁。外围块apples的存在和值不受影响，我们通过打印apples（5）的值来证明这一点。

请注意，如果未在嵌套块内新定义apples，则嵌套块中的apples仍然指外部块apples，因此将值10分配给apples将应用于外部块apples：

```C++
#include <iostream>

int main()
{ // 外围代码块
    int apples{5}; // 外围代码块中的 apples 变量

    { // 内层代码块
        // apples refers to outer block apples here
        std::cout << apples << '\n'; // 打印外围的 apples 的值

        // 这个例子不定义内层的apples变量

        apples = 10; // 赋值给外部块的apples

        std::cout << apples << '\n'; // 打印外围的 apples 的值
    } // 外围代码块中的 apples在内层代码块结束时仍然存在

    std::cout << apples << '\n'; // 打印外围代码块中的 apples 变量

    return 0;
} // 外围代码块中的apples被销毁
```

上述程序打印：

```C++
5
10
10
```

***
## 遮挡全局变量

类似于嵌套块中的变量会隐藏外部块中的同名变量，与全局变量同名的局部变量将遮挡全局变量，无论局部变量在作用域中的何处：

```C++
#include <iostream>
int value { 5 }; // 全局变量

void foo()
{
    std::cout << "global variable value: " << value << '\n'; // 这里使用的是全局变量
}

int main()
{
    int value { 7 }; // 会遮挡全局变量 value，直到本代码块结束

    ++value; // 局部变量value加一

    std::cout << "local variable value: " << value << '\n';

    foo();

    return 0;
} // 局部变量 value 销毁
```

此代码打印：

```C++
local variable value: 8
global variable value: 5
```

然而，由于全局变量是全局命名空间的一部分，我们可以使用没有前缀的域操作符（ :: ）来告诉编译器我们是指全局变量，而不是局部变量。

```C++
#include <iostream>
int value { 5 }; // 全局变量

int main()
{
    int value { 7 }; // 会遮挡全局变量 value，直到本代码块结束
    ++value; // 局部变量value加一

    --(::value); // 全局变量 value 减一， 这里的括号是为了可读性

    std::cout << "local variable value: " << value << '\n';
    std::cout << "global variable value: " << ::value << '\n';

    return 0;
} // 局部变量 value 销毁
```

此代码打印：

```C++
local variable value: 8
global variable value: 4
```

***
## 避免变量遮挡

通常应避免局部变量的命名遮挡，因为在使用或修改错误的变量时，会导致意外错误。当变量被遮挡时，某些编译器将发出警告。

出于相同原因，我们建议也避免遮挡全局变量。如果所有全局变量名称都使用“g_”前缀，则这可以方便的避免。

{{< alert success >}}
**最佳实践**

避免变量遮挡。

{{< /alert >}}

{{< alert success >}}
**对于GCC/G++用户**

GCC和Clang支持标记 -Wshadow，如果变量被遮挡，则会生成警告。该标志有几个子变量（-Wshadow=global、-Wshahow=local和-Wshadow=compatible-local）。有关差异的解释，请参阅GCC文档。

默认情况下，Visual Studio已启用此类警告。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter7/global-var/" next="/basic/chapter7/internal-link/" >}}
7.3 全局变量
<--->
7.5 内部链接
{{< /prevnext >}}
