---
title: "非限定作用域枚举的输入与输出"
date: 2024-03-08T13:20:57+08:00
---

在上一课，提到枚举元素是符号常量。没有告诉你们的是，枚举元素是整型符号常量。因此，枚举类型实际上持有整数值。

这类似于使用char的情况。考虑：

```C++
char ch { 'A' };
```

char实际上只是一个1字节的整数值，字符'A'被转换为整数值（在本例中为65）并存储。

定义枚举时，每个枚举元素都会根据其在枚举列表中的位置自动分配一个整数值。默认情况下，为第一个枚举元素分配整数值0，并且每个后续枚举元素的值都比前一个大一：

```C++
enum Color
{
    black, // 值为 0
    red, // 1
    blue, // 2
    green, // 3
    white, // 4
    cyan, // 5
    yellow, // 6
    magenta, // 7
};

int main()
{
    Color shirt{ blue }; // shirt 实际存储了整数值 2

    return 0;
}
```

可以显式定义枚举元素的值。这些整数值可以是正值或负值，并且可以与其他枚举元素共享相同的值。任何未定义的枚举元素都被赋予比前一个大一的值。

```C++
enum Animal
{
    cat = -3,
    dog,         // 值为 -2
    pig,         // -1
    horse = 5,
    giraffe = 5, // 与 horse 存储相同的值
    chicken,      // 6 
};
```

注意，在这种情况下，horse和giraffe被赋予了相同的值。当这种情况发生时，枚举元素变得无法区分——本质上，horse和giraffe使用时可以互换了。尽管C++允许，但通常应避免将相同的值分配给同一枚举中的两个枚举元素。

{{< alert success >}}
**最佳实践**

避免将显式值分配给枚举元素，除非有令人信服的理由这样做。

{{< /alert >}}

***
## 非限定作用域枚举将隐式转换为整数值

考虑以下程序：

```C++
#include <iostream>

enum Color
{
    black, // 0
    red, // 1
    blue, // 2
    green, // 3
    white, // 4
    cyan, // 5
    yellow, // 6
    magenta, // 7
};

int main()
{
    Color shirt{ blue };

    std::cout << "Your shirt is " << shirt << '\n'; // 这一行的效果是?

    return 0;
}
```

由于枚举类型保存整数值，因此正如您所期望的那样，这会打印：

```C++
Your shirt is 2
```

在函数调用中或与运算符一起使用枚举类型时，编译器将首先尝试查找与枚举类型匹配的函数或运算符。例如，当编译器尝试编译 std::cout << shirt 时，编译器将首先查看 操作符<< 是否知道如何将Color类型的对象（因为shirt的类型是Color）打印到std::cout。这里无法找到。

如果编译器找不到匹配项，则编译器将隐式地将枚举元素转换为其相应的整数值。因为std::cout可以打印整数值，所以shirt中的值被转换为整数并打印为整数值2。

***
## 打印枚举元素名称

在大多数情况下，将枚举打印为整数值（如2）不是我们想要的。相反，通常希望打印枚举元素表示的名称（blue）。但要做到这一点，需要某种方法将枚举（2）的整数值转换为与枚举元素名称（“blue”）匹配的字符串。

在C++20中，C++没有任何简单的方法来实现这一点，因此必须自己实现解决方案。幸运的是，这并不困难。典型方法是编写一个函数，该函数将枚举类型作为参数，然后输出相应的字符串（或将字符串返回给调用方）。

```C++
// 这里使用if else，运行效率不高
void printColor(Color color)
{
    if (color == black) std::cout << "black";
    else if (color == red) std::cout << "red";
    else if (color == blue) std::cout << "blue";
    else std::cout << "???";
}
```

然而，为此使用一系列if-else语句是低效的，因为它需要在找到匹配之前进行多次比较。执行相同操作的更有效的方法是使用switch语句。在下面的示例中，将Color转换为std::string返回，以使调用方能够更灵活地对名称执行任何操作（包括打印它）：

