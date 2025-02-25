---
title: "异常、类和继承"
date: 2025-02-12T14:07:59+08:00
---

## 异常和成员函数

到目前为止，在本教程中，您只看到了在非成员函数中使用的异常。然而，异常在成员函数中同样有用，在重载运算符中更是如此。考虑将以下重载IntArray的「operator[]」代码：

```C++
int& IntArray::operator[](const int index)
{
    return m_data[index];
}
```

尽管只要index是有效的数组索引，该函数就可以很好地工作，但该函数严重缺乏一些错误检查。我们可以添加断言语句来确保索引有效：

```C++
int& IntArray::operator[](const int index)
{
    assert (index >= 0 && index < getLength());
    return m_data[index];
}
```

现在，如果用户传入无效的索引，程序将抛出断言错误。不幸的是，由于重载运算符对于参数和返回值类型有严格要求，因此无法灵活地将错误码或布尔值传递给调用方来处理。然而，由于异常不会更改函数的签名，因此可以在这里使用它。下面是一个示例：

```C++
int& IntArray::operator[](const int index)
{
    if (index < 0 || index >= getLength())
        throw index;

    return m_data[index];
}
```

现在，如果用户传入无效的索引，「operator[]」将抛出int异常。

***
## 当构造函数执行失败

构造函数是类的另一个领域，异常可能在其中有用。如果构造函数由于某种原因必须失败（例如，用户传入了无效的输入），只需抛出一个异常来指示对象创建失败。在这种情况下，对象的构造被中止，并且所有类成员（在构造函数的函数体执行之前已经创建和初始化）都像往常一样被销毁。

然而，这不会调用类的析构函数（因为对象从未完成构造）。由于析构函数从不执行，因此不能依赖析构函数来清理已经分配的任何资源。

这导致了这样一个问题：如果我们在构造函数中分配了资源，然后在构造函数完成之前发生异常，我们应该做什么。如何确保我们已经分配的资源得到适当的清理？一种方法是包装任何可能在try块中失败的代码，使用相应的catch块捕获异常并进行任何必要的清理，然后重新引发异常（后面章节讨论）。然而，这增加了许多混乱，并且很容易出错，特别是当类分配多个资源的时候。

幸运的是，有一种更好的方法。利用即使构造函数失败也会销毁类成员的事实，如果在类的成员内部（而不是在构造函数本身中）进行资源分配，则当这些成员被销毁时，它们可以被清理到。

下面是一个示例：

```C++
#include <iostream>

class Member
{
public:
	Member()
	{
		std::cerr << "Member allocated some resources\n";
	}

	~Member()
	{
		std::cerr << "Member cleaned up\n";
	}
};

class A
{
private:
	int m_x {};
	Member m_member;

public:
	A(int x) : m_x{x}
	{
		if (x <= 0)
			throw 1;
	}
	
	~A()
	{
		std::cerr << "~A\n"; // 不会被调用
	}
};


int main()
{
	try
	{
		A a{0};
	}
	catch (int)
	{
		std::cerr << "Oops\n";
	}

	return 0;
}
```

这将打印：

```C++
Member allocated some resources
Member cleaned up
Oops
```

在上面的程序中，当类A抛出异常时，A的所有成员都被销毁。m_member的析构函数被调用，提供了清理它分配资源的机会。

这是RAII如此受欢迎的部分原因——即使在特殊情况下，实现RAII的类也能够在它被销毁时进行清理。

然而，创建一个自定义类（如Member）来管理资源分配并不高效。幸运的是，C++标准库附带了与RAII兼容的类，用于管理常见的资源类型，例如文件（std::fstream，下一章介绍）和动态内存（std::unique_ptr和其他智能指针）。

例如，不是这样：

```C++
class Foo
private:
    int* ptr; // Foo 需要处理内存分配和释放
```

而是以下操作：

```C++
class Foo
private:
    std::unique_ptr<int> ptr; // std::unique_ptr 来处理内存分配和释放
```

在前一种情况下，如果Foo的构造函数在ptr分配其动态内存后失败，则Foo必须负责清理，这可能是一个挑战。在后一种情况下，如果Foo的构造函数在ptr分配其动态内存后失败，则ptr的析构函数将执行并将该内存返回给系统。将资源处理委托给符合RAII的成员时，Foo不必执行任何显式清理！

***
## 异常类

使用基本数据类型（如int）作为异常类型的主要问题之一是，它们本质上是模糊的。一个更大的问题是，当一个try块中有多个语句或函数调用时，消除异常的含义的歧义。

