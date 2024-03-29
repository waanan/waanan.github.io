---
title: "Void"
date: 2023-10-09T20:06:10+08:00
---

Void是最容易解释的数据类型。基本上，void意味着“没有类型”！

Void是不完整类型的第一个例子。不完整类型是已声明但尚未定义的类型。编译器知道这种类型的存在，但没有足够的信息来确定为该类型的对象分配多少内存。void是故意不完整的，因为它表示缺少类型，因此无法定义。

无法实例化不完整的类型：

```C++
void value; // 无法编译，变量无法被定义为不完整的类型
```

Void通常用于几种不同的上下文。

***
## 不返回值的函数

最常见的是，void用于指示函数不返回值：

```C++
void writeValue(int x) // void 这里代表不返回值
{
    std::cout << "The value of x is: " << x << '\n';
    // 无return语句
}
```

如果使用return语句尝试在这样的函数中返回值，则将导致编译错误：

```C++
void noReturn(int x) // void 这里代表不返回值
{
    std::cout << "The value of x is: " << x << '\n';

    return 5; // 会导致编译失败
}
```

***
## 不推荐：不带参数的函数

在C中，void用作指示函数不带任何参数：

```C++
int getValue(void) // void 这里代表没有参数
{
    int x{};
    std::cin >> x;

    return x;
}
```

尽管这将在C++中可以通过编译（出于向后兼容性的原因），但在C++中，这种使用关键字void的做法被认为是不推荐的。下面的代码是等效的，并且在C++中是首选的：

```C++
int getValue() // 无参数函数
{
    int x{};
    std::cin >> x;

    return x;
}
```

{{< alert success >}}
**最佳实践**

使用空参数列表而不是void来指示函数没有参数。

{{< /alert >}}

***
## void的其他用途

void关键字在C++中有第三种（更高级）用法，我们在介绍指针时介绍了这一用法——void指针。因为我们还没有讨论指针是什么，所以您现在不需要担心这种情况。

***

{{< prevnext prev="/basic/chapter4/intro/" next="/basic/chapter4/size-of/" >}}
4.0 基本数据类型简介
<--->
4.2 对象大小和sizeof运算符
{{< /prevnext >}}
