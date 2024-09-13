---
title: "再谈析构函数"
date: 2024-08-19T20:25:40+08:00
---

析构函数是另一种特殊类型的类成员函数，当该类的对象被销毁时执行。构造函数被设计为初始化类，而析构函数被设计为帮助清理类。

当对象正常超出作用域，或者使用delete关键字显式删除动态分配的对象时，类析构函数将自动调用（如果存在），以便在从内存中删除对象之前进行任何必要的清理。对于简单的类（那些只初始化普通成员变量的值的类），不需要析构函数，因为C++将自动为您清理内存。

然而，如果类对象持有任何资源（例如动态内存、文件或数据库句柄），或者如果您需要在销毁对象之前进行任何类型的维护，析构函数是这样做的最佳位置，因为它通常是销毁对象之前发生的最后一件事。

***
## 析构函数命名

与构造函数一样，析构函数具有特定的命名规则:

1. 析构函数与类名一致，外加一个前导的 ~
2. 析构函数无任何参数
3. 析构函数无返回值

类只能有一个析构函数。

通常，您不应该显式调用析构函数（因为当对象被销毁时它将自动调用），因为很少有情况下您希望多次清理对象。析构函数可以安全地调用其他成员函数，因为对象直到析构函数执行后才被销毁。

***
## 析构函数示例

让我们来看一个使用析构函数的简单类:

```C++
#include <iostream>
#include <cassert>
#include <cstddef>

class IntArray
{
private:
	int* m_array{};
	int m_length{};

public:
	IntArray(int length) // 构造函数
	{
		assert(length > 0);

		m_array = new int[static_cast<std::size_t>(length)]{};
		m_length = length;
	}

	~IntArray() // 析构函数
	{
		// 删除初始化时动态分配的数组
		delete[] m_array;
	}

	void setValue(int index, int value) { m_array[index] = value; }
	int getValue(int index) { return m_array[index]; }

	int getLength() { return m_length; }
};

int main()
{
	IntArray ar ( 10 ); // 分配 10 个int
	for (int count{ 0 }; count < ar.getLength(); ++count)
		ar.setValue(count, count+1);

	std::cout << "The value of element 5 is: " << ar.getValue(5) << '\n';

	return 0;
} // ar 在这里销毁, 所以 ~IntArray() 析构函数在这里被调用
```

该程序生成结果:

```C++
The value of element 5 is: 6
```

在main()的第一行，我们实例化了一个名为ar的新IntArray类对象，并传入长度为10的值。这将调用构造函数，该构造函数为数组成员动态分配内存。我们必须在这里使用动态分配，因为我们在编译时不知道数组的长度是多少（调用方决定）。

在main()的末尾，ar超出作用域。这导致调用~IntArray()析构函数，这将删除在构造函数中分配的数组！

{{< alert success >}}
**一个提醒**

在介绍std::vector和列表构造函数中，我们注意到在初始化具有长度（而不是元素列表）的数组/容器/列表类时，应该使用基于括号的初始化。因此，我们使用  “IntArray ar ( 10 );”  初始化IntArray。

{{< /alert >}}

***
## 构造函数和析构函数的调用时机

如前所述，在创建对象时调用构造函数，在销毁对象时调用析构函数。在下面的示例中，我们在构造函数和析构函数中使用cout语句来显示这一点:

```C++
#include <iostream>

class Simple
{
private:
    int m_nID{};

public:
    Simple(int nID)
        : m_nID{ nID }
    {
        std::cout << "Constructing Simple " << nID << '\n';
    }

    ~Simple()
    {
        std::cout << "Destructing Simple" << m_nID << '\n';
    }

    int getID() { return m_nID; }
};

int main()
{
    // 在栈上分配了一个对象 simple
    Simple simple{ 1 };
    std::cout << simple.getID() << '\n';

    // 动态分配了一个 Simple 对象
    Simple* pSimple{ new Simple{ 2 } };
    
    std::cout << pSimple->getID() << '\n';

    // pSimple 动态分配的, 所以这里手动delete它.
    delete pSimple;

    return 0;
} // simple 超出作用域
```

该程序产生以下结果:

```C++
Constructing Simple 1
1
Constructing Simple 2
2
Destructing Simple 2
Destructing Simple 1
```

注意，“Simple1”在“Simple2”之后被销毁，因为我们在函数结束之前delete了pSimple，而simple直到 main() 结束才被销毁。

全局变量在main()之前构造，在main()之后销毁。

***
## RAII

RAII（Resource Acquisition Is Initialization，资源获取即初始化）是一种编程技术，其中资源使用与具有自动持续时间的对象（例如，非动态分配的对象）的生命周期相关联。在C++中，RAII是通过具有构造函数和析构函数的类来实现的。资源（如内存、文件或数据库句柄等）通常在对象的构造函数中获取（尽管可以在创建对象后获取）。然后，可以在对象处于活动状态时使用该资源。销毁对象时，资源在析构函数中释放。RAII的主要优势是，它有助于防止资源泄漏（例如，内存未被释放），因为所有持有资源的对象都会自动清理。

本课顶部的IntArray类是一个实现RAII的类的示例——在构造函数中分配，在析构函数中释放。string和std::vector是标准库中遵循RAII的类的示例——动态内存在初始化时获得，在销毁时自动清理。

***
## 关于std::exit()函数的警告

注意，如果使用std::exit()函数，程序将终止，并且不会调用析构函数。如果您依赖析构函数来执行必要的清理工作（例如，在退出之前将某些内容写入日志文件或数据库），请谨慎使用。

***
## 总结

正如您所看到的，当构造函数和析构函数一起使用时，您的类可以来辅助做初始化和清理，而使用类程序员不必做任何特殊的工作！这降低了出错的概率，并使类更易于使用。

***

{{< prevnext prev="/basic/chapter19/new-delete-arr/" next="/basic/chapter19/ptr-to-ptr/" >}}
19.1 动态分配数组
<--->
19.3 指向指针和动态多维数组的指针
{{< /prevnext >}}