```C++
// Using the IntArray overloaded operator[] above

try
{
    int* value{ new int{ array[index1] + array[index2]} };
}
catch (int value)
{
    // What are we catching here?
}
```

在这个例子中，如果我们捕获一个int异常，那它到底告诉了我们什么？数组索引之一是否超出界限？运算符+是否导致整数溢出？操作员new是否因内存不足而失败？不幸的是，在这种情况下，没有简单的方法来消除歧义。虽然我们可以抛出constchar*异常来解决识别错误的问题，但这仍然不能为我们提供以不同的方式处理来自不同来源的异常的能力。

解决这个问题的一种方法是使用异常类。异常类只是一个普通类，专门设计为作为异常抛出。让我们设计一个简单的异常类，与IntArray类一起使用：

```C++
#include <string>
#include <string_view>

class ArrayException
{
private:
	std::string m_error;

public:
	ArrayException(std::string_view error)
		: m_error{ error }
	{
	}

	const std::string& getError() const { return m_error; }
};
```

下面是使用该类的完整程序：

```C++
#include <iostream>
#include <string>
#include <string_view>

class ArrayException
{
private:
	std::string m_error;

public:
	ArrayException(std::string_view error)
		: m_error{ error }
	{
	}

	const std::string& getError() const { return m_error; }
};

class IntArray
{
private:
	int m_data[3]{}; // assume array is length 3 for simplicity

public:
	IntArray() {}

	int getLength() const { return 3; }

	int& operator[](const int index)
	{
		if (index < 0 || index >= getLength())
			throw ArrayException{ "Invalid index" };

		return m_data[index];
	}

};

int main()
{
	IntArray array;

	try
	{
		int value{ array[5] }; // out of range subscript
	}
	catch (const ArrayException& exception)
	{
		std::cerr << "An array exception occurred (" << exception.getError() << ")\n";
	}
}
```

使用这样的类，我们可以让异常返回发生的问题的描述，这为错误提供了上下文。由于ArrayException是其自己的唯一类型，因此我们可以专门捕获数组类引发的异常，并根据需要将它们与其他异常区别对待。

请注意，异常处理程序应该通过引用而不是通过值来捕获类异常对象。这可以防止编译器在捕获异常的位置复制该异常，当异常是类对象时，这可能会非常昂贵，并防止在处理派生异常类（我们稍后将讨论）时进行对象切片。通常应避免通过指针捕获异常，除非您有特定的原因这样做。

{{< alert success >}}
**最佳做法**

基本类型的异常可以被值捕获，因为它们的复制成本很低。类类型的异常应由（const）引用捕获，以防止昂贵的复制和切片。

{{< /alert >}}

***
## 例外和继承

由于可以将类作为异常抛出，并且类可以从其他类派生，因此我们需要考虑将继承的类用作异常时会发生什么情况。事实证明，异常处理程序不仅匹配特定类型的类，还匹配从该特定类型派生的类！考虑以下示例：

```C++
#include <iostream>

class Base
{
public:
    Base() {}
};

class Derived: public Base
{
public:
    Derived() {}
};

int main()
{
    try
    {
        throw Derived();
    }
    catch (const Base& base)
    {
        std::cerr << "caught Base";
    }
    catch (const Derived& derived)
    {
        std::cerr << "caught Derived";
    }

    return 0;
}	
```

在上面的例子中，我们抛出了一个Derived类型的异常。然而，该程序的输出是：

发生了什么事？

首先，如上所述，派生类将被基类型的处理程序捕获。因为Derived是从Base派生而来的，所以Derivedis-aBase（它们具有is-a关系）。其次，当C++试图为引发的异常查找处理程序时，它会按顺序执行。因此，C++所做的第一件事是检查Base的异常处理程序是否与Derived异常匹配。因为Derived是一个Base，所以答案是yes，并且它执行Base类型的catch块！在这种情况下，Derived的catch块甚至从未测试过。

为了使此示例按预期工作，我们需要翻转catch块的顺序：

```C++
#include <iostream>

class Base
{
public:
    Base() {}
};

class Derived: public Base
{
public:
    Derived() {}
};

int main()
{
    try
    {
        throw Derived();
    }
    catch (const Derived& derived)
    {
        std::cerr << "caught Derived";
    }
    catch (const Base& base)
    {
        std::cerr << "caught Base";
    }

    return 0;
}	
```

