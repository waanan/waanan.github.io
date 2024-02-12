---
title: "函数重载决议"
date: 2024-02-10T01:33:43+08:00
---

在上一课中，我们讨论了使用函数的哪些属性来区分重载函数。如果重载函数没有与同名的其他函数正确区分，则编译器将提示编译错误。

然而，拥有一组差异化的重载函数只是实际情况的一半。当进行任何函数调用时，编译器还必须确保可以找到匹配的函数声明。

对于非重载函数（具有唯一名称的函数），只有一个函数可以潜在地匹配函数调用。该函数要么匹配（或者可以在应用类型转换后匹配），要么不匹配（会有编译错误）。对于重载函数，可以有许多函数可能与函数调用匹配。由于函数调用只能解析为其中一个，因此编译器必须确定哪个重载函数是最佳匹配的。将函数调用与特定重载函数匹配的过程称为重载决议。

在调用值和函数参数类型完全匹配的简单情况下，这（通常）很简单：

```C++
#include <iostream>

void print(int x)
{
     std::cout << x << '\n';
}

void print(double d)
{
     std::cout << d << '\n';
}

int main()
{
     print(5); // 5 是 int, 所以匹配 print(int)
     print(6.7); // 6.7 是 double, 所以匹配 print(double)

     return 0;
}
```

但是，如果函数调用值的类型不完全匹配任何重载函数的参数类型，会发生什么情况？例如：

```C++
#include <iostream>

void print(int x)
{
     std::cout << x << '\n';
}

void print(double d)
{
     std::cout << d << '\n';
}

int main()
{
     print('a'); // char 不匹配 int 或 double
     print(5L); // long 不匹配 int 或 double

     return 0;
}
```

这里没有完全匹配并不意味着找不到匹配——毕竟，char或long可以隐式类型转换为int或double。但在每种情况下，哪种转换是最好的呢？

在本课中，我们将探索编译器如何将给定的函数调用与特定的重载函数相匹配。

***
## 函数重载决议

当对重载函数进行函数调用时，编译器逐步执行一系列规则，以确定哪个重载函数（如果有）是最佳匹配的。

在每个步骤中，编译器将一系列不同的类型转换应用于函数调用中的参数。对于应用的每个转换，编译器检查是否有任何重载函数现在是匹配的。在应用了所有不同的类型转换并检查了是否匹配后，步骤完成。结果将是三种可能的结果之一：

1. 找不到匹配的函数。编译器将移动到序列中的下一步。
2. 找到单个匹配函数。该函数被认为是最佳匹配。匹配过程现在已完成，并且不会执行后续步骤。
3. 找到多个匹配函数。编译器将提示匹配错误。我们稍后将进一步讨论这种情形。

如果编译器到达了整个序列的末尾，但未找到匹配项，它将生成一个编译错误，即无法为函数调用找到匹配的重载函数。

***
## 参数匹配序列

步骤1）编译器尝试查找精确匹配。这分两个阶段发生。首先，编译器将查看是否存在重载函数，其中函数调用中的实际数据类型与重载函数中的参数的类型完全匹配。例如：

```C++
void print(int)
{
}

void print(double)
{
}

int main()
{
    print(0); // 精确匹配 print(int)
    print(3.4); // 精确匹配 print(double)

    return 0;
}
```

由于函数调用print(0)中的0是int，编译器将查看是否声明了print(int)这个函数。由于有，编译器确定print(int)是完全匹配的。

其次，编译器将对函数调用中的参数应用许多琐碎的转换（trivial conversions）。这是一组特定的转换规则，它们将修改类型（而不修改值）以查找匹配。例如，非常量类型可以简单地转换为常量类型：

```C++
void print(const int)
{
}

void print(double)
{
}

int main()
{
    int x { 0 };
    print(x); // x 也可以用作 const int

    return 0;
}
```

在上面的例子中，我们调用了print(x) ，其中x是一个int。编译器将把x从int转换为const int，然后与print(const int)匹配。

通过这样的转换进行的匹配被认为是精确匹配。

