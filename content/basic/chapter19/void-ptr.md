---
title: "void指针"
date: 2024-08-19T20:25:40+08:00
---

void指针，也称为泛型指针，是一种特殊类型的指针，可以指向任何数据类型的对象！使用void关键字作为指针的类型，来声明void指针：

```C++
void* ptr {}; // ptr 是 void指针
```

void指针可以指向任何数据类型的对象：

```C++
int nValue {};
float fValue {};

struct Something
{
    int n;
    float f;
};

Something sValue {};

void* ptr {};
ptr = &nValue; // 有效
ptr = &fValue; // 有效
ptr = &sValue; // 有效
```

然而，由于void指针不知道它所指向的对象类型，因此解引用void指针是非法的。相反，在执行解引用之前，必须首先将void指针转换为其它指针类型。

```C++
int value{ 5 };
void* voidPtr{ &value };

// std::cout << *voidPtr << '\n'; // 非法: 解引用void指针是非法的

int* intPtr{ static_cast<int*>(voidPtr) }; // 然而, 可以将void指针转换为其它指针

std::cout << *intPtr << '\n'; // 然后进行解引用
```

这将打印：

```C++
5
```

下一个明显的问题是：如果void指针不知道它所指向的是什么，我们如何知道将其强制转换为什么？这取决于您的自定义代码逻辑，或可以为void指针附带一个标签。

下面是正在使用的void指针的示例：

```C++
#include <cassert>
#include <iostream>

enum class Type
{
    tInt, // 注: 不能直接写 "int" 因为它是关键字, 所以使用 "tInt"
    tFloat,
    tCString
};

void printValue(void* ptr, Type type)
{
    switch (type)
    {
    case Type::tInt:
        std::cout << *static_cast<int*>(ptr) << '\n'; // 转成int指针，然后解引用
        break;
    case Type::tFloat:
        std::cout << *static_cast<float*>(ptr) << '\n'; // 转成float指针，然后解引用
        break;
    case Type::tCString:
        std::cout << static_cast<char*>(ptr) << '\n'; // 转成char指针，然后打印对应的字符串
        // std::cout 会将 char* 当作C样式字符串
        // 因此这里打印的是对应的字符串
        break;
    default:
        std::cerr << "printValue(): invalid type provided\n"; 
        assert(false && "type not found");
        break;
    }
}

int main()
{
    int nValue{ 5 };
    float fValue{ 7.5f };
    char szValue[]{ "Mollie" };

    printValue(&nValue, Type::tInt);
    printValue(&fValue, Type::tFloat);
    printValue(szValue, Type::tCString);

    return 0;
}
```

该程序打印：

```C++
5
7.5
Mollie
```

***
## void指针杂项

void指针可以设置为空值：

```C++
void* ptr{ nullptr }; // ptr 是void指针，现在是nullptr
```

由于void指针不知道它所指向的对象类型，因此delete void指针将导致未定义的行为。如果需要删除void指针，请首先将其static_cast转换回适当的类型。

不能对空指针进行指针运算。这是因为指针算法要求指针知道它所指向的对象的大小，因此它可以适当地增加或减小指针。

请注意，没有所谓的void引用。这是因为void引用的类型为void&，完全不知道它引用的值的类型。

***
## 结论

通常，除非绝对必要，否则最好避免使用void指针，因为它允许您避免类型检查。这允许您无意中做一些没有意义的事情，编译器不会对此告警。例如，以下内容有效：

```C++
    int nValue{ 5 };
    printValue(&nValue, Type::tCString);
```

但谁知道结果会是什么呢！

尽管上述函数似乎是一种使单个函数处理多个数据类型的简洁方法，但C++实际上提供了一种更好的方法来执行相同的操作（通过函数重载）。函数重载保留类型检查以帮助防止误用。许多其它地方曾经使用空指针来处理多个数据类型，现在最好使用模板来完成，模板还提供强类型检查。

然而，偶尔您可能仍然会发现void指针的合理用法。但需确保没有更好（更安全）的方法来使用其它语言机制做相同的事情！

***
