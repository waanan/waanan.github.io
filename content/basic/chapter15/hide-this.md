---
title: "隐藏的“this”指针和成员函数调用"
date: 2024-06-24T18:56:16+08:00
---

新程序员经常问的关于类的问题之一是，“当调用成员函数时，C++如何知道被调用的对象？”。

首先，定义一个要使用的简单类。此类封装整数值，并提供一些访问函数来获取和设置该值：

```C++
#include <iostream>

class Simple
{
private:
    int m_id{};
 
public:
    Simple(int id)
        : m_id{ id }
    {
    }

    int getID() const { return m_id; }
    void setID(int id) { m_id = id; }

    void print() const { std::cout << m_id; }
};

int main()
{
    Simple simple{1};
    simple.setID(2);

    simple.print();

    return 0;
}
```

如您所料，该程序会产生以下结果：

```C++
2
```

当调用 simple.setID(2); 时，C++知道函数 setID() 应该在对象simple上操作，并且m_id实际上是指simple.m_id。

C++使用了一个名为this的隐藏指针！在本课中，将更详细地了解这一点。

***
## 隐藏的this指针

在每个成员函数内部，关键字this是保存当前隐式对象地址的const指针。

大多数时候，没有明确提到这一点，下面是一个说明示例：

```C++
#include <iostream>

class Simple
{
private:
    int m_id{};

public:
    Simple(int id)
        : m_id{ id }
    {
    }

    int getID() const { return m_id; }
    void setID(int id) { m_id = id; }

    void print() const { std::cout << this->m_id; } // 使用 `this` 访问隐式对象 使用 操作符-> 访问成员 m_id
};

int main()
{
    Simple simple{ 1 };
    simple.setID(2);
    
    simple.print();

    return 0;
}
```

这与前面的示例相同，并打印：

```C++
2
```

请注意上述两个示例中的print()成员函数执行的操作完全相同：

```C++
    void print() const { std::cout << m_id; }       // 隐式使用 this
    void print() const { std::cout << this->m_id; } // 显示使用 this
```

原来，前者是后者的简写。当编译程序时，编译器将使用this->隐式地为引用隐式对象的任何成员添加前缀。前一种写法有助于保持代码更简洁，并防止冗余的必须反复显式地编写此->。

{{< alert success >}}
**提醒**

使用->从指向对象的指针中选择成员。this->mid 相当于 (*this).mid。

在前面介绍指针和引用选择成员中介绍了 操作符->。

{{< /alert >}}

***
## this 如何生效？

让我们仔细看看这个函数调用：

```C++
    simple.setID(2);
```

尽管对函数 setID(2) 的调用看起来只有一个参数，但实际上有两个！编译时，编译器重写表达式 simple.setID(2); 如下所示：

```C++
    Simple::setID(&simple, 2); // simple由前缀变换为函数参数！
```

注意，这现在只是一个标准函数调用，对象simple（以前是对象前缀）现在的地址作为函数的参数传递。

但这只是答案的一半。由于函数调用现在有一个添加的参数，因此还需要修改成员函数定义，以接受（并使用）该参数。下面是setID()的原始成员函数定义：

```C++
    void setID(int id) { m_id = id; }
```

编译器如何重写函数是特定于实现的细节，但最终结果如下：

```C++
    static void setID(Simple* const this, int id) { this->m_id = id; }
```

注意，setID函数有一个新的最左边的参数this，它是一个const指针（这意味着它不能被重新指向，但指向的内容可以修改）。m_id成员也被重写为this->m_id，使用this指针。

组合在一起：

1. 当调用 simple.setID(2) ，编译器实际会调用 Simple::setID(&simple, 2)，simple 的地址会传递给函数。
2. 函数有一个隐藏的 this 参数来接收 simple。
3. setID() 函数中的成员变量，被改写为带 this-> 前缀的形式，这指向传入的 simple。所以当执行到 this->m_id 时，实际计算的是 simple.m_id。


