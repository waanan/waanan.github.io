---
title: "指针与常量"
date: 2024-02-19T14:35:47+08:00
---

请考虑以下代码段：

```C++
int main()
{
    int x { 5 };
    int* ptr { &x }; // ptr 是一个普通（非常量）指针

    int y { 6 };
    ptr = &y; // 可以指向其它对象

    *ptr = 7; // 可以改变指向的对象的内容

    return 0;
}
```

对于普通（非常量）指针，可以更改指针所指向的对象（通过为指针赋值一个新地址），也可以更改所指向对象的值（通过解引用指针来访问指向的对象）。

然而，如果我们想要指向的值是常量，会发生什么？

```C++
int main()
{
    const int x { 5 }; // x 是 const
    int* ptr { &x };   // 编译失败: 无法从 const int* 转换到 int*

    return 0;
}
```

上面的代码段无法编译——不能将普通指针设置为指向const变量。这很有意义：const 变量其值不能更改。允许程序员将普通指针指向常量，将能通过该指针修改常量，这违反了常量的定义。

***
## 指向常量值的指针

常量指针是指向常量值的指针。

要声明指向常量值的指针，请在指针的数据类型之前使用const关键字：

```C++
int main()
{
    const int x{ 5 };
    const int* ptr { &x }; // okay: ptr 现在指向 "const int"

    *ptr = 6; // 不被允许: 不能修改常量

    return 0;
}
```

在上面的示例中，ptr指向常量int。由于所指向的数据类型是常量，因此无法更改所指向的值。

然而，由于指向常量的指针本身不是常量（它只是指向常量值），因此我们可以通过为指针分配新地址来更改指针所指向的内容：

```C++
int main()
{
    const int x{ 5 };
    const int* ptr { &x }; // ptr 指向 const int x

    const int y{ 6 };
    ptr = &y; // okay: ptr 现在指向 const int y

    return 0;
}
```

就像const引用一样，常量指针实际可以指向非const变量。常量指针将所指向的值视为常量，而不管该地址处的对象最初是否定义为常量：

```C++
int main()
{
    int x{ 5 }; // non-const
    const int* ptr { &x }; // ptr 指向 "const int"

    *ptr = 6;  // 不被允许: ptr 指向 "const int" ，所以不能通过ptr修改指向的对象
    x = 6; // ok: x是非const，所以仍然可以通过 x 这个标识符来修改实际的对象

    return 0;
}
```

***
## 指针常量（const 指针）

也可以使指针本身成为常量。指针常量是其指向地址在初始化后不能更改的指针。

要声明指针常量，请在指针声明中的星号后面使用const关键字：

```C++
int main()
{
    int x{ 5 };
    int* const ptr { &x }; // 星号后面的 const 代表这是一个 const pointer

    return 0;
}
```

在上述情况下，ptr是指向（非常量）int值的const指针。

就像普通常量一样，指针常量必须在定义时初始化，并且不能通过赋值更改该值：

```C++
int main()
{
    int x{ 5 };
    int y{ 6 };

    int* const ptr { &x }; // okay: const指针ptr被初始化为 x 的地址
    ptr = &y; // 错误: 初始化完成后，指针常量不能修改

    return 0;
}
```

然而，由于所指向的值是非常量的，因此可以通过解引用const指针来更改所指向的数值：

```C++
int main()
{
    int x{ 5 };
    int* const ptr { &x }; // ptr 永远指向 x

    *ptr = 6; // okay: 指向的x不是 常量

    return 0;
}
```

***
## 指向常量值的指针常量

最后，可以通过在类型之前和星号之后使用const关键字来声明指向常量值的指针常量：

```C++
int main()
{
    int value { 5 };
    const int* const ptr { &value }; // const指针，指向const对象

    return 0;
}
```

指向常量值的指针常量不能更改其地址，也不能通过指针更改它所指向的值。它只能解引用以获得它所指向的值。

***
## 指针和常量重述

总而言之，你只需要记住4条规则，它们非常符合逻辑：

1. 可以为非常量指针分配另一个地址，以更改它所指向的对象。
2. 指针常量始终指向相同的地址，并且不能更改该地址。
3. 指向非常量的指针可以更改它所指向的值。它不能指向常量。
4. 指向常量值的指针在通过指针访问时将该值视为常量，因此不能更改它所指向的值。指针常量可以指向非常量或常量左值（但不能指向右值，因为右值没有地址）。

记住以下的语法：

1. 星号之前的const与所指向的类型相关联。因此，这是一个指向常量值的指针，不能通过指针修改该值。
2. 星号后面的const与指针本身相关联。因此，不能为该指针分配新地址。


```C++
int main()
{
    int v{ 5 };

    int* ptr0 { &v };             // 指向 "int" 的普通指针
    const int* ptr1 { &v };       // 指向 "const int"，指针本身不是const
    int* const ptr2 { &v };       // 指向 "int"，指针本身是const
    const int* const ptr3 { &v }; // 指向 "const int"，指针本身是const

    // const 在 * 左边, const 属于指向的值
    // cont 在 * 右边, const 属于指针

    return 0;
}
```

***