这样，Derived处理程序将在捕获Derived类型的对象时获得第一个机会（在Base处理程序可以之前）。Base类型的对象将与派生处理程序不匹配（Derived是Base，但Base不是Deriveed），因此将“落到”Base处理程序。

使用基类的处理程序来捕获派生类型的异常的能力被证明是非常有用的。

{{< alert success >}}
**规则**

派生异常类的句柄应列在基类的句柄之前。

{{< /alert >}}

***
## 标准：：异常

标准库中的许多类和运算符在失败时引发异常类。例如，如果操作符new无法分配足够的内存，则它可以抛出std:：bad_alloc。失败的dynamic_cast将引发std:：bad_cast。从C++20开始，有28个不同的异常类可以抛出，在每个后续的语言标准中都添加了更多的异常类。

好消息是，所有这些异常类都派生自一个名为std:：exception的类（在<exception>头中定义）。exception是一个小型接口类，旨在充当C++标准库引发的任何异常的基类。

在大多数情况下，当标准库抛出异常时，我们不会关心它是错误的分配、错误的强制转换还是其他什么。我们只关心灾难性的错误，现在我们的程序正在爆炸。由于std:：exception，我们可以设置一个异常处理程序来捕获类型为std：：except的异常，并且我们最终将在一个地方同时捕获std：:exception.和所有派生的异常。简单！

```C++
#include <cstddef> // for std::size_t
#include <exception> // for std::exception
#include <iostream>
#include <limits>
#include <string> // for this example

int main()
{
    try
    {
        // Your code using standard library goes here
        // We'll trigger one of these exceptions intentionally for the sake of the example
        std::string s;
        s.resize(std::numeric_limits<std::size_t>::max()); // will trigger a std::length_error or allocation exception
    }
    // This handler will catch std::exception and all the derived exceptions too
    catch (const std::exception& exception)
    {
        std::cerr << "Standard exception: " << exception.what() << '\n';
    }

    return 0;
}
```

在作者的机器上，上述程序打印：

上面的例子应该非常简单。值得注意的一点是，std:：exception有一个名为what（）的虚拟成员函数，该函数返回异常的C样式字符串描述。大多数派生类都重写what（）函数来更改消息。注意，该字符串仅用于描述性文本——不要将其用于比较，因为它不能保证在编译器之间是相同的。

有时，我们希望以不同的方式处理特定类型的异常。在这种情况下，我们可以为该特定类型添加处理程序，并让所有其他处理程序“落到”基础处理程序。考虑：

```C++
try
{
     // code using standard library goes here
}
// This handler will catch std::length_error (and any exceptions derived from it) here
catch (const std::length_error& exception)
{
    std::cerr << "You ran out of memory!" << '\n';
}
// This handler will catch std::exception (and any exception derived from it) that fall
// through here
catch (const std::exception& exception)
{
    std::cerr << "Standard exception: " << exception.what() << '\n';
}
```

在本例中，类型为std:：length_error的异常将由第一个处理程序捕获并在那里处理。第二个处理程序将捕获std:：exception类型的异常和所有其他派生类。

这样的继承层次结构允许我们使用特定的处理程序来定位特定的派生异常类，或者使用基类处理程序来捕获整个异常层次结构。这允许我们在一定程度上控制我们想要处理的异常类型，同时确保我们不必做太多工作来捕获层次结构中的“其他一切”。

***
## 直接使用标准异常

没有任何东西直接抛出std:：异常，您也不应该这样做。然而，如果其他标准异常类充分地代表了您的需求，那么您应该可以在标准库中随意抛出它们。您可以找到cppreference上所有标准异常的列表。

std:：runtime_error（作为stdexcept头的一部分包含）是一个流行的选择，因为它具有通用名称，并且其构造函数采用可定制的消息：

```C++
#include <exception> // for std::exception
#include <iostream>
#include <stdexcept> // for std::runtime_error

int main()
{
	try
	{
		throw std::runtime_error("Bad things happened");
	}
	// This handler will catch std::exception and all the derived exceptions too
	catch (const std::exception& exception)
	{
		std::cerr << "Standard exception: " << exception.what() << '\n';
	}

	return 0;
}
```

这将打印：

***
## 从std::exception或std:：runtime_error派生您自己的类

当然，您可以从std:：exception派生自己的类，并重写虚拟what（）const成员函数。下面是与上面相同的程序，其中ArrayException派生自std:：exception:

```C++
#include <exception> // for std::exception
#include <iostream>
#include <string>
#include <string_view>

class ArrayException : public std::exception
{
private:
	std::string m_error{}; // handle our own string

public:
	ArrayException(std::string_view error)
		: m_error{error}
	{
	}

	// std::exception::what() returns a const char*, so we must as well
	const char* what() const noexcept override { return m_error.c_str(); }
};

class IntArray
{
private:
	int m_data[3] {}; // assume array is length 3 for simplicity

public:
	IntArray() {}
	
	int getLength() const { return 3; }

	int& operator[](const int index)
	{
		if (index < 0 || index >= getLength())
			throw ArrayException("Invalid index");

		return m_data[index];
	}

};

int main()
{
	IntArray array;

	try
	{
		int value{ array[5] };
	}
	catch (const ArrayException& exception) // derived catch blocks go first
	{
		std::cerr << "An array exception occurred (" << exception.what() << ")\n";
	}
	catch (const std::exception& exception)
	{
		std::cerr << "Some other std::exception occurred (" << exception.what() << ")\n";
	}
}
```

请注意，虚拟函数what（）具有说明符noexcept（这意味着函数承诺不抛出异常本身）。因此，我们的重写还应该具有说明符noexcept。

由于std:：runtime_error已经具有字符串处理功能，因此它也是派生异常类的流行基类。std:：runtime_error可以采用C样式的字符串参数，也可以采用const std：：string&parameter。

下面是从std:：runtime_error派生的相同示例：

```C++
#include <exception> // for std::exception
#include <iostream>
#include <stdexcept> // for std::runtime_error
#include <string>

class ArrayException : public std::runtime_error
{
public:
	// std::runtime_error takes either a null-terminated const char* or a const std::string&.
	// We will follow their lead and take a const std::string&
	ArrayException(const std::string& error)
		: std::runtime_error{ error } // std::runtime_error will handle the string
	{
	}


        // no need to override what() since we can just use std::runtime_error::what()
};

class IntArray
{
private:
	int m_data[3]{}; // assume array is length 3 for simplicity

public:
	IntArray() {}

	int getLength() const { return 3; }

	int& operator[](const int index)
	{
		if (index < 0 || index >= getLength())
			throw ArrayException("Invalid index");

		return m_data[index];
	}

};

int main()
{
	IntArray array;

	try
	{
		int value{ array[5] };
	}
	catch (const ArrayException& exception) // derived catch blocks go first
	{
		std::cerr << "An array exception occurred (" << exception.what() << ")\n";
	}
	catch (const std::exception& exception)
	{
		std::cerr << "Some other std::exception occurred (" << exception.what() << ")\n";
	}
}
```

您可以决定是创建自己的独立异常类、使用标准异常类，还是从std:：exception或std:：runtime_error派生自己的异常类。所有这些都是有效的方法，取决于您的目标。

***
## 异常的生存期

当抛出异常时，被抛出的对象通常是在堆栈上分配的临时或局部变量。然而，异常处理过程可能会展开函数，导致函数的所有局部变量被销毁。那么，被抛出的异常对象如何在堆栈展开中幸存下来呢？

当抛出异常时，编译器将异常对象的副本复制到为处理异常而保留的某个未指定内存（调用堆栈之外）。这样，不管堆栈是否展开或展开多少次，都会持久化异常对象。在处理异常之前，确保异常存在。

这意味着被抛出的对象通常需要是可复制的（即使堆栈实际上没有解除绑定）。智能编译器可以改为执行移动，或者在特定情况下完全删除副本。

下面的一个示例显示了当我们尝试抛出不可复制的派生对象时发生的情况：

```C++
#include <iostream>

class Base
{
public:
    Base() {}
};

class Derived : public Base
{
public:
    Derived() {}

    Derived(const Derived&) = delete; // not copyable
};

int main()
{
    Derived d{};

    try
    {
        throw d; // compile error: Derived copy constructor was deleted
    }
    catch (const Derived& derived)
    {
        std::cerr << "caught Derived";
    }
    catch (const Base& base)
    {
        std::cerr << "caught Base";
    }

    return 0;
}
```

编译此程序时，编译器将抱怨派生副本构造函数不可用，并停止编译。

异常对象不应保留堆栈分配对象的指针或引用。如果引发的异常导致堆栈展开（导致堆栈分配对象的销毁），则这些指针或引用可能会悬而未决。

{{< alert success >}}
**提示**

异常对象需要是可复制的。

{{< /alert >}}

***