```C++
#include <iostream>
#include <string>

enum Color
{
    black,
    red,
    blue,
};


std::string getColor(Color color)
{
    switch (color)
    {
    case black: return "black";
    case red:   return "red";
    case blue:  return "blue";
    default:    return "???";
    }
}

int main()
{
    Color shirt { blue };

    std::cout << "Your shirt is " << getColor(shirt) << '\n';

    return 0;
}
```

这将打印：

```C++
Your shirt is blue
```

这比if-else链执行得更好（switch语句往往比if-else链更有效），并且也更容易阅读。然而，这个版本仍然效率低下，因为需要在每次调用函数时创建并返回std::string（这很昂贵）。

在C++17中，一个更有效的选项是用std::string_view替换std::string。string_view允许以一种复制成本低得多的方式返回字符串文本。

```C++
#include <iostream>
#include <string_view> // C++17

enum Color
{
    black,
    red,
    blue,
};

constexpr std::string_view getColor(Color color) // C++17
{
    switch (color)
    {
    case black: return "black";
    case red:   return "red";
    case blue:  return "blue";
    default:    return "???";
    }
}

int main()
{
    constexpr Color shirt{ blue };

    std::cout << "Your shirt is " << getColor(shirt) << '\n';

    return 0;
}
```

***
## 设定运算符<<以打印枚举数

尽管上面的示例运行良好，但我们仍然必须记住创建的函数名称，以获得枚举元素名称。虽然这通常不是太繁琐，但如果有许多枚举，则可能会变得麻烦。使用操作符重载（类似于函数重载的功能），实际上可以设定操作符<<如何打印程序定义的枚举！我们还没有解释这是如何工作的，所以现在它有点神奇：

```C++
#include <iostream>

enum Color
{
	black,
	red,
	blue,
};

// 设定 operator<< 如何打印 Color
// 现在可能看起来有点神奇，后续进行介绍
// std::ostream 是 std::cout 的类型
// 返回值与参数都是引用 (避免制作副本)!
std::ostream& operator<<(std::ostream& out, Color color)
{
	switch (color)
	{
	case black: return out << "black";
	case red:   return out << "red";
	case blue:  return out << "blue";
	default:    return out << "???";
	}
}

int main()
{
	Color shirt{ blue };
	std::cout << "Your shirt is " << shirt << '\n'; // it works!

	return 0;
}
```

这将打印：

```C++
Your shirt is blue
```

我们在后续讨论I/O操作符的重载。现在，您可以复制此代码并将Color替换为自己的枚举类型。

{{< alert success >}}
**对于高级读者**

这里简要介绍上面代码的作用。当尝试使用std::cout和 运算符<< 打印shirt时，编译器将看到我们重载了 运算符<< 来处理Color类型的对象。然后使用std::cout作为out参数，使用shirt作为参数color来调用该重载 操作符<< 对应的函数。由于out是对std::cout的引用，因此像 out << "blue" 这样的语句实际上只是将"blue"打印到std::cout。

{{< /alert >}}

***
## 枚举大小和底层类型

枚举元素是整型常量。用于表示枚举数的特定整型类型称为其底层类型。

对于非限定作用域枚举，C++标准没有指定应将哪个特定的整型用作底层类型。大多数编译器将使用类型int作为底层类型（这意味着非限定作用域枚举将与int大小相同），除非需要更大的类型来存储枚举元素值。

可以指定不同的底层类型。例如，如果您在某些带宽敏感的环境中工作（例如，通过网络发送数据），则可能需要指定较小的类型：

```C++
#include <cstdint>  // for std::int8_t
#include <iostream>

// 使用 8-bit 整数作为 Color 的底层类型
enum Color : std::int8_t
{
    black,
    red,
    blue,
};

int main()
{
    Color c{ black };
    std::cout << sizeof(c) << '\n'; // 打印 1 (字节)

    return 0;
}
```

{{< alert success >}}
**最佳实践**

仅在必要时指定枚举的底层类型。

{{< /alert >}}

{{< alert success >}}
**警告**

