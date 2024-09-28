---
title: "使用普通函数重载运算符"
date: 2024-08-20T12:01:51+08:00
---

在上一课中，我们将operator+重载为友元函数：

```C++
#include <iostream>
 
class Cents
{
private:
  int m_cents{};

public:
  Cents(int cents)
    : m_cents{ cents }
  {}

  // Cents + Cents 实现为友元函数
  friend Cents operator+(const Cents& c1, const Cents& c2);

  int getCents() const { return m_cents; }
};
 
// 注: 这个函数不是成员函数
Cents operator+(const Cents& c1, const Cents& c2)
{
	// 可以直接访问m_cents，因为本函数是 Cents 的友元函数
	// 返回 int，触发Cents的构造函数
  return { c1.m_cents + c2.m_cents };
}
 
int main()
{
  Cents cents1{ 6 };
  Cents cents2{ 8 };
  Cents centsSum{ cents1 + cents2 };
  std::cout << "I have " << centsSum.getCents() << " cents.\n";

  return 0;
}
```

使用友元函数重载运算符很方便，因为它使您可以直接访问正在操作的类的内部成员。在上面的示例中，我们的友元函数operator+版本直接访问了成员变量m_Cents。

然而，如果您不需要该访问能力，则可以将重载操作符编写为普通函数。请注意，上面的Cents类包含一个访问函数（getCents()），该函数允许我们在不必直接访问私有成员的情况下获取m_Cents。因此，我们可以将重载运算符+编写为非友元：

```C++
#include <iostream>

class Cents
{
private:
  int m_cents{};

public:
  Cents(int cents)
    : m_cents{ cents }
  {}

  int getCents() const { return m_cents; }
};

// 注: 这个函数，不是成员函数，也不是友元函数
Cents operator+(const Cents& c1, const Cents& c2)
{
  // 不再需要直接访问Cents的私有成员
  return Cents{ c1.getCents() + c2.getCents() };
}

int main()
{
  Cents cents1{ 6 };
  Cents cents2{ 8 };
  Cents centsSum{ cents1 + cents2 };
  std::cout << "I have " << centsSum.getCents() << " cents.\n";

  return 0;
}
```

由于普通函数和友元函数的工作方式几乎相同（它们只是对私有成员的访问级别不同），因此通常不会特别区分它们。一个区别是类中的友元函数声明也充当函数原型。对于普通函数版本，您必须提供自己的函数原型。

Cents.h：

```C++
#ifndef CENTS_H
#define CENTS_H

class Cents
{
private:
  int m_cents{};

public:
  Cents(int cents)
    : m_cents{ cents }
  {}
  
  int getCents() const { return m_cents; }
};

// 需要显示声明 operator+ 的原型，这样其它使用该.h文件的地方可以看见这个函数
Cents operator+(const Cents& c1, const Cents& c2);

#endif
```

Cents.cpp：

```C++
#include "Cents.h"

// 注: 这个函数，不是成员函数，也不是友元函数
Cents operator+(const Cents& c1, const Cents& c2)
{
  // 不再需要直接访问Cents的私有成员
  return { c1.getCents() + c2.getCents() };
}
```

main.cpp：

```C++
#include "Cents.h"
#include <iostream>

int main()
{
  Cents cents1{ 6 };
  Cents cents2{ 8 };
  Cents centsSum{ cents1 + cents2 }; // 如果 Cents.h 中没有对应的函数原型, 这里无法通过编译
  std::cout << "I have " << centsSum.getCents() << " cents.\n";

  return 0;
}
```

通常，如果可以使用现有的可用成员函数来实现，则应该首选普通函数而不是友元函数（接触类内部的函数越少越好）。然而，不要仅仅为了将操作符重载为普通函数而不是友元函数而添加额外的访问函数！

{{< alert success >}}
**最佳实践**

如果可以在不添加额外函数的情况下这样做，则有限将重载操作符作为普通函数，而不是友元函数。

{{< /alert >}}

***