步骤2）如果找不到精确匹配，编译器将尝试通过对参数应用数值提升来查找匹配。在前面，我们介绍了如何将某些窄整型和浮点型自动提升为更宽的类型，如int或double。如果在数值提升后可以找到匹配，则可以编译成功。

例如：

```C++
void print(int)
{
}

void print(double)
{
}

int main()
{
    print('a'); // 数值提升 匹配 print(int)
    print(true); // 数值提升 匹配 print(int)
    print(4.5f); // 数值提升 匹配 print(double)

    return 0;
}
```

对于print('a')，由于在前面的步骤中找不到print(char)的精确匹配，编译器将char 'a'提升为int，并查找匹配项。这与print(int)匹配，因此函数调用解析为print(int)。

步骤3）如果通过数值提升未找到匹配项，编译器将尝试通过对参数应用数值转换来查找匹配项。

例如：

```C++
#include <string> // for std::string

void print(double)
{
}

void print(std::string)
{
}

int main()
{
    print('a'); // 'a' 被转换以匹配 print(double)

    return 0;
}
```

在这种情况下，由于没有print(char)（精确匹配）和print(int)（提升匹配），因此'a'在数字上转换为double并与print(double)匹配。

{{< alert success >}}
**关键点**

通过应用数值提升进行的匹配优先于通过应用数值转换进行的任何匹配。

{{< /alert >}}

步骤4）如果通过数值转换未找到匹配项，编译器将尝试通过任何用户定义的转换来查找匹配项。尽管我们还没有介绍用户定义的转换，但某些类型（例如class）可以定义到隐式转换到其他类型。这里有一个例子，只是为了说明这一点：

```C++
// 我们还没介绍 class, 所以下面只是演示，看不懂也无需担心
class X // 这里定义了一个新的类型 X
{
public:
    operator int() { return 0; } // 自定义了一个 X 类型到 int 类型的转换
};

void print(int)
{
}

void print(double)
{
}

int main()
{
    X x; // 创建一个类型 X 的变量 x
    print(x); // 通过用户自定义的转换规则，x 可以被转换为 int

    return 0;
}
```

在本例中，编译器将首先检查是否存在与print(X)完全匹配的项。没有对应的定义。接下来，编译器将检查x是否可以进行数值提升，它不能。然后，编译器将检测x是否可以被数值转换，它也不能。最后，编译器将查找任何用户定义的转换。因为我们定义了一个自定义的从X到int的转换，编译器将X转换为int以匹配print(int)。

应用用户定义的转换后，编译器可以应用其他隐式提升或转换来查找匹配项。因此，如果我们的自定义转换是类型char而不是int，编译器就会使用用户定义的转换来转换为char，然后将结果提升为int以进行匹配。

{{< alert success >}}
**对于高级读者**

class的构造函数还充当从其他类型到该类型的用户定义转换，并且可以在该步骤中用于查找匹配的函数。

{{< /alert >}}

步骤5）如果通过用户定义的转换未找到匹配，编译器将查找使用省略号的匹配函数。

步骤6）如果此时仍未找到匹配项，编译器将放弃，并将发出关于无法找到匹配函数的编译报错。

{{< alert success >}}
**相关内容**

我们在后续介绍省略号（以及为什么要避免使用它们）。

{{< /alert >}}

***
## 不明确的匹配

对于非重载函数，每个函数调用要么可以匹配到对应的定义。要么找不到匹配项时，编译器将发出编译错误：

```C++
void foo()
{
}

int main()
{
     foo(); // okay: 可以找到匹配
     goo(); // 编译失败: 无法找到匹配

     return 0;
}
```

对于重载函数，有第三种可能的结果：可能会发现不明确的匹配。当编译器找到两个或多个可以在同一步骤中匹配的函数时，会发生不明确的匹配。发生这种情况时，编译器将停止匹配，并发出编译错误，指出它发现了不明确的函数调用。

由于必须区分每个重载函数才能进行编译，因此您可能想知道函数调用如何可能导致多个匹配。让我们看一个例子来说明这一点：

