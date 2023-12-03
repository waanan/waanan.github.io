---
title: "std::string简介"
date: 2023-11-28T13:19:42+08:00
---

在之前，我们介绍了C样式的字符串:

```C++
#include <iostream>
 
int main()
{
    std::cout << "Hello, world!"; // "Hello world!" 是C样式的字符串.
    return 0;
}
```

虽然C样式字符串文本很好使用，但C样式字符串变量的行为很奇怪，很难使用（例如，不能使用赋值来为C样式的字符串变量分配新值），并且很危险（例如，如果将较大的C样式字符串复制到分配给较短C样式字符串的空间中，将导致未定义的行为）。在现代C++中，最好避免使用C样式的字符串变量。

幸运的是，C++在语言中引入了两种额外的字符串类型，使用它们更容易、更安全:std::string和std::string_view（C++17）。尽管std::string和std::string_view不是基本类型，但它们非常简单，非常有用，将在这里介绍它们。

***
## 引入std::string

在C++中处理字符串和字符串对象的最简单方法是通过std::string类型，它位于<string>头文件中。

我们可以像创建其他对象一样创建std::string类型的对象:

```C++
#include <string> // 引入 std::string

int main()
{
    std::string name {}; // 空 string

    return 0;
}
```

就像普通变量一样，您可以初始化或分配值给std::string对象:

```C++
#include <string>

int main()
{
    std::string name { "Fly" }; // 初始化变量 name，值为 "Fly"
    name = "John";               // 赋值"John"给变量 name  

    return 0;
}
```

请注意，字符串也可以由数字字符组成:

```C++
std::string myID{ "45" }; // "45" 与数字 45不同!
```

在字符串形式中，数字被视为文本，而不是数字，因此它们不能作为数字进行操作（例如，不能将它们相乘）。C++不会自动将字符串转换为整型或浮点值，反之亦然（尽管有一些方法可以这样做，我们将在以后的课程中介绍）。

***
## std::cout输出字符串

使用std::cout，可以按预期输出std::string对象

```C++
#include <iostream>
#include <string>

int main()
{
    std::string name { "Fly" };
    std::cout << "My name is: " << name << '\n';

    return 0;
}
```

这将打印:

```C++
My name is: Fly
```

空字符串将不打印任何内容:

```C++
#include <iostream>
#include <string>

int main()
{
    std::string empty{ };
    std::cout << '[' << empty << ']';

    return 0;
}
```

打印:

```C++
[]
```

***
## std::string可以处理不同长度的字符串

大多数类型都有分配给它们的固定字节数。例如，如果系统上的int是4个字节，则每个int对象都将使用4个字节的内存。如果你想保存一个需要4个字节以上的整数值……那么，你必须使用其他类型。

string可以做的最整洁的事情之一是保存不同大小的字符串:

```C++
#include <iostream>
#include <string>

int main()
{
    std::string name { "Fly" }; // 初始化变量 name，值为 "Fly"
    std::cout << name << '\n';

    name = "Jason";              // 将 name 更改成更长的字符串
    std::cout << name << '\n';

    name = "Jay";                // 将 name 更改成更短的字符串
    std::cout << name << '\n';

    return 0;
}
```

这将打印:

```C++
Fly
Jason
Jay
```

在上面的示例中，名称用字符串 "Fly" 初始化，该字符串包含四个字符（三个显式字符和一个空终止符）。然后，我们将name设置为较大的字符串，然后设置为较小的字符串。std::string在处理时没有问题！

这是std::string强大的原因之一。

***
## std::cin获取字符串输入

将std::string与std::cin一起使用可能会产生一些意外！考虑以下示例:

```C++
#include <iostream>
#include <string>

int main()
{
    std::cout << "Enter your full name: ";
    std::string name{};
    std::cin >> name; // 可能不一定按预期工作，因为std::cin读取到 空白字符，就会停止

    std::cout << "Enter your favorite color: ";
    std::string color{};
    std::cin >> color;

    std::cout << "Your name is " << name << " and your favorite color is " << color << '\n';

    return 0;
}
```

下面是此程序的示例运行结果:

```C++
Enter your full name: John Doe
Enter your favorite color: Your name is John and your favorite color is Doe
```

发生了什么事？结果是，当使用 操作符>> 从std::cin中提取字符串时，操作符>> 仅返回其遇到的第一个空格之前的字符。任何其他字符都留在std::cin中，等待下一次提取。

所以，当我们使用 操作符>> 将输入提取到变量名中时，只提取了“John”，将“Doe”留在std::cin中。然后，当我们使用 操作符>> 提取输入到color变量时，它提取了“Doe”，而不是等待我们输入。然后程序结束。

***
## 使用std::getline()获取输入文本

