---
title: "指针、引用和常量的类型自动推导"
date: 2024-02-19T14:35:47+08:00
---

在前面，我们讨论了可以使用auto关键字，让编译器从初始值设定项推断变量的类型：

```C++
int getVal(); // 返回int的一个函数

int main()
{
    auto val { getVal() }; // val 类型推导为 int

    return 0;
}
```

同时，默认情况下，类型推导将删除const（和constexpr）限定符：

```C++
const double foo()
{
    return 5.6;
}

int main()
{
    const double cd{ 7.8 };

    auto x{ cd };    // double (const 被丢弃)
    auto y{ foo() }; // double (const 被丢弃)

    return 0;
}
```

通过在定义中添加const（或constexpr）限定符，可以（重新）应用const（或contexpr）：

```C++
const double foo()
{
    return 5.6;
}

int main()
{
    constexpr double cd{ 7.8 };

    const auto x{ foo() };  // const double
    constexpr auto y{ cd }; // constexpr double
    const auto z { cd };    // const double

    return 0;
}
```

***
## 类型推导会删除引用属性

除了删除常量限定符外，类型演绎还将删除引用属性：

```C++
#include <string>

std::string& getRef(); // 返回引用

int main()
{
    auto ref { getRef() }; // 类型推导为 std::string (而不是 std::string&)

    return 0;
}
```

在上面的示例中，尽管函数getRef()返回std::string&，但引用限定符被删除，因此ref的类型被推导为std::string。

就像删除的常量限定符一样，如果希望推导出的类型是引用，可以在定义点重新应用引用：

```C++
#include <string>

std::string& getRef(); // 返回引用

int main()
{
    auto ref1 { getRef() };  // std::string (引用限定符被丢弃)
    auto& ref2 { getRef() }; // std::string& (重新加上引用限定符)

    return 0;
}
```

***
## 顶层const和底层const

顶层（top-level）const 是应用于对象本身的常量限定符。例如：

```C++
const int x;    // const 作用于 x, 所以是顶层const
int* const ptr; // const 作用于 ptr, 所以是顶层const
```

相反，底层（low-level）const 是应用于被引用或指向的对象的常量限定符：

```C++
const int& ref; // const 作用于被引用的对象, 所以是底层const
const int* ptr; // const 作用于被指向的对象, 所以是底层const
```

对常量值的引用始终是底层const。指针可以具有顶层、底层或两种const：

```C++
const int* const ptr; // 左边的 const 是底层, 右边的 const 是顶层
```

当我们说类型推导删除常量限定符时，它只删除顶层const。不会丢弃底层const。稍后将看到这方面的示例。

***
## 类型推导和常量引用

如果初始值设定项是对const（或constexpr）的引用，则首先删除引用（如果类型是auto&，则会重新加上引用），然后从结果中删除任何顶层const。

```C++
#include <string>

const std::string& getConstRef(); // 返回const 引用

int main()
{
    auto ref1{ getConstRef() }; // std::string (先丢弃引用, 然后丢弃顶层const)

    return 0;
}
```

在上面的示例中，由于getConstRef()返回一个const std::string&，因此首先删除引用，留下一个const std::string。现在是顶层const，因此它也被删除，推导出的类型为std::string。

{{< alert success >}}
**关键点**

删除引用可能会将底层const更改为顶层const： const std::string& 是底层const，但删除引用会产生const std::string，这是顶层const。

{{< /alert >}}

我们可以重新应用以下任一项或两项：

```C++
#include <string>

const std::string& getConstRef(); // 返回const 引用

int main()
{
    auto ref1{ getConstRef() };        // std::string (引用 和 顶层 const 丢弃)
    const auto ref2{ getConstRef() };  // const std::string (引用丢弃, const 重新设置)

    auto& ref3{ getConstRef() };       // const std::string& (引用重新设置, 底层const 保留)
    const auto& ref4{ getConstRef() }; // const std::string& (引用 和 const 重新设置)

    return 0;
}
```

在前面的示例中，我们讨论了ref1的情况。对于ref2，这类似于ref1的情况，只是重新应用了const限定符，因此导出的类型是const std::string。

ref3让事情变得更有趣。通常，引用将首先被删除，但由于重新应用了引用，因此它被保留。这意味着类型仍然是const std::string&。由于它是底层const，不会删除const。因此，推导出的类型是const std::string&。

ref4类似于ref3，只是也重新应用了const限定符。由于类型已经被推导为对const的引用，因此在这里重新应用const是多余的。也就是说，在这里使用const可以明确地表明，结果将是const（而在ref3的情况下，推导结果是const是隐式的，不那么明显）。

{{< alert success >}}
**最佳做法**

如果需要常量引用，请重新设置const限定符，即使这不是严格必要的。因为它使我们的意图清晰，并有助于防止错误。

{{< /alert >}}

***
## constexpr引用

它的工作方式与const引用相同：