由于std::int8_t和std::uint8_t通常是char类型的类型别名，因此使用这两种类型之一作为枚举底层类型很可能会导致枚举元素打印为char值，而不是int值。

{{< /alert >}}

***
## 整数到非限定作用域枚举转换

虽然编译器将隐式地将非限定作用域枚举转换为整数，但它不会隐式地把整数转换为非限定作用域枚举。以下操作将产生编译器错误：

```C++
enum Pet // 未指定底层类型
{
    cat, // 0
    dog, // 1
    pig, // 2
    whale, // 3
};

int main()
{
    Pet pet { 2 }; // 编译错误: 整数 2 不能隐式的转换为 Pet
    pet = 3;       // 编译错误: 整数 3 不能隐式的转换为 Pet

    return 0;
}
```

有两种方法可以解决这个问题。

首先，可以使用static_cast强制编译器将整数转换为枚举元素：

```C++
enum Pet // 未指定底层类型
{
    cat, // 0
    dog, // 1
    pig, // 2
    whale, // 3
};

int main()
{
    Pet pet { static_cast<Pet>(2) }; // 将整数 2 转换为 Pet
    pet = static_cast<Pet>(3);       // pet 从 pig 变成了 whale!

    return 0;
}
```

稍后我们将看到一个示例，这个功能是有实际用途的。

第二，在C++17中，如果非限定作用域枚举具有指定的底层类型，则编译器将允许您使用整数值来列表初始化非限定作用域枚举：

```C++
enum Pet: int // 指定底层类型
{
    cat, // 0
    dog, // 1
    pig, // 2
    whale, // 3
};

int main()
{
    Pet pet1 { 2 }; // ok: 使用列表初始化
    Pet pet2 (2);   // 编译错误: 不能使用整数做直接初始化
    Pet pet3 = 2;   // 编译错误: 不能使用整数做复制初始化

    pet1 = 3;       // 编译错误: 不能使用整数赋值

    return 0;
}
```

***
## 非限定作用域枚举输入

由于Pet是程序定义的类型，因此C++不知道如何使用std::cin获取Pet：

```C++
#include <iostream>

enum Pet
{
    cat, // 0
    dog, // 1
    pig, // 2
    whale, // 3
};

int main()
{
    Pet pet { pig };
    std::cin >> pet; // 编译失败, std::cin 不知道如何获取Pet

    return 0;
}
```

为了解决这个问题，可以读取整数，并使用static_cast将该整数转换为适当枚举元素：

```C++
#include <iostream>

enum Pet
{
    cat, // 0
    dog, // 1
    pig, // 2
    whale, // 3
};

int main()
{
    std::cout << "Enter a pet (0=cat, 1=dog, 2=pig, 3=whale): ";

    int input{};
    std::cin >> input; // 输入整数

    Pet pet{ static_cast<Pet>(input) }; // static_cast 将整数转换为Pet

    return 0;
}
```

{{< alert success >}}
**对于高级读者**

类似于如何设定 操作符<< 输出枚举类型，还可以设定 操作符>> 如何输入枚举类型：

```C++
#include <iostream>

enum Pet
{
    cat, // 0
    dog, // 1
    pig, // 2
    whale, // 3
};

// 目前可能看起来有些神奇
// 传递引用，以便可以在函数中修改输入
std::istream& operator>> (std::istream& in, Pet& pet)
{
    int input{};
    in >> input; // 读取一个整数

    pet = static_cast<Pet>(input);
    return in;
}

int main()
{
    std::cout << "Enter a pet (0=cat, 1=dog, 2=pig, 3=whale): ";

    Pet pet{};
    std::cin >> pet; // 使用 std::cin 获取输入的 pet

    std::cout << pet << '\n'; // 验证运行正常

    return 0;
}
```

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter13/unscoped-enum/" next="/basic/chapter13/scoped-enum/" >}}
13.1 非限定作用域枚举
<--->
13.3 限定作用域枚举（枚举类）
{{< /prevnext >}}
