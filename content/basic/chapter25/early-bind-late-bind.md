---
title: "静态绑定和动态绑定"
date: 2024-11-04T13:14:53+08:00
---

在这一课和下一课中，我们将更深入地了解虚函数是如何实现的。虽然这些信息对于有效使用虚拟函数并不是严格必要的，但它很有趣。您可以将这两节视为可选阅读。

执行C++程序时，它从main()的顶部开始按顺序执行。当遇到函数调用时，执行点跳到被调用函数的开头。CPU如何知道这样做？

编译程序时，编译器会将C++程序中的每个语句转换为一行或多行机器语言。机器语言的每一行都被赋予自己唯一的序列地址。对于函数来说，这没有什么不同——当遇到函数时，它被转换为机器语言，并给出可用的地址。因此，每个函数最终都有一个唯一的地址。

***
## 绑定和分派

我们的程序包含许多名称（标识符、关键字等）。每个名称都有一组相关的属性：例如，如果名称表示变量，则该变量具有类型、值、内存地址等。

例如，当我们说"int x"时，我们告诉编译器将名称x与类型int相关联。稍后，如果我们说"x = 5"，则编译器可以使用此关联来类型检查赋值，以确保它有效。

在一般编程中，绑定是将名称与此类属性相关联的过程。函数绑定（或方法绑定，bind）是确定与函数调用关联的函数定义的过程。实际调用绑定函数的过程称为分派（dispatch）。

在C++中，术语绑定的使用更随意（而分派通常被认为是绑定的一部分）。我们将探索下面这些术语的C++用法。

绑定是一个有多重含义术语。在其他上下文中，绑定可以指：
1. 将引用与对象绑定
2. std::bind
3. 语言绑定

## 静态绑定

编译器遇到的大多数函数调用都是直接函数调用。例如：

```C++
#include <iostream>

struct Foo
{
    void printValue(int value)
    {
        std::cout << value;
    }
};

void printValue(int value)
{
    std::cout << value;
}

int main()
{
    printValue(5);   // 直接函数调用 printValue(int)

    Foo f{};
    f.printValue(5); // 直接函数调用 Foo::printValue(int)
    return 0;
}
```

在C++中，当直接调用非成员函数或非虚成员函数时，编译器可以确定哪个函数定义应与调用匹配。这称为静态绑定或早期绑定，因为它可以在编译时执行。然后，编译器（或链接器）可以生成机器语言指令，告诉CPU直接跳到函数的地址。

对重载函数和函数模板的调用也可以在编译时解析：

```C++
#include <iostream>

template <typename T>
void printValue(T value)
{
    std::cout << value << '\n';
}

void printValue(double value)
{
    std::cout << value << '\n';
}

void printValue(int value)
{
    std::cout << value << '\n';
}

int main()
{
    printValue(5);   // 直接函数调用 printValue(int)
    printValue<>(5); // 直接函数调用 printValue<int>(int)

    return 0;
}
```

让我们来看一个使用静态的简单计算器程序：

```C++
#include <iostream>

int add(int x, int y)
{
    return x + y;
}

int subtract(int x, int y)
{
    return x - y;
}

int multiply(int x, int y)
{
    return x * y;
}

int main()
{
    int x{};
    std::cout << "Enter a number: ";
    std::cin >> x;

    int y{};
    std::cout << "Enter another number: ";
    std::cin >> y;

    int op{};
    std::cout << "Enter an operation (0=add, 1=subtract, 2=multiply): ";
    std::cin >> op;

    int result {};
    switch (op)
    {
        // 使用静态绑定，调用对应的函数
        case 0: result = add(x, y); break;
        case 1: result = subtract(x, y); break;
        case 2: result = multiply(x, y); break;
        default:
            std::cout << "Invalid operator\n";
            return 1;
    }

    std::cout << "The answer is: " << result << '\n';

    return 0;
}
```

由于add()、subtract()和multiply()都是对非成员函数的直接函数调用，因此编译器将在编译时将这些函数调用与其各自的函数定义相匹配。

注意，由于switch语句，直到运行时才确定实际调用的函数。然而，这是一个执行路径问题，而不是绑定问题。

## 动态绑定

在某些情况下，函数调用直到运行时才能解析。在C++中，这被称为动态绑定（或者延时绑定）。

在一般编程术语中，术语“延时绑定”通常意味着被调用的函数不能仅基于静态类型信息来确定，而必须使用动态类型信息来解析。

在C++中，该术语的使用倾向于更松散地表示，编译器或链接器在实际进行函数调用的点，不知道所调用的实际函数实际对应哪个具体的函数。

在C++中，获得动态绑定的一种方法是使用函数指针。简单地回顾函数指针，函数指针是一种指向函数而不是变量的指针。可以通过使用函数名加「运算符()」来调用。

例如，下面的代码通过函数指针调用printValue()函数：

```C++
#include <iostream>

void printValue(int value)
{
    std::cout << value << '\n';
}

int main()
{
    auto fcn { printValue }; // 创建函数指针，并指向 printValue
    fcn(5);                  // 通过函数指针，间接的调用 printValue

    return 0;
}
```

通过函数指针调用函数也称为间接函数调用。在实际调用fcn(5)的点上，编译器在编译时不知道正在调用什么函数。相反，在运行时，对函数指针所持有的地址中，存在的函数进行间接函数调用。

下面的计算器程序在功能上与上面的计算器示例相同，只是它使用函数指针而不是直接函数调用：

```C++
#include <iostream>

int add(int x, int y)
{
    return x + y;
}

int subtract(int x, int y)
{
    return x - y;
}

int multiply(int x, int y)
{
    return x * y;
}

int main()
{
    int x{};
    std::cout << "Enter a number: ";
    std::cin >> x;

    int y{};
    std::cout << "Enter another number: ";
    std::cin >> y;

    int op{};
    std::cout << "Enter an operation (0=add, 1=subtract, 2=multiply): ";
    std::cin >> op;

    using FcnPtr = int (*)(int, int); // 给 丑陋的类型 一个别名
    FcnPtr fcn { nullptr }; // 创建函数指针, 设置为 nullptr

    // 按找用户选择，将 fcn 设置为对应的函数
    switch (op)
    {
        case 0: fcn = add; break;
        case 1: fcn = subtract; break;
        case 2: fcn = multiply; break;
        default:
            std::cout << "Invalid operator\n";
            return 1;
    }

    // 调用 fcn 对应的函数
    std::cout << "The answer is: " << fcn(x, y) << '\n';

    return 0;
}
```

在这个例子中，我们没有直接调用add()、subtract()或multiply()函数，而是将fcn指向希望调用的函数。然后通过指针调用函数。

编译器无法使用静态绑定来解析函数调用fcn(x，y)，因为它无法确定在编译时fcn将指向哪个函数！

动态绑定的效率稍低，因为它涉及额外的间接使用。通过静态绑定，CPU可以直接跳到函数的地址。对于动态绑定，程序必须读取指针中保存的地址，然后跳到该地址。这涉及一个额外的步骤，使其稍微慢一些。然而，动态绑定的优点是它比静态绑定更灵活，因为在运行时才需要决定调用什么函数。

在下一课中，我们将了解如何使用动态绑定来实现虚拟函数。

***