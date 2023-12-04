---
title: "std::string_view简介"
date: 2023-11-28T13:19:42+08:00
---

考虑以下程序:

```C++
#include <iostream>

int main()
{
    int x { 5 }; // x 拷贝了一下初始值5
    std::cout << x << '\n';

    return 0;
}
```

当执行x的定义时，初始化值5被复制到为变量 int x 分配的内存中。对于基本类型，初始化和复制变量是快速的。

现在考虑一下类似的程序:

```C++
#include <iostream>
#include <string>

int main()
{
    std::string s{ "Hello, world!" }; // s 拷贝了初始值
    std::cout << s << '\n';

    return 0;
}
```

初始化s时，C样式字符串文本“Hello，world！”将复制到为std::string s分配的内存中。与基本类型不同，初始化和复制std::string的速度很慢。

在上面的程序中，我们对s所做的一切就是将值打印到控制台，然后销毁s。我们制作了一个“Hello，world！”的副本，只是为了打印然后销毁该副本。这是低效的。

我们在这个例子中看到类似的东西:

```C++
#include <iostream>
#include <string>

void printString(std::string str) // str 拷贝了实际传入的参数
{
    std::cout << str << '\n';
}

int main()
{
    std::string s{ "Hello, world!" }; // s 拷贝了初始值
    printString(s);

    return 0;
}
```

这个例子制作了C样式字符串“Hello，world！”的两个副本:一个是在main() 中初始化s时，另一个是当在printString() 中初始参数str时。仅仅为了打印字符串而进行大量不必要的复制！

***
## std::string_view C++17

为了解决std::string初始化（或复制）开销大的问题，C++17引入了std::string_view（位于<string_view>头文件中）。std::string_view提供对现有字符串（C样式字符串、std::string或另一个std::string_view）的只读访问，而不制作副本。只读意味着我们可以访问和使用正在查看的值，但不能修改它。

下面的示例与前面的示例相同，只是我们用std::string_view替换了std::string。

```C++
#include <iostream>
#include <string_view>

// str 提供了传入参数的只读访问能力
void printSV(std::string_view str) // str现在是 std::string_view
{
    std::cout << str << '\n';
}

int main()
{
    std::string_view s{ "Hello, world!" }; // s现在是 std::string_view
    printSV(s);

    return 0;
}
```

该程序产生与前一个程序相同的输出，但没有生成字符串“Hello，world！”的副本。

当我们用C样式的字符串文本“Hello，world！”初始化std::string_views时，s提供对“HelloWorld！”的只读访问，而不制作字符串的副本。当我们将s传递给printSV() 时，参数str从s初始化。这允许我们再次通过str访问“Hello，world！”，而无需复制字符串。

{{< alert success >}}
**最佳实践**

当您需要只读字符串时，特别是对于函数参数，请首选std::string_view而不是std::string。

{{< /alert >}}

***
## 可以用许多不同类型的字符串初始化std::string_view

关于std::string_view的一个好处是它非常灵活。可以使用C样式的字符串、std::string或另一个std::string_view进行初始化

```C++
#include <iostream>
#include <string>
#include <string_view>

int main()
{
    std::string_view s1 { "Hello, world!" }; // 使用c样式字符串初始化
    std::cout << s1 << '\n';

    std::string s{ "Hello, world!" };
    std::string_view s2 { s };  // 使用 std::string 初始化
    std::cout << s2 << '\n';

    std::string_view s3 { s2 }; // 使用 std::string_view 初始化
    std::cout << s3 << '\n';
       
    return 0;
}
```

***
## std::string_view作为函数参数将接受许多不同类型的字符串参数

C样式的字符串和std::string都可以隐式转换为std::string_view。因此，std::string_view作为函数参数将接受类型为C-样式字符串、std::string或std::string_view的参数

```C++
#include <iostream>
#include <string>
#include <string_view>

void printSV(std::string_view str)
{
    std::cout << str << '\n';
}

int main()
{
    printSV("Hello, world!"); // 使用c样式字符串调用

    std::string s2{ "Hello, world!" };
    printSV(s2); // 使用 std::string 调用

    std::string_view s3 { s2 };
    printSV(s3); // 使用 std::string_view 调用
       
    return 0;
}
```

***
## std::string_view不会隐式转换为std::string

由于std::string复制了其初始值设定项（这很昂贵），C++不允许将std::string_view隐式转换为std::string。这是为了防止意外地将std::string_view参数传递到std::string参数，并防止意外地制作昂贵的副本，而其实可能不需要这样的副本。

如果需要，我们有两个选项:

1. 显示的创建一个std::string，用std::string_view初始化。
2. 使用static_cast做转换

以下示例显示了这两个选项:

```C++
#include <iostream>
#include <string>
#include <string_view>

void printString(std::string str)
{
	std::cout << str << '\n';
}

int main()
{
	std::string_view sv{ "Hello, world!" };

	// printString(sv);   // 会编译失败: 不能隐式的将 std::string_view 转换为 std::string

	std::string s{ sv }; // okay: 可以使用 std::string_view 来初始化 std::string 
	printString(s);      // 然后使用 std::string 来做函数调用

	printString(static_cast<std::string>(sv)); // okay: 可以做显示转换

	return 0;
}
```

***
## 更改std::string_view

将新字符串分配给std::string_view会导致std::string_view替换成新的字符串。单不会以任何方式修改先前的字符串。

下面的示例对此进行了说明:

```C++
#include <iostream>
#include <string>
#include <string_view>

int main()
{
    std::string name { "Alex" };
    std::string_view sv { name }; // sv 现在view的是 name
    std::cout << sv << '\n'; // 打印 Alex

    sv = "John"; // sv 现在 view "John" (不会更改 name 变量)
    std::cout << sv << '\n'; // 打印 John

    std::cout << name << '\n'; // 打印 Alex

    return 0;
}
```

在上面的示例中，sv = "John" 使sv现在view字符串"John"。它不会更改name变量持有的值（仍然是“Alex”）。

***
## std::string_view的字面值常量

默认情况下，双引号字符串是C样式的字符串。我们可以通过在双引号字符串之后使用sv后缀来创建类型为std::string_view的字符串字面值。

```C++
#include <iostream>
#include <string>      // for std::string
#include <string_view> // for std::string_view

int main()
{
    using namespace std::string_literals;      // 允许使用 s 后缀
    using namespace std::string_view_literals; // 允许使用 sv 后缀

    std::cout << "foo\n";   // 无后缀， c样式字符串字面值
    std::cout << "goo\n"s;  // s 后缀， std::string 字面值
    std::cout << "moo\n"sv; // sv 后缀， std::string_view 字面值

    return 0;
};
```

***
## constexpr std::string_view

与std::string不同，std::string_view完全支持constexpr:

```C++
#include <iostream>
#include <string_view>

int main()
{
    constexpr std::string_view s{ "Hello, world!" }; // s 是一个字符串常量
    std::cout << s << '\n'; // s 在编译时会被替换为 "Hello, world!"

    return 0;
}
```

这使得constexpr std::string_view 成为需要字符串符号常量时的首选。

我们将在下一课中继续讨论std::string_view。

***
