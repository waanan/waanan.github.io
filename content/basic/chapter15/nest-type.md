---
title: "嵌套类型（成员类型）"
date: 2024-06-24T18:56:16+08:00
---

考虑以下简短的程序：

```C++
#include <iostream>

enum class FruitType
{
	apple,
	banana,
	cherry
};

class Fruit
{
private:
	FruitType m_type { };
	int m_percentageEaten { 0 };

public:
	Fruit(FruitType type) :
		m_type { type }
	{
	}

	FruitType getType() { return m_type; }
	int getPercentageEaten() { return m_percentageEaten; }

	bool isCherry() { return m_type == FruitType::cherry; }

};

int main()
{
	Fruit apple { FruitType::apple };
	
	if (apple.getType() == FruitType::apple)
		std::cout << "I am an apple";
	else
		std::cout << "I am not an apple";
	
	return 0;
}
```

这个程序没有问题。但由于枚举类FruitType旨在与Fruit类一起使用，但它独立于类存在，这让我们不得不记住他们的关联。

***
## 嵌套类型（成员类型）

到目前为止，我们已经看到了类类型的两种不同成员：数据成员和成员函数。在上面的例子中，Fruit类同时具有这两个特性。

类类型支持另一种类型的成员：嵌套类型（也称为成员类型）。要创建嵌套类型，只需在类内的适当访问说明符下定义类型。

下面是与上面相同的程序，重写为使用在Fruit类中定义的嵌套类型：

```C++
#include <iostream>

class Fruit
{
public:
	// FruitType 移动到了 Fruit 内部, 在 public 下面
    // 同时重命名为Type，并定义为 enum 而不是 enum class
	enum Type
	{
		apple,
		banana,
		cherry
	};

private:
	Type m_type {};
	int m_percentageEaten { 0 };

public:
	Fruit(Type type) :
		m_type { type }
	{
	}

	Type getType() { return m_type;  }
	int getPercentageEaten() { return m_percentageEaten;  }

	bool isCherry() { return m_type == cherry; } // 在 Fruit 内, 不需要使用 FruitType:: 前缀
};

int main()
{
	// 注: 在 class 外部, 使用 Fruit:: 前缀访问
	Fruit apple { Fruit::apple };
	
	if (apple.getType() == Fruit::apple)
		std::cout << "I am an apple";
	else
		std::cout << "I am not an apple";
	
	return 0;
}
```

这里有几点值得指出。

首先，请注意，FruitType现在在类中定义，由于稍后将讨论的原因，它已被重命名为Type。

其次，在类的顶部定义了嵌套类型Type。嵌套类型名称在使用之前必须完全定义，因此通常首先定义它们。

第三，嵌套类型遵循正常的访问规则。类型是在public访问说明符下定义的，因此类型名称和枚举元素可以由外部直接访问。

第四，类类型充当中声明的名称的作用域，就像命名空间一样。因此，Type的完全限定名为Fruit::Type，而apple枚举元素的完全限定名称为Fruit::apple。

在类的成员中，不需要使用完全限定名。例如，在成员函数 isCherry() 中，在没有Fruit:: 作用域限定符的情况下访问cherry枚举元素。

在类之外，必须使用完全限定的名称（例如，Fruit::apple ）。我们将FruitType重命名为Type，以便可以使用 Fruit::Type（而不是更冗余的 Fruit::FruitType ）。

最后，将枚举类型从 enum class 更改为 enum。由于类本身现在充当作用域，因此使用 enum class 有些多余。更改为未限定作用域的枚举意味着可以用Fruit::apple的形式访问枚举元素，而不是必须使用的较长的 Fruit::Type::apple 。

{{< alert success >}}
**最佳实践**

在类类型的顶部定义任何嵌套类型。

{{< /alert >}}

***
## 嵌套的typedef和类型别名

类类型还可以包含嵌套的typedef或类型别名：

```C++
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
public:
    using IDType = int;

private:
    std::string m_name{};
    IDType m_id{};
    double m_wage{};

public:
    Employee(std::string_view name, IDType id, double wage)
        : m_name { name }
        , m_id { id }
        , m_wage { wage }
    {
    }

    const std::string& getName() { return m_name; }
    IDType getId() { return m_id; } // 类内部可以使用不带限定名的类型
};

int main()
{
    Employee john { "John", 1, 45000 };
    Employee::IDType id { john.getId() }; // 类外部必须使用完全限定名

    std::cout << john.getName() << " has id: " << id << '\n';

    return 0;
}
```

这将打印：

```C++
John has id: 1
```

请注意，在类内部，可以直接使用IDType，但在类外部，必须使用完全限定名Employee::IDType。

我们之前讨论过Typedef和类型别名，它们在这里的作用是相同的。C++标准库中的类通常使用嵌套的typedef。截至编写时，std::string定义了十个嵌套的typedef！

***
## 嵌套类和对外部类成员的访问

类将其他类作为嵌套类型是相当少见的，但这是可行的。在C++中，嵌套类不能访问外部类的this指针，嵌套类也不能直接访问外部类的成员。这是因为嵌套类可以独立于外部类进行实例化（在这种情况下，将没有可访问的外部类实例和成员！）

然而，由于嵌套类是外部类的成员，因此它们可以访问外部类的任何私有成员。

用一个例子来说明：

```C++
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
public:
    using IDType = int;

    class Printer
    {
    public:
        void print(const Employee& e) const
        {
            // Printer 不能使用 Employee 的 `this` 指针
            // 所以不能直接使用 m_name 和 m_id
            // 代替的方案是, 可以传入一个 Employee 对象
            // 因为 Printer 是 Employee 的成员,
            // 所以可以直接访问私有成员 e.m_name 和 e.m_id
            std::cout << e.m_name << " has id: " << e.m_id << '\n';
        }
    };

private:
    std::string m_name{};
    IDType m_id{};
    double m_wage{};

public:
    Employee(std::string_view name, IDType id, double wage)
        : m_name{ name }
        , m_id{ id }
        , m_wage{ wage }
    {
    }

    // 这个例子中不提供访问函数
};

int main()
{
    const Employee john{ "John", 1, 45000 };
    const Employee::Printer p{}; // 实例化嵌套类的实例
    p.print(john);

    return 0;
}
```

这将打印：

```C++
John has id: 1
```

有一种情况下，嵌套类更常用。在标准库中，大多数迭代器类都被实现为容器的嵌套类，它们被设计为在容器上迭代。例如，std::string::iterator被实现为std:∶string的嵌套类。我们将在未来的一章中介绍迭代器。

***
## 嵌套类型不能前向声明

嵌套类型还有一个值得一提的限制——嵌套类型不能被前向声明。在C++的未来版本中，可能取消此限制。

***

{{< prevnext prev="/basic/chapter15/class-header-file/" next="/basic/chapter15/destruct-intro/" >}}
15.1 类和头文件
<--->
15.3 析构函数简介
{{< /prevnext >}}
