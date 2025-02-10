---
title: "指针的部分模板特化"
date: 2025-01-22T20:47:14+08:00
---

在上一课中，我们看了一个简单的模板类，以及类型double的特化：

```C++
#include <iostream>

template <typename T>
class Storage
{
private:
    T m_value {};
public:
    Storage(T value)
      : m_value { value }
    {
    }

    void print()
    {
        std::cout << m_value << '\n';
    }
};

template<>
void Storage<double>::print() // 针对double的完全特化
{
    std::cout << std::scientific << m_value << '\n';
}

int main()
{
    // 定义一些 Storage
    Storage i { 5 };
    Storage d { 6.7 }; // 会导致 Storage<double> 被隐式实例化

    // 进行打印
    i.print(); // 调用 Storage<int>::print (从 Storage<T> 实例化)
    d.print(); // 调用 Storage<double>::print (从特化的 Storage<double>::print() 实例化)
}
```

然而，尽管这个类很简单，但它有一个隐藏的缺陷：但当T是指针类型时，可以编译，但打印结果比较奇怪。例如：

```C++
int main()
{
    double d { 1.2 };
    double *ptr { &d };

    Storage s { ptr };
    s.print();
    
    return 0;
}
```

在作者的机器上，这产生了结果：

```C++
0x7ffe164e0f50
```

发生了什么事？由于ptr是double\*，因此s的类型为Storage\<double\*\>，这意味着m_value的类型为double\*。当调用构造函数时，m_value接收ptr持有的地址的副本，并且在调用print()成员函数时打印该地址。

那么我们如何解决这个问题呢？

一种选择是为类型double\*添加完全特化：

```C++
#include <iostream>

template <typename T>
class Storage
{
private:
    T m_value {};
public:
    Storage(T value)
      : m_value { value }
    {
    }

    void print()
    {
        std::cout << m_value << '\n';
    }
};

template<>
void Storage<double*>::print() // 针对 double* 的完全特化
{
    if (m_value)
        std::cout << std::scientific << *m_value << '\n';
}

template<>
void Storage<double>::print() // 针对 double 的完全特化
{
    std::cout << std::scientific << m_value << '\n';
}

int main()
{
    double d { 1.2 };
    double *ptr { &d };

    Storage s { ptr };
    s.print(); // 调用 Storage<double*>::print()
    
    return 0;
}
```

现在打印正确的结果：

```C++
1.200000e+00
```

但这仅解决了T为double\*类型时的问题。当T是int\*、char\*或其他指针类型时呢？

我们确实不想为每个指针类型创建完全特化。事实上，这甚至是不可能的，因为用户总是可以传入指向自定义类型的指针。

***
## 指针的部分模板特化

您可能会考虑尝试创建在类型T*上重载的模板函数：

```C++
// 无法按预期执行
template<typename T>
void Storage<T*>::print()
{
    if (m_value)
        std::cout << std::scientific << *m_value << '\n';
}
```

这样的函数是部分特化的模板函数，因为它将T的类型限制为（指针类型），但T仍然是类型模板参数。

不幸的是，这不起作用，原因很简单：函数不能部分特化。正如我们之前提到的，只有类可以部分特化。

因此，让我们部分特化Storage类：

```C++
#include <iostream>

template <typename T>
class Storage // 这是基础的模版类
{
private:
    T m_value {};
public:
    Storage(T value)
      : m_value { value }
    {
    }

    void print()
    {
        std::cout << m_value << '\n';
    }
};

template <typename T> // 仍然有一个类型模版参数
class Storage<T*> // 部分特化为 T*
{
private:
    T* m_value {};
public:
    Storage(T* value)
      : m_value { value }
    {
    }

    void print();
};

template <typename T>
void Storage<T*>::print() // Storage<T*> 的成员函数
{
    if (m_value)
        std::cout << std::scientific << *m_value << '\n';
}

int main()
{
    double d { 1.2 };
    double *ptr { &d };

    Storage s { ptr }; // 从部分特化的 Storage<double*> 进行实例化
    s.print(); // 调用 Storage<double*>::print()
    
    return 0;
}
```

我们在类之外定义了Storage\<T\*\>::print()，只是为了说明它是如何完成的，并表明该定义与上面无法工作的部分特化函数Storage\<T\*\>::print）相同。然而，既然Storage\<T\*\>是一个部分特化的类，Storage\<T\*\>::print()就不再是部分特化的——它是一个非特化函数，这就是为什么它被允许定义。