要将整行输入读取到字符串中，最好改用std::getline() 函数。getline() 需要两个参数:第一个是std::cin，第二个是字符串变量。

下面是使用std::getline() 的与上面相同的程序:

```C++
#include <iostream>
#include <string> // 引入 std::string 和 std::getline

int main()
{
    std::cout << "Enter your full name: ";
    std::string name{};
    std::getline(std::cin >> std::ws, name); // 将一整行输入读取到 name

    std::cout << "Enter your favorite color: ";
    std::string color{};
    std::getline(std::cin >> std::ws, color); // 将一整行输入读取到 color

    std::cout << "Your name is " << name << " and your favorite color is " << color << '\n';

    return 0;
}
```

现在，我们的程序如预期般工作:

```C++
Enter your full name: John Doe
Enter your favorite color: blue
Your name is John Doe and your favorite color is blue
```

***
## 什么是std::ws？

在——浮点数相关课程中，我们讨论了输出操纵器，它允许我们改变输出的显示方式。在那一课中，我们使用输出操纵器函数std::setprecision() 来更改std::cout显示的精度位数。

C++还支持输入操纵器，它改变了接受输入的方式。std::ws输入操纵器告诉std::cin在提取之前忽略任何前导空格。前导空格是出现在字符串开头的任何空格字符（空格、制表符、换行符）。

探索一下为什么这是有用的。考虑以下程序:

```C++
#include <iostream>
#include <string>

int main()
{
    std::cout << "Pick 1 or 2: ";
    int choice{};
    std::cin >> choice;

    std::cout << "Now enter your name: ";
    std::string name{};
    std::getline(std::cin, name); // 注: 没有 std::ws

    std::cout << "Hello, " << name << ", you picked " << choice << '\n';

    return 0;
}
```

下面是该程序的一些输出:

```C++
Pick 1 or 2: 2
Now enter your name: Hello, , you picked 2
```

这个程序首先要求您输入1或2。到目前为止一切都很好。然后它会要求您输入您的姓名。然而，它实际上不会等待您输入您的姓名！相反，它打印“Hello”字符串，然后退出。

使用 运算符>> 获取输入值时，std::cin不仅捕获该值，还捕获当您按enter键时出现的换行符（“\n”）。因此，当我们键入2然后单击enter时，std::cin将捕获字符串“2\n”作为输入。然后，它将值2提取为变量choice，将换行符留待以后使用。然后，当std::getline() 获取输入到 name中时，它看到“\n”已经在std::cin中等待，并且认为我们输入的是一个空字符串！

我们可以修改上面的程序，以使用std::ws输入操纵器，告诉std::getline() 忽略任何前导空格字符:

```C++
#include <iostream>
#include <string>

int main()
{
    std::cout << "Pick 1 or 2: ";
    int choice{};
    std::cin >> choice;

    std::cout << "Now enter your name: ";
    std::string name{};
    std::getline(std::cin >> std::ws, name); // 注: 添加 std::ws

    std::cout << "Hello, " << name << ", you picked " << choice << '\n';

    return 0;
}
```

现在，该程序将按预期运行。

```C++
Pick 1 or 2: 2
Now enter your name: Alex
Hello, Alex, you picked 2
```

{{< alert success >}}
**最佳实践**

如果使用std::getline() 读取字符串，请使用std::cin >> std::ws 输入操纵器忽略前导空格。这需要为每个std::getline() 调用添加，因为在新的调用不会保留std::ws。

{{< /alert >}}

{{< alert success >}}
**关键点**

将提取运算符（>>）与 std::cin 一起使用会忽略前导空格。std::getline() 不会忽略前导空格，除非使用输入操纵器std::ws。当遇到换行时，它停止提取。

{{< /alert >}}

***
## std::string的长度

如果我们想知道一个std::string中有多少个字符，我们可以询问一个std::string对象的长度。这样做的语法与您以前看到的不同，但非常简单:

```C++
#include <iostream>
#include <string>

int main()
{
    std::string name{ "Alex" };
    std::cout << name << " has " << name.length() << " characters\n";

    return 0;
}
```

这将打印:

```C++
Alex has 4 characters
```

尽管std::string需要以null结尾（从C++11开始），但std::string的返回长度不包括隐式null终止字符。

请注意，不是 length(name) ，而是 name.length()。length() 函数不是普通的独立函数——它是一种特殊类型的函数，嵌套在std::string中，称为成员函数。由于length() 成员函数是在std::string内部声明的，因此在文档中它有时被写做std::string::length()。

之后我们将更详细地介绍成员函数，包括如何编写自己的成员函数。

还要注意，std::string::length() 返回无符号整数值（很可能是size_t类型）。如果要将长度分配给int变量，则应将其static_cast，以避免编译器对有符号/无符号转换发出警告:

```C++
int length { static_cast<int>(name.length()) };
```

在C++20中，您还可以使用std::ssize() 函数来获取std::string的长度作为有符号整数值:

```C++
#include <iostream>
#include <string>

int main()
{
    std::string name{ "Alex" };
    std::cout << name << " has " << std::ssize(name) << " characters\n";

    return 0;
}
```

{{< alert success >}}
**关键点**

对于普通函数，我们调用function(object)。对于成员函数，我们调用object.function() 。

{{< /alert >}}

***
## 初始化std::string的开销很大

每当初始化std::string时，都会生成用于初始化它的字符串的副本。复制字符串的成本很高，因此应注意将复制的数量降至最低。

***
## 不按值传递std::string

当通过值将std::string传递给函数时，必须实例化std::string函数参数，并使用参数进行初始化。这将导致昂贵的拷贝。我们将在——std::string_view简介中讨论如何做（使用std:∶string_view）。

{{< alert success >}}
**最佳实践**

不要按值传递std::string，因为它会生成昂贵的副本。

{{< /alert >}}

{{< alert success >}}
**提示**

在大多数情况下，请改用std::string_view参数（在——std:∶string_view简介中介绍）。

{{< /alert >}}

***
## 返回std::string

当函数按值返回给调用者时，返回值通常从函数复制回调用者。因此，您可能希望不应该按值返回std::string，因为这样做将返回std::string的昂贵副本。

然而，根据经验法则，当return语句的表达式解析为以下任一项时，可以按值返回std::string:

1. 类型为std::string的局部变量。
2. 由函数调用或运算符的值返回的std::string。
3. 作为return语句的一部分创建的std::string。


在大多数其他情况下，不要按值返回std::string，因为这样做将产生昂贵的副本。

{{< alert success >}}
**对于高级读者**

string支持一种称为move语义的功能，它允许在函数结束时本应销毁的对象由值返回，而不进行复制。移动语义如何工作超出了这篇文章的范围，我们将在后续介绍。

{{< /alert >}}

{{< alert success >}}
**提示**

如果返回C样式字符串文本，请改用std::string_view返回类型。

{{< /alert >}}

{{< alert success >}}
**对于高级读者**

std::string也可以由（const）引用返回，这是另一种避免复制的方法。我们在后续进行介绍。

{{< /alert >}}

***
## std::string的字面值

双引号字符串（如"Hello，world！"）默认为C样式的字符串（因此，具有奇怪的类型）。

我们可以通过在双引号字符串后面使用s后缀来创建类型为std::string的字符串字面值。

```C++
#include <iostream>
#include <string> // for std::string

int main()
{
    using namespace std::string_literals; // 可以让我们方便的使用 s 后缀

    std::cout << "foo\n";   // C-style 字符串字面值
    std::cout << "goo\n"s;  // s 后缀意味着 std::string 字面值

    return 0;
}
```

您可能不需要经常使用std::string字面值（因为用C样式的字符串初始化std::string对象是可以的），但我们将在以后的课程中看到一些情况（涉及类型推导），其中使用std::string而不是C样式字符串的使事情变得更容易。

{{< alert success >}}
**提示**

“s”后缀位于命名空间std::literals::string_literals中。

引入字面值后缀的最简洁的方法是使用 using namespace std::literals。然而，这会将所有标准库字面值后缀导入，这会带来一大堆您可能不会使用的东西。

我们建议使用 using namespace std::string_literals，它仅导入std::string的字面值后缀。

我们在后续讨论using指令。这是一种例外情况，使用整个名称空间通常是可以的，因为定义的字面值后缀不太可能与您的任何代码冲突。在头文件中，避免函数之外的using指令。

{{< /alert >}}

{{< alert success >}}
**对于高级读者**

"Hello"s解析为std::string{"Hello"，6}，它创建一个用C样式的字符串"Hello"（长度为6，包含隐式null终止符）初始化的临时std::string。

{{< /alert >}}

***
## constexpr字符串

如果尝试定义constexpr std::string，编译器可能会生成错误:

```C++
#include <iostream>
#include <string>

int main()
{
    using namespace std::string_literals;

    constexpr std::string name{ "Alex"s }; // 编译失败

    std::cout << "My name is: " << name;

    return 0;
}
```

发生这种情况是因为在C++17或更早版本中根本不支持constexpr std::string，并且在C++20/23中仅在非常有限的情况下支持。如果需要constexpr字符串，请改用std::string_view。

***
## 结论

string很复杂，利用了许多我们尚未介绍的语言功能。幸运的是，您不需要理解这些复杂性，就可以将std::string用于简单的任务，如基本的字符串输入和输出。我们鼓励您现在就开始尝试字符串，稍后我们将介绍其他字符串功能。

***
