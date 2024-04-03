---
title: "结构体指针和引用的成员选择操作"
date: 2024-03-08T13:20:57+08:00
---

## 结构体引用的成员选择

在前面，我们展示了可以使用成员选择操作符（.）从结构体对象中选择成员：

```C++
#include <iostream>

struct Employee
{
    int id {};
    int age {};
    double wage {};
};

int main()
{
    Employee joe { 1, 34, 65000.0 };

    // 使用成员选择操作符 (.) 从结构体对象中选择成员
    ++joe.age; // Joe 大了一岁
    joe.wage = 68000.0; // Joe 升职加薪了
    
    return 0;
}
```

由于对象的引用就像对象本身一样，因此也可以使用成员选择操作符（.）对结构体的引用来选择成员：

```C++
#include <iostream>

struct Employee
{
    int id{};
    int age{};
    double wage{};
};

void printEmployee(const Employee& e)
{
    // 使用成员选择操作符 (.) 从结构体对象的引用中选择成员
    std::cout << "Id: " << e.id << '\n';
    std::cout << "Age: " << e.age << '\n';
    std::cout << "Wage: " << e.wage << '\n';
}

int main()
{
    Employee joe{ 1, 34, 65000.0 };

    ++joe.age;
    joe.wage = 68000.0;

    printEmployee(joe);

    return 0;
}
```

***
## 结构体指针的成员选择

然而，如果有指向结构体的指针，则使用成员选择运算符（.）会编译失败：

```C++
#include <iostream>

struct Employee
{
    int id{};
    int age{};
    double wage{};
};

int main()
{
    Employee joe{ 1, 34, 65000.0 };

    ++joe.age;
    joe.wage = 68000.0;

    Employee* ptr{ &joe };
    std::cout << ptr.id << '\n'; // 编译失败: 不能对指针使用 operator. 

    return 0;
}
```

对于普通变量或引用，可以直接访问对象。然而，由于指针保存地址，首先需要解引用指针以获取对象，然后才能对其进行操作。因此，从指向结构体的指针访问成员的一种方法如下：

```C++
#include <iostream>

struct Employee
{
    int id{};
    int age{};
    double wage{};
};

int main()
{
    Employee joe{ 1, 34, 65000.0 };

    ++joe.age;
    joe.wage = 68000.0;

    Employee* ptr{ &joe };
    std::cout << (*ptr).id << '\n'; // 虽然不优雅但是有效: 解引用指针, 再进行成员选择

    return 0;
}
```

然而，这有点难看，因为需要将解引用操作括起来，以便它优先于成员选择操作。

为了实现更简洁的语法，C++提供了指针运算符（->）（有时也称为箭头运算符），可以用于从指向对象的指针中选择成员：

```C++
#include <iostream>

struct Employee
{
    int id{};
    int age{};
    double wage{};
};

int main()
{
    Employee joe{ 1, 34, 65000.0 };

    ++joe.age;
    joe.wage = 68000.0;

    Employee* ptr{ &joe };
    std::cout << ptr->id << '\n'; // 推荐: 使用 -> 从对象的指针中进行成员选择

    return 0;
}
```

指针运算符（->）进行成员选择与成员选择运算符（.）的工作方式相同，但在选择成员之前对指针执行隐式解引用。因此，ptr->id相当于(*ptr).id。

这个箭头操作符不仅更容易输入，而且更不容易出错，因为解引用是隐式完成的，因此不需要担心优先级问题。因此，当通过指针进行成员访问时，应始终使用->运算符。

{{< alert success >}}
**最佳实践**

使用指针访问成员的值时，请使用指针操作符（->），而不是成员选择操作符（.）。

{{< /alert >}}

***
## 混合使用指针与非指针

成员选择运算符始终应用于当前选定的变量。如果混合使用了指针与非指针，则每一步都应该正确使用成员选择方式：

```C++
#include <iostream>
#include <string>

struct Paw
{
    int claws{};
};
 
struct Animal
{
    std::string name{};
    Paw paw{};
};
 
int main()
{
    Animal puma{ "Puma", { 5 } };
 
    Animal* ptr{ &puma };
 
    // ptr 是指针, 使用 ->
    // paw 不是指针, 使用 .

    std::cout << (ptr->paw).claws << '\n';
 
    return 0;
}
```

注意，(ptr->paw).claws中，括号是不必要的，因为 操作符-> 和 操作符. 都是按从左到右的顺序进行计算，但它确实稍微有助于可读性。

***