值得注意的是，我们的类型模板参数被定义为T，而不是T\*。这意味着T将被推导为非指针类型，因此我们必须在希望指针指向T的任何地方使用T*。还值得提醒的是，部分特化Storage\<T\*\>需要在基础模板类Storage\<T\>之后定义。

***
## 所有权和生命周期问题

上述部分特化类Storage\<T*\>还有另一个潜在问题。因为m_value是T\*，所以它是一个指向传入对象的指针。如果该对象随后被销毁，则Storage\<T*\>将悬空。

核心问题是，我们的Storage\<T\>实现具有复制语义（这意味着它制作其初始值设定项的副本），但Storage\<T\*\>具有引用语义（这表示它是对其初始值设置项的引用）。这种不一致性会导致错误。

我们可以通过几种不同的方法来处理这些问题（按照复杂性的增加顺序）：

首先，可以让Storage\<T*\>成为查看器（引用语义），调用方来确保在Storage\<T*\>存在时，实际的对象保持有效。不幸的是，因为部分特化的类，其名称必须和基础类的名称一致，所以我们不能将其命名为StorageView。所以只能添加一些非强制性的注释，来提醒使用者。

或者，避免使用Storage\<T*\>。调用方永远可以解引用指针，传递对象的一份拷贝数据（对于storage类来讲语义更合适）。然而，虽然可以删除重载函数，但C++不允许删除类。显而易见的解决方案是部分特化Storage\<T*\>，然后在模板被实例化时做一些事情使其不能编译（例如，static_assert），这种方法有一个主要缺点：std::nullptr_t不是指针类型，因此Storage\<std::nullptr_t\>将与Storage\<T\*\>不匹配！

更好的解决方案是完全避免部分特化，并在基础模板上使用static_assert来确保T是我们可以接受的类型。下面是该方法的一个示例：

```C++
#include <iostream>
#include <type_traits> // 引入 std::is_pointer_v 和 std::is_null_pointer_v

template <typename T>
class Storage
{
    // 确保 T 不是指针，也不是 std::nullptr_t
    static_assert(!std::is_pointer_v<T> && !std::is_null_pointer_v<T>, "Storage<T*> and Storage<nullptr> disallowed");

private:
    T m_value {};

public:
    Storage(T value)
      : m_value { value }
    {
    }

    void print()
    {
        std::cout << m_value << '\n';
    }
};

int main()
{
    double d { 1.2 };

    Storage s1 { d }; // ok
    s1.print();

    Storage s2 { &d }; // static_assert 触发，因为 T 是指针
    s2.print();

    Storage s3 { nullptr }; // static_assert 触发，因为 T 是 nullptr
    s3.print();
    
    return 0;
}
```

又或者，让Storage\<T*\>在堆空间制作原始对象的一份拷贝。 比较简单的方式是使用std::unique_ptr来自动管理生命周期:

```C++
#include <iostream>
#include <type_traits> // 引入 std::is_pointer_v 和 std::is_null_pointer_v
#include <memory>

template <typename T>
class Storage
{
    // 确保 T 不是指针，也不是 std::nullptr_t
    static_assert(!std::is_pointer_v<T> && !std::is_null_pointer_v<T>, "Storage<T*> and Storage<nullptr> disallowed");

private:
    T m_value {};

public:
    Storage(T value)
      : m_value { value }
    {
    }

    void print()
    {
        std::cout << m_value << '\n';
    }
};

template <typename T>
class Storage<T*>
{
private:
    std::unique_ptr<T> m_value {}; // 使用 std::unique_ptr 自动管理存储对象的生命周期

public:
    Storage(T* value)
      : m_value { std::make_unique<T>(value ? *value : 0) }
    {
    }

    void print()
    {
        if (m_value)
            std::cout << *m_value << '\n';
    }
};

int main()
{
    double d { 1.2 };

    Storage s1 { d }; // ok
    s1.print();

    Storage s2 { &d }; // ok, 制作拷贝
    s2.print();

    return 0;
}
```

***
## 总结

当您希望模版类以不同的方式处理指针和非指针实现时，使用模板类部分特化是非常有用的，但这种方式需要对最终用户是完全透明的。

***