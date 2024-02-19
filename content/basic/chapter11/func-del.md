---
title: "函数的delete说明符"
date: 2024-02-10T01:33:43+08:00
---

在某些情况下，编写的函数，不希望被某些类型的参数来调用。

考虑以下示例：

```C++
#include <iostream>

void printInt(int x)
{
    std::cout << x << '\n';
}

int main()
{
    printInt(5);    // okay: 打印 5
    printInt('a');  // 打印 97 -- 这样的输出是否有意义?
    printInt(true); // 打印 1 -- 这样的输出是否有意义?
    
    return 0;
}
```

此示例打印：

```C++
5
97
1
```


虽然printInt(5)显然没问题，但对printInt()的其他两个调用值得怀疑。使用printInt('a')，编译器将确定它可以将'a'提升为int值97，以便将函数调用与函数定义相匹配。同理将把true提升为int值1。

假设我们认为用char或bool类型的值调用printInt()没有意义。我们能做什么？

***
## 使用=delete说明符删除函数

在我们有一个显式不希望可调用的函数的情况下，可以使用=delete说明符将该函数定义为删除。如果编译器将函数调用与已删除函数相匹配，则将因编译错误而停止编译。

下面是使用此语法的上述更新版本：

```C++
#include <iostream>

void printInt(int x)
{
    std::cout << x << '\n';
}

void printInt(char) = delete; // 编译时匹配到这个函数将报错
void printInt(bool) = delete; // 编译时匹配到这个函数将报错

int main()
{
    printInt(97);   // okay

    printInt('a');  // 编译失败: 匹配到的函数被删除
    printInt(true); // 编译失败: 匹配到的函数被删除

    printInt(5.0);  // 编译失败: 有多个可匹配的函数
    
    return 0;
}
```

让我们快速看一下。首先，printInt('a')与printInt(char)精确匹配，该函数被删除。编译器因此产生编译错误。printInt(true)与printInt(bool)精确匹配，该函数被删除，因此也会产生编译错误。

printInt(5.0)是一个有趣的例子，可能会产生意想不到的结果。首先，编译器检查是否存在完全匹配的printInt(double)。没有找到。接下来，编译器尝试查找最佳匹配。尽管printInt(int)是唯一未删除的函数，但已删除的函数仍然被视为函数重载决议的候选函数。由于这些函数都不是明确的最佳匹配，编译器将发出不明确匹配的编译错误。

{{< alert success >}}
**关键点**

=delete表示“我禁止这样做”，而不是“这不存在”。

删除的函数参与函数重载决议的所有阶段（不仅仅是精确匹配阶段）。如果匹配到已删除的函数，则会导致编译错误。

{{< /alert >}}

***
## 删除所有不匹配的重载

删除一组单独的函数重载可以很好地工作，但可能会很冗长。有时，我们可能希望仅使用类型与函数参数完全匹配的值来调用某个函数。我们可以通过使用函数模板（在即将到来的函数模板中介绍）来实现这一点，如下所示：

```C++
#include <iostream>

// 这个函数优先使用int参数来匹配
void printInt(int x)
{
    std::cout << x << '\n';
}

// 这个函数模版将会匹配其它所有类型
// 因为这个函数模版被删除，因此匹配到它，将会导致编译失败
template <typename T>
void printInt(T x) = delete;

int main()
{
    printInt(97);   // okay
    printInt('a');  // 编译报错
    printInt(true); // 编译报错
    
    return 0;
}
```

***

{{< prevnext prev="/basic/chapter11/func-overload-resolution/" next="/basic/chapter11/default-param/" >}}
11.2 函数重载决议
<--->
11.4 默认参数
{{< /prevnext >}}
