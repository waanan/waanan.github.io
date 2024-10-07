---
title: "重载运算符和函数模板"
date: 2024-08-20T12:01:51+08:00
---

在函数模板实例化中，我们讨论了编译器如何使用函数模板来实例化函数，然后对这些函数进行编译。还注意到，如果函数模板中的代码试图执行实际类型不支持的某些操作（例如将整数值1添加到std::string），则这些函数可能无法编译。

在本课中，我们将看几个示例，其中实例化的函数将无法编译，因为我们的实际类类型不支持这些运算符，并展示如何定义这些运算符，以便实例化函数可以进行编译。

***
## 运算符、函数调用和函数模板

首先，让我们创建一个简单的类：

```C++
class Cents
{
private:
    int m_cents{};
public:
    Cents(int cents)
        : m_cents { cents }
    {
    }

    friend std::ostream& operator<< (std::ostream& ostr, const Cents& c)
    {
        ostr << c.m_cents;
        return ostr;
    }
};
```

并定义max函数模板：

```C++
template <typename T>
const T& max(const T& x, const T& y)
{
    return (x < y) ? y : x;
}
```

现在，让我们看看当我们试图用Cents类型的对象调用max()时会发生什么：

```C++
#include <iostream>

class Cents
{
private:
    int m_cents{};
public:
    Cents(int cents)
        : m_cents { cents }
    {
    }

    friend std::ostream& operator<< (std::ostream& ostr, const Cents& c)
    {
        ostr << c.m_cents;
        return ostr;
    }
};

template <typename T>
const T& max(const T& x, const T& y)
{
    return (x < y) ? y : x;
}

int main()
{
    Cents nickel{ 5 };
    Cents dime{ 10 };

    Cents bigger { max(nickel, dime) };
    std::cout << bigger << " is bigger\n";

    return 0;
}
```

C++将为max()创建一个模板实例，如下所示：

```C++
template <>
const Cents& max(const Cents& x, const Cents& y)
{
    return (x < y) ? y : x;
}
```

然后它将尝试编译这个函数。看到这里的问题了吗？当x和y是Cents类型时，C++不知道如何计算"x \< y" ！因此，这将产生编译错误。

要解决此问题，只需重载 运算符<，对于我们希望与max一起使用的任何类：

```C++
#include <iostream>

class Cents
{
private:
    int m_cents {};
public:
    Cents(int cents)
        : m_cents { cents }
    {
    }
    
    friend bool operator< (const Cents& c1, const Cents& c2)
    {
        return (c1.m_cents < c2.m_cents);
    }

    friend std::ostream& operator<< (std::ostream& ostr, const Cents& c)
    {
        ostr << c.m_cents;
        return ostr;
    }
};

template <typename T>
const T& max(const T& x, const T& y)
{
    return (x < y) ? y : x;
}

int main()
{
    Cents nickel{ 5 };
    Cents dime { 10 };

    Cents bigger { max(nickel, dime) };
    std::cout << bigger << " is bigger\n";

    return 0;
}
```

这按预期工作，并打印：

```C++
10 is bigger
```

***
## 另一个例子

让我们再举一个由于缺少重载操作符而无法工作的函数模板的例子。

以下函数模板将计算数组中多个对象的平均值：

```C++
#include <iostream>

template <typename T>
T average(const T* myArray, int numValues)
{
    T sum { 0 };
    for (int count { 0 }; count < numValues; ++count)
        sum += myArray[count];

    sum /= numValues;
    return sum;
}

int main()
{
    int intArray[] { 5, 3, 2, 1, 4 };
    std::cout << average(intArray, 5) << '\n';

    double doubleArray[] { 3.12, 3.45, 9.23, 6.34 };
    std::cout << average(doubleArray, 4) << '\n';

    return 0;
}
```

这将产生以下值：

```C++
3
5.535
```

正如您所看到的，它非常适合内置类型！

现在，让我们看看在Cents类上调用此函数时会发生什么：

