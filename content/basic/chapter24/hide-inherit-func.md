---
title: "隐藏继承的功能"
date: 2024-10-08T17:45:57+08:00
---

## 更改继承来成员的访问级别

可以更改派生类中继承来成员的访问说明符。在派生类的对应的访问说明符下，使用「using」来声明基类的对应成员即可。

考虑以下程序：

```C++
#include <iostream>

class Base
{
private:
    int m_value {};

public:
    Base(int value)
        : m_value { value }
    {
    }

protected:
    void printValue() const { std::cout << m_value; }
};
```

由于Base::printValue()已声明为protected，因此只能由Base或其派生类调用它。外部无法访问它。

让我们定义一个Derived类，该类将printValue()的访问说明符更改为public:

```C++
class Derived: public Base
{
public:
    Derived(int value)
        : Base { value }
    {
    }

    // Base::printValue 继承而来是 protected, 所以外部无法调用该函数
    // 通过使用using，我们将其修改为 public
    using Base::printValue; // 注: 这里没有括号
};
```


这意味着下面的代码现在可以工作了：

```C++
int main()
{
    Derived derived { 7 };

    // 在Derived中 printValue 是 public，所以下面写法ok
    derived.printValue(); // 打印 7
    return 0;
}
```

只能更改派生类能够访问到的基类成员的访问说明符。因此，如果基类成员的访问说明符是private，则派生类不能将其改为protected或public，因为派生类不能访问基类的私有成员。

***
## 隐藏功能

在C++中，除了修改源代码外，无法从基类中删除或限制功能。然而，在派生类中，可以隐藏基类中存在的功能，以便不能通过派生类访问它。这可以通过简单地更改相关的访问说明符来完成。

例如，我们可以将public成员设置为private：

```C++
#include <iostream>

class Base
{
public:
	int m_value{};
};

class Derived : public Base
{
private:
	using Base::m_value;

public:
	Derived(int value) : Base { value }
	{
	}
};

int main()
{
	Derived derived{ 7 };
	std::cout << derived.m_value; // 错误: m_value 在 Derived 中是 private

	Base& base{ derived };
	std::cout << base.m_value; // okay: m_value 在 Base 中是 public

	return 0;
}
```

这允许我们使用一个设计糟糕的基类，并将其封装在派生类中。可以public继承Base的成员，然后修改其访问说明符。又或者，可以private继承Base，这将导致Base的所有成员首先被private继承。

然而，值得注意的是，虽然m_value在Derived类中是私有的，但它在基类中仍然是public的。因此，通过强制转换为Base&并直接访问成员，仍然可以破坏Derived中m_value的封装。

出于相同的原因，如果基类具有public virtual函数，而派生类将访问说明符更改为private，则外部仍然可以通过将派生对象强制转换为Base&并调用虚函数来访问private的派生函数。编译器允许这样做，因为该函数在Base中是公共的。然而，由于对象实际上是派生的，因此虚函数解析将解析（并调用）函数的（私有）派生版本。在运行时不强制执行访问控制。

```C++
#include <iostream>

class A
{
public:
    virtual void fun()
    {
        std::cout << "public A::fun()\n";
    }
};

class B : public A
{
private:
    virtual void fun()
    {
         std::cout << "private B::fun()\n";
   }
};

int main()
{
    B b {};
    b.fun();                  // 编译失败: B::fun() 是 private
    static_cast<A&>(b).fun(); // okay: A::fun() 是 public, 但在运行时会解析为 private B::fun()

    return 0;
}
```

也许令人惊讶的是，给定基类中的一组重载函数，没有办法更改单个重载的访问说明符。只能全部更改：

```C++
#include <iostream>

class Base
{
public:
    int m_value{};

    int getValue() const { return m_value; }
    int getValue(int) const { return m_value; }
};

class Derived : public Base
{
private:
	using Base::getValue; // 让所有的 getValue 函数变为 private

public:
	Derived(int value) : Base { value }
	{
	}
};

int main()
{
	Derived derived{ 7 };
	std::cout << derived.getValue();  // 错误: getValue() 在 Derived 中是 private
	std::cout << derived.getValue(5); // 错误: getValue(int) 在 Derived 中是 private

	return 0;
}
```

***
## 删除派生类中的函数

您还可以将派生类中成员函数标记为删除，这确保它们不能通过派生对象调用：

```C++
#include <iostream>
class Base
{
private:
	int m_value {};

public:
	Base(int value)
		: m_value { value }
	{
	}

	int getValue() const { return m_value; }
};

class Derived : public Base
{
public:
	Derived(int value)
		: Base { value }
	{
	}


	int getValue() const = delete; // 将这个函数标记为外部不可访问
};

int main()
{
	Derived derived { 7 };

	// 因为 getValue() 被删除了，所以下面这一行不会编译通过!
	std::cout << derived.getValue();

	return 0;
}
```

在上面的示例中，我们将getValue()函数标记为删除。这意味着当我们试图调用函数的派生类版本时，编译器将报错。请注意，getValue()的基类版本仍然可以访问。我们可以用下面两种方法之一调用Base:：


```C++
int main()
{
	Derived derived { 7 };

	// 可以通过 Base::getValue() 函数直接访问
	std::cout << derived.Base::getValue();

	// 可以将 Derived 转换为 Base 引用， 那么 getValue() 会被解析为 Base::getValue()
	std::cout << static_cast<Base&>(derived).getValue();

	return 0;
}
```

如果使用转换方法，则推荐转换为Base&而不是Base，以避免发生实际的复制。

***

{{< prevnext prev="/basic/chapter24/call-inherit-func-and-overload/" next="/basic/chapter24/multiple-inherit/" >}}
24.6 调用继承的函数与重写行为
<--->
24.8 多重继承
{{< /prevnext >}}