好消息是，所有这些都是自动发生的，是否记得它是如何工作的并不重要。需要记住的是，所有非静态成员函数都有一个this指针，该指针指向调用该函数的对象。

{{< alert success >}}
**对于高级读者**

在这个上下文中，static关键字意味着函数不与类的对象相关联，被视为类的作用域内的普通函数。将在学习静态成员函数时进行讲解。

{{< /alert >}}

{{< alert success >}}
**关键点**

所有非静态成员函数都有一个this const指针，该指针保存隐式对象的地址。

{{< /alert >}}

***
## this总是指向正在操作的对象

新程序员有时会对存在多少个指针感到困惑。每个成员函数都有一个指向隐式对象的this指针参数。考虑：

```C++
int main()
{
    Simple a{1}; // this = &a 在 Simple 的构造函数里
    Simple b{2}; // this = &b 在 Simple 的构造函数里
    a.setID(3); // this = &a 在成员函数 setID() 里
    b.setID(4); // this = &b 在成员函数 setID() 里

    return 0;
}
```

注意，this指针交替保存对象a或b的地址，这取决于调用的是对象a还是b的成员函数。

因为this是一个函数参数（而不是成员），所以它不会使类的实例在内存占用更大。

***
## 明确使用this

大多数情况下，不需要显式引用this指针。然而，在一些情况下，这样做是有用的：

首先，如果成员函数中具有与数据成员同名的参数，则可以通过使用以下命令来消除它们的歧义：

```C++
struct Something
{
    int data{}; // 这个结构体里没有使用 m_ 前缀

    void setData(int data)
    {
        this->data = data; // this->data 是成员变量, data 是参数
    }
};
```

这个Something类有一个名为data的成员。setData() 的函数参数也被命名为data。在 setData() 函数中，data是函数参数（因为函数参数遮挡了成员变量data），因此如果想要使用data成员，采用 this->data 的形式。

一些开发人员喜欢显式地将 this-> 添加到所有类成员中，以明确他们正在引用成员变量。建议您避免这样做，因为这样做往往会降低代码的可读性，而不会带来什么好处。使用“m_”前缀是区分私有成员变量和非成员（局部）变量的更简洁的方法。

***
## 返回 *this

其次，有时让成员函数将隐式对象作为返回值是有用的。这样做的主要原因是允许成员函数“链接”在一起，因此可以在单个表达式中对同一对象调用多个成员函数！这称为函数链接（或方法链接）。

考虑这个常见的示例，其中您使用std::cout 输出几次文本

```C++
std::cout << "Hello, " << userName;
```

编译器对上述代码段的求值如下：

```C++
(std::cout << "Hello, ") << userName;
```

首先，操作符<<使用std::cout和字符串文字“Hello”，将“Hello“打印到控制台。然而，由于这是表达式的一部分，运算符<<还需要返回值（或void）。如果运算符<<返回void，则最终将此作为部分求值的表达式：

```C++
void{} << userName;
```

这显然没有任何意义（编译器会抛出错误）。相反，操作符<<返回传入的流对象，在本例中为std::cout。这样，在计算完第一个运算符<<后，我们得到：

```C++
(std::cout) << userName;
```

然后打印用户名。

这样，只需要指定一次std::cout，然后可以使用操作符<<将任意多段文本链接在一起。每次调用operator<<都返回std::cout，因此下一次调用operator<<时使用std::cout作为左操作数。

也可以在成员函数中实现这种行为。考虑以下类：

```C++
class Calc
{
private:
    int m_value{};

public:

    void add(int value) { m_value += value; }
    void sub(int value) { m_value -= value; }
    void mult(int value) { m_value *= value; }

    int getValue() const { return m_value; }
};
```

如果你想加5，减3，再乘以4，你必须这样做：

```C++
#include <iostream>

int main()
{
    Calc calc{};
    calc.add(5); // 返回 void
    calc.sub(3); // 返回 void
    calc.mult(4); // 返回 void

    std::cout << calc.getValue() << '\n';

    return 0;
}
```

然而，如果通过引用使每个函数返回*this，可以将调用链接在一起。下面是具有“可链接”函数的Calc的新版本：