```C++
void print(int)
{
}

void print(double)
{
}

int main()
{
    print(5L); // 5L 是类型 long

    return 0;
}
```

由于字面值5L是long类型，编译器将首先查看是否可以找到与print(long)完全匹配的项，但它不会找到。接下来，编译器将尝试数值提升，但无法提升long类型的值，因此这里也没有匹配项。

然后，编译器将尝试通过对long参数应用数值转换来查找匹配项。在检查所有数值转换规则的过程中，编译器将找到两个潜在的匹配。如果long参数转换为int，则函数调用将匹配print(int)。如果改为将long参数转换为double，则它将匹配print(double)。由于通过数值转换找到了两个可能的匹配，因此函数调用被认为是不明确的。

在Visual Studio 2019上，这会导致以下错误消息：

```C++
error C2668: 'print': ambiguous call to overloaded function
message : could be 'void print(double)'
message : or       'void print(int)'
message : while trying to match the argument list '(long)'
```

{{< alert success >}}
**关键点**

如果编译器在给定的步骤中找到多个匹配项，则将导致不明确的函数调用。这意味着给定步骤中的任何匹配都不被认为比同一步骤中的其他匹配更好。

{{< /alert >}}

下面是另一个产生不明确匹配的示例：

```C++
void print(unsigned int)
{
}

void print(float)
{
}

int main()
{ 
    print(0); // int 可以被转换为 unsigned int 或 float
    print(3.14159); // double 可以被转换为  unsigned int 或 float

    return 0;
}
```

尽管您可能期望0解析到  print(unsigned int) ，3.14159解析到 print(float)，但这两个调用都会导致不明确的匹配。int值0可以数值转换为unsigned int 或 float，它们重载匹配得同样好，因此这是一个不明确的函数调用。

这同样适用于将double数转换为float或unsigned int。两者都是数值转换，因此重载匹配得同样好，结果也不明确。

***
## 修正不明确的匹配

由于不明确的匹配是编译时错误，因此在程序编译之前，需要消除不明确匹配。有几种方法可以解决不明确的匹配：

1. 通常，最好的方案是新定一个能完全精确匹配的新函数。
2. 或者，显式的将不能明确匹配的参数转换为匹配的类型。例如，如果想让print(0) 匹配 print(unsigned int)，可以这样做：

```C++
int x{ 0 };
print(static_cast<unsigned int>(x)); // 会调用print(unsigned int)
```

3. 如果调用的值，是一个字面值常量。可以添加后缀，确保字面值是能精确匹配的类型。

```C++
print(0u); // 会调用 print(unsigned int) 因为 'u' 后缀代表 unsigned int, 所以现在是精确匹配
```

***
## 匹配具有多个参数的函数

如果有多个参数，编译器依次将匹配规则应用于每个参数。最终所选函数，每个参数至少与所有其他函数匹配的一样好，并且至少一个参数比所有其他函数更好地匹配。换句话说，对于至少一个参数，所选函数必须比所有其他候选函数提供更好的匹配，而对于所有其他参数，不能提供更差的匹配。

在找到这样一个函数的情况下，它显然是最好的选择。如果找不到这样的函数，则该调用将被视为不明确（或不匹配）。

例如：

```C++
#include <iostream>

void print(char, int)
{
	std::cout << 'a' << '\n';
}

void print(char, double)
{
	std::cout << 'b' << '\n';
}

void print(char, float)
{
	std::cout << 'c' << '\n';
}

int main()
{
	print('x', 'a');

	return 0;
}
```

在上面的程序中，所有函数都与第一个参数完全匹配。然而，第一个函数通过数值提升匹配第二个参数，而其他函数需要转换。因此，print(char, int)无疑是最佳匹配。

***

{{< prevnext prev="/basic/chapter11/func-overload-diff/" next="/basic/chapter11/func-del/" >}}
11.1 被重载函数之间互相区分
<--->
11.3 函数的delete说明符
{{< /prevnext >}}