```C++
#include <string_view>

constexpr std::string_view hello { "Hello" };

constexpr const std::string_view& getConstRef()
{
    return hello;
}

int main()
{
    auto ref1{ getConstRef() };            // std::string_view (引用 和 顶层 const 丢弃)
    constexpr auto ref2{ getConstRef() };  // constexpr std::string_view (引用丢弃, const 重新设置)

    auto& ref3{ getConstRef() };           // const std::string_view& (引用重新设置, 底层const 保留)
    constexpr auto& ref4{ getConstRef() }; // constexpr const std::string_view& (引用 和 const 重新设置)

    return 0;
}
```

***
## 类型推导和指针

与引用不同，类型推导不会丢弃指针类型：

```C++
#include <string>

std::string* getPtr(); // 返回指针

int main()
{
    auto ptr1{ getPtr() }; // std::string*

    return 0;
}
```

还可以将星号与指针类型推导结合使用：

```C++
#include <string>

std::string* getPtr(); // 返回指针

int main()
{
    auto ptr1{ getPtr() };  // std::string*
    auto* ptr2{ getPtr() }; // std::string*

    return 0;
}
```

***
## auto 与 auto* 的区别 （选读）

当我们将auto与指针类型初始值设定项一起使用时，为auto推导的类型包括指针。因此，对于上面的ptr1，auto的替代类型是std::string*。

当我们将auto*与指针类型初始值设定项一起使用时，为auto推导的类型不包括指针——在推导类型之后重新应用指针。因此，对于上面的ptr2，auto的替代类型是std::string，然后重新应用指针。

在大多数情况下，实际效果是相同的（在上例中，ptr1和ptr2都推导为std::string*）。

然而，在实践中，auto和auto\*之间存在一些差异。首先，auto\*必须解析为指针类型，否则将导致编译错误：

```C++
#include <string>

std::string* getPtr(); // 返回指针

int main()
{
    auto ptr3{ *getPtr() };      // std::string (解引用 getPtr())
    auto* ptr4{ *getPtr() };     // 编译失败 (初始值设定项不是指针)

    return 0;
}
```

这很有意义：在ptr4情况下，类型自动推导为std::string，然后重新应用指针。因此，ptr4具有类型std::string\*，并且不能使用不是指针的初始值设定项来初始化std::string\*。

第二，当考虑到const存在的情况下，auto和auto*的行为存在差异。下面介绍这一点。

***
## 类型演绎和const指针 (选读)

指针不会被丢弃，我们不必担心这一点。但对于指针，我们既有const指针，也有指向const的指针，也有auto和auto*。就像引用一样，在指针类型推导期间仅删除顶层常量。

让我们从一个简单的例子开始：

```C++
#include <string>

std::string* getPtr(); // 返回指针

int main()
{
    const auto ptr1{ getPtr() };  // std::string* const
    auto const ptr2 { getPtr() }; // std::string* const

    const auto* ptr3{ getPtr() }; // const std::string*
    auto* const ptr4{ getPtr() }; // std::string* const

    return 0;
}
```

当使用auto const或const auto时，我们是在说，“使导出的类型成为const”。因此，在ptr1和ptr2的情况下，导出的类型是std::string*，然后应用const，使最终的类型为std::string* const。这类似于const int和int const表示同一事物的方式。

然而，当使用auto*时，const限定符的顺序很重要。左侧的const意味着“使推导指针类型成为指向常量的指针”，而右侧的const则意味着“将推导指针类型变成指针常量”。因此，ptr3最终作为指向常量的指针，而ptr4最终作为指针常量。

现在让我们看一个例子，其中初始值设定项是指向常量的指针常量。

```C++
#include <string>

int main()
{
    std::string s{};
    const std::string* const ptr { &s };

    auto ptr1{ ptr };  // const std::string*
    auto* ptr2{ ptr }; // const std::string*

    auto const ptr3{ ptr };  // const std::string* const
    const auto ptr4{ ptr };  // const std::string* const

    auto* const ptr5{ ptr }; // const std::string* const
    const auto* ptr6{ ptr }; // const std::string*

    const auto const ptr7{ ptr };  // 错误: const 限定符不能使用两次
    const auto* const ptr8{ ptr }; // const std::string* const

    return 0;
}
```

ptr1和ptr2的情况很简单。顶层const（指针本身上的const）被删除。未删除所指向对象上的底层const。因此，在这两种情况下，最终的类型都是const std::string*。

ptr3和ptr4的情况也很简单。顶层const被删除，但我们重新设置了它。所指向对象上的底层常量不会被删除。因此，在这两种情况下，最终的类型都是const std::string* const。

ptr5和ptr6，在这两种情况下，顶层常量都会被删除。对于ptr5，auto\* const重新应用顶层const，因此最终类型为const std::string\* const。对于ptr6，const auto\*将const应用于所指向的类型（在本例中，该类型已经是const），因此最终的类型是const std::string\*。

在ptr7的情况下，将应用const限定符两次，这是不允许的，并将导致编译错误。

最后，在ptr8情况下，在指针的两侧应用const（这是允许的，因为auto\*必须是指针类型），因此结果类型是const std::string* const。

{{< alert success >}}
**最佳时间**

如果需要const指针，请重新设置常量限定符，即使它不是严格必要的。但这使您的意图清晰，并有助于防止错误。

{{< /alert >}}

***
