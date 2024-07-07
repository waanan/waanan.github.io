---
title: "引用限定符"
date: 2024-06-24T18:56:16+08:00
---

{{< alert success >}}
**注**

这是一节选修课。建议您稍微通读一下，以熟悉材料，继续学习未来的课程不需要全面理解这里。

{{< /alert >}}

在前面学习返回对数据成员的引用的成员函数中，讨论了当隐式对象是右值时，返回对数据成员的引用是危险的。下面简要回顾一下：

```C++
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
private:
	std::string m_name{};

public:
	Employee(std::string_view name): m_name { name } {}
	const std::string& getName() const { return m_name; } //  返回 const 引用
};

// createEmployee() 按值返回一个 Employee (意味着返回的是一个右值)
Employee createEmployee(std::string_view name)
{
	Employee e { name };
	return e;
}

int main()
{
	// Case 1: okay: 在同一个表达式中使用右值的成员的引用
	std::cout << createEmployee("Frank").getName() << '\n';

	// Case 2: 有问题: 保存右值返回的成员的引用，稍后使用
	const std::string& ref { createEmployee("Garbo").getName() }; // 悬空引用，createEmployee() 创建的临时对象已经被销毁
	std::cout << ref << '\n'; // 未定义的行为

	return 0;
}
```

在案例2中，从createEmployee("Garbo") 返回的右值对象在初始化ref后被销毁，使ref引用刚被销毁的数据成员。ref的后续使用造成未定义的行为。

这有点棘手。

1. 如果getName()函数按值返回，会生成昂贵且不必要的副本。
2. 如果getName()函数通过常量引用返回，则这是高效的（因为没有生成std::string的副本），但当调用的对象是右值时，可能会被误用（导致未定义的行为）。


由于成员函数通常在左值对象上调用，因此传统的选择是通过常量引用返回，并在隐式对象是右值的情况下简单地避免误用返回的引用。

***
## 引用限定符

上述挑战的根源是，希望一个函数服务于两种不同的情况（一种是隐式对象是左值，另一种是隐式对象是右值）。一种情况下的最佳方案对另一种情况并不理想。

为了帮助解决这些问题，C++11引入了一个鲜为人知的特性，称为引用限定符，它允许根据是在左值还是右值对象上调用成员函数来重载它。使用这个特性，可以创建getName()的两个版本——一个用于对象是左值的情况，另一个用于对象为右值的情况。

首先，从getName() 的非引用限定版本开始

```C++
std::string& getName() const { return m_name; } // 在左值和右值对象上均可调用
```

为了引用限定此函数，将一个「&」限定符添加到只匹配左值对象的重载中，并将一个「&&」限定符加到只匹配右值对象的重载中：

```C++
const std::string& getName() const &  { return m_name; } //  & 限定只匹配左值隐式对象, 按引用返回
std::string        getName() const && { return m_name; } // && 限定只匹配右值隐式对象, 按值返回
```

因为这些函数是不同的重载，所以它们可以有不同的返回类型！左值限定重载通过常量引用返回，而右值限定重载则通过值返回。

下面是上面的完整示例：

```C++
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
private:
	std::string m_name{};

public:
	Employee(std::string_view name): m_name { name } {}

	const std::string& getName() const &  { return m_name; } //  & 限定只匹配左值隐式对象, 按引用返回
	std::string        getName() const && { return m_name; } // && 限定只匹配右值隐式对象, 按值返回
};

// createEmployee() 按值返回一个 Employee (意味着返回的是一个右值)
Employee createEmployee(std::string_view name)
{
	Employee e { name };
	return e;
}

int main()
{
	Employee joe { "Joe" };
	std::cout << joe.getName() << '\n'; // Joe 是 左值, 调用的是 std::string& getName() & (返回引用)
    
	std::cout << createEmployee("Frank").getName() << '\n'; // Frank 是 右值, 调用的是 std::string getName() && (返回拷贝)

	return 0;
}
```

这允许我们在隐式对象是左值时做高效率的事情，而在隐式目标是右值时做安全的事情。

{{< alert success >}}
**对于高级读者**

当隐式对象是非常量临时对象时，从性能角度来看，上面的getName()的上述右值重载可能是次优的。在这种情况下，隐式对象无论如何都将在表达式末尾死亡。因此，可以让它尝试移动成员（使用std::move），而不是返回成员的副本（可能很昂贵）。

这可以通过为非常量值添加以下重载getter来实现：

```C++
        // 如果隐式对象是 非 const 右值, 使用 std::move 去尝试移动 m_name
	std::string getName() && { return std::move(m_name); }
```

这既可以与const 右值 getter共存，也可以直接使用它（因为const 右值相当少见）。

std:∶move将在之后的课程介绍。

{{< /alert >}}

***
## 关于引用限定成员函数的一些注释

首先，对于给定的函数，非引用限定重载和引用限定过载不能共存。只用使用一个或另一个。

其次，如果仅提供左值限定重载（即未定义右值限定版本），则对具有右值隐式对象的函数的任何调用都将导致编译错误。这提供了一种有用的方法，可以完全防止将函数与右值隐式对象一起使用。

***
## 那么，为什么不建议使用引用限定符呢？

虽然引用限定符有用，但以这种方式使用它们有一些缺点。

1. 向每个返回引用的getter添加右值重载会给类增加混乱，而只是为了解决不常见的情况，通过良好的习惯很容易避免问题。
2. 通过值返回右值重载意味着必须支付复制（或移动）的成本，即使在可以安全使用引用的情况下（例如，在课程顶部的示例的情况1）。


此外：

1. 大多数C++开发人员都不知道该功能（这可能会导致错误或使用效率低下）。
2. 标准库通常不使用此功能。


基于以上所有内容，不建议将引用限定符用作最佳实践。相反，建议始终立即使用访问函数的结果，而不要保存返回的引用以供以后使用。

***