```C++
class Calc
{
private:
    int m_value{};

public:
    Calc& add(int value) { m_value += value; return *this; }
    Calc& sub(int value) { m_value -= value; return *this; }
    Calc& mult(int value) { m_value *= value; return *this; }

    int getValue() const { return m_value; }
};
```

注意，add()、sub() 和mult() 现在通过引用返回*this。因此，这允许我们执行以下操作：

```C++
#include <iostream>

int main()
{
    Calc calc{};
    calc.add(5).sub(3).mult(4); // 函数链接

    std::cout << calc.getValue() << '\n';

    return 0;
}
```

有效地将三行压缩为一个表达式！让我们仔细看看这是如何工作的。

首先，调用calc.add(5)，将5与m_value相加。然后，add() 返回对*this的引用，这是对隐式对象calc的引用，因此calc将是后续求值中使用的对象。接下来，calc.sub(3) 求值，它从m_value中减去3，然后再次返回calc。最后，calc.mult(4) 将m_value乘以4，并返回calc，它不再使用，因此被忽略。

由于每个函数在执行时都修改了calc，因此calc的m_value现在包含值（（（0+5）-3）*4），即8。

这可能是this最常见的显式用法，并且无论何时，具有可链接的成员函数都应该考虑使用 *this。

因为this总是指向隐式对象，所以在解引用它时，不需要检查它是否为空指针。

***
## 将类重置回默认状态

如果您的类具有默认构造函数，您可能会对提供一种将现有对象重置到其默认状态的方法感兴趣。

在前面讲解委托构造函数时，可以知道构造函数仅用于初始化新对象，不应直接调用。这样做将导致意外的行为。

将类重置回默认状态的最佳方法是创建 reset() 成员函数，让该函数创建新对象（使用默认构造函数），然后将该新对象分配给当前隐式对象，如下所示：

```C++
    void reset()
    {
        *this = {}; // 值初始化一个新对象，并赋值给当前的隐式对象
    }
```

下面是一个完整的程序，演示了此reset() 函数的实际使用：

```C++
#include <iostream>

class Calc
{
private:
    int m_value{};

public:
    Calc& add(int value) { m_value += value; return *this; }
    Calc& sub(int value) { m_value -= value; return *this; }
    Calc& mult(int value) { m_value *= value; return *this; }

    int getValue() const { return m_value; }

    void reset() { *this = {}; }
};


int main()
{
    Calc calc{};
    calc.add(5).sub(3).mult(4);

    std::cout << calc.getValue() << '\n'; // 打印 8

    calc.reset();
    
    std::cout << calc.getValue() << '\n'; // 打印 0

    return 0;
}
```

***
## this和const对象

对于非const成员函数，this是指向非常量值的const指针（这意味着它不能指向其他对象，但指向的对象可以修改）。对于const成员函数，这是指向常量值的const指针（意味着指针不能指向其他对象，也不能修改被指向的对象）。

尝试调用常量对象上的非常量成员时生成的错误可能有点神秘：

```C++
error C2662: 'int Something::getValue(void)': cannot convert 'this' pointer from 'const Something' to 'Something &'
error: passing 'const Something' as 'this' argument discards qualifiers [-fpermissive]
```

当对常量对象调用非常量成员函数时，隐式this函数参数是非常量对象的const指针。但传入的值是具有指向常量对象的const指针类型。将常量对象的指针转换为非常量对象的指针需要丢弃常量限定符，不能隐式完成。某些编译器生成的编译器错误反映了编译器无法执行这种转换。

***
## 为什么 this 是指针而不是引用

由于this指针始终指向隐式对象（并且永远不能是空指针，除非我们做了一些事情导致未定义的行为），因此您可能想知道为什么这是指针而不是引用。答案很简单：当它被添加到C++时，引用还不存在。

如果今天将 this 添加到C++语言中，它无疑将是引用而不是指针。在其他更现代的类C++语言（如Java和C#）中，this 被实现为引用。

***