```C++
#include <iostream>

template <typename T>
T average(const T* myArray, int numValues)
{
    T sum { 0 };
    for (int count { 0 }; count < numValues; ++count)
        sum += myArray[count];

    sum /= numValues;
    return sum;
}

class Cents
{
private:
    int m_cents {};
public:
    Cents(int cents)
        : m_cents { cents }
    {
    }
};

int main()
{
    Cents centsArray[] { Cents { 5 }, Cents { 10 }, Cents { 15 }, Cents { 14 } };
    std::cout << average(centsArray, 4) << '\n';

    return 0;
}
```

编译器变得疯狂，并产生了大量的错误消息！第一条错误消息如下所示：

```C++
error C2679: binary << : no operator found which takes a right-hand operand of type Cents (or there is no acceptable conversion)
```

请记住，average()返回一个Cents对象，我们试图使用 操作符<< 将该对象流式传输到std::cout。然而，我们还没有为Cents类定义 运算符<<。让我们这样做：

```C++
#include <iostream>

template <typename T>
T average(const T* myArray, int numValues)
{
    T sum { 0 };
    for (int count { 0 }; count < numValues; ++count)
        sum += myArray[count];

    sum /= numValues;
    return sum;
}

class Cents
{
private:
    int m_cents {};
public:
    Cents(int cents)
        : m_cents { cents }
    {
    }

    friend std::ostream& operator<< (std::ostream& out, const Cents& cents)
    {
        out << cents.m_cents << " cents ";
        return out;
    }
};

int main()
{
    Cents centsArray[] { Cents { 5 }, Cents { 10 }, Cents { 15 }, Cents { 14 } };
    std::cout << average(centsArray, 4) << '\n';

    return 0;
}
```

如果我们再次编译，我们将得到另一个错误：

```C++
error C2676: binary += : Cents does not define this operator or a conversion to a type acceptable to the predefined operator
```

此错误实际上是由调用average（const Cents*，int）时创建的函数模板实例引起的。请记住，当我们调用模板化函数时，编译器“模板化”出函数的副本，其中模板类型参数（占位符类型）已被函数调用中的实际类型替换。下面是T是Cents对象时average（）的函数模板实例：

```C++
template <>
Cents average(const Cents* myArray, int numValues)
{
    Cents sum { 0 };
    for (int count { 0 }; count < numValues; ++count)
        sum += myArray[count];

    sum /= numValues;
    return sum;
}
```

收到错误消息的原因是由于以下行：

```C++
        sum += myArray[count];
```

在这种情况下，sum是一个Cents对象，但我们没有为Cents对象定义 运算符+= ！我们需要定义此函数，以便average（）能够使用Cents。可以看到average（）也使用运算符/=，因此也定义它：

```C++
#include <iostream>

template <typename T>
T average(const T* myArray, int numValues)
{
    T sum { 0 };
    for (int count { 0 }; count < numValues; ++count)
        sum += myArray[count];

    sum /= numValues;
    return sum;
}

class Cents
{
private:
    int m_cents {};
public:
    Cents(int cents)
        : m_cents { cents }
    {
    }

    friend std::ostream& operator<< (std::ostream& out, const Cents& cents)
    {
        out << cents.m_cents << " cents ";
        return out;
    }

    Cents& operator+= (const Cents &cents)
    {
        m_cents += cents.m_cents;
        return *this;
    }

    Cents& operator/= (int x)
    {
        m_cents /= x;
        return *this;
    }
};

int main()
{
    Cents centsArray[] { Cents { 5 }, Cents { 10 }, Cents { 15 }, Cents { 14 } };
    std::cout << average(centsArray, 4) << '\n';

    return 0;
}
```

最后，我们的代码将编译并运行！结果如下：

```C++
11 cents
```

请注意，我们根本不需要修改average（）来使其与Cents类型的对象一起工作。我们只需定义用于实现Cents类的average（）的需要的操作符，其余的由编译器处理！

***

{{< prevnext prev="/basic/chapter21/shadow-deep-copy/" next="/basic/chapter21/summary/" >}}
21.12 浅拷贝与深拷贝
<--->
21.14 第21章总结
{{< /prevnext >}}
