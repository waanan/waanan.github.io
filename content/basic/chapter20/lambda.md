---
title: "lambda（匿名函数）简介"
date: 2024-08-20T10:49:32+08:00
---

回忆下我们之前是如何使用算法标准库:

```C++
#include <algorithm>
#include <array>
#include <iostream>
#include <string_view>

// 如果匹配nut的话，返回true
bool containsNut(std::string_view str)
{
    // 如果没找到匹配的，std::string_view::find 返回 std::string_view::npos
    // 否则返回对应匹配的下标
    return str.find("nut") != std::string_view::npos;
}

int main()
{
    constexpr std::array<std::string_view, 4> arr{ "apple", "banana", "walnut", "lemon" };

    // 遍历数组，查找包含“nut”的字符串
    auto found{ std::find_if(arr.begin(), arr.end(), containsNut) };

    if (found == arr.end())
    {
        std::cout << "No nuts\n";
    }
    else
    {
        std::cout << "Found " << *found << '\n';
    }

    return 0;
}
```

该代码搜索字符串数组，查找包含子串“nut”的第一个元素。因此，它产生结果:

```C++
Found walnut
```

虽然它有效，但它可以改进。

这里问题的根源是std::find_if要求我们向它传递函数指针。因此，我们被迫定义一个只使用一次的函数，必须给它一个名称，并且必须放在全局作用域内（因为函数不能嵌套！）。函数也很短，从一行代码中几乎可以比从名称和注释中更容易地看出它做了什么。

***
## Lambda匿名函数

lambda表达式（也称为闭包）允许我们在函数中定义匿名函数。嵌套很重要，因为它既允许我们避免名称空间命名污染，又允许我们在尽可能接近函数使用位置的地方定义函数（提供额外的上下文）。

lambda的语法是C++中比较奇怪的东西之一，需要一点时间来适应。lambdas的形式为:

```C++
[ 捕获列表 ] ( 参数列表 ) -> 返回类型
{
    函数语句;
}
```

1. 如果不需要捕获，则捕获列表可以为空。
2. 如果不需要参数，则参数列表可以为空。参数列表如果为空，那么可以省略它。
3. 返回类型是可选的，如果省略，则假定为auto（返回类型会自动推导）。虽然我们之前注意到应该避免函数返回类型的自动推导，但在这种情况下，使用它是很好用的（因为这些函数通常非常简单）。

还要注意，lambda函数（匿名）没有名称，因为我们不需要提供名称。

这意味着简单的lambda定义如下所示:

```C++
#include <iostream>

int main()
{
  [] {}; // 没有返回类型，没有捕获列表，没有参数的lambda

  return 0;
}
```

让我们使用lambda重写上面的示例:

```C++
#include <algorithm>
#include <array>
#include <iostream>
#include <string_view>

int main()
{
  constexpr std::array<std::string_view, 4> arr{ "apple", "banana", "walnut", "lemon" };

  // 在使用的地方，定义函数
  auto found{ std::find_if(arr.begin(), arr.end(),
                           [](std::string_view str) // 这里是没有捕获列表的lambda函数
                           {
                             return str.find("nut") != std::string_view::npos;
                           }) };

  if (found == arr.end())
  {
    std::cout << "No nuts\n";
  }
  else
  {
    std::cout << "Found " << *found << '\n';
  }

  return 0;
}
```

这与函数指针情况类似，并产生相同的结果:

```C++
Found walnut
```

请注意，lambda与containsNut函数是多么相似。它们都具有相同的参数和函数体。这里lambda没有捕获列表（我们将在下一课中解释捕获列表是什么），因为它不需要捕获外层的对象。我们在lambda中省略了尾部返回类型（为了简洁），但由于运算符!=返回布尔值，我们的lambda函数也将返回布尔值。


{{< alert success >}}
**最佳实践**

根据在最小范围和最接近首次使用的情况下定义事物的最佳实践，当我们需要一个简单的一次性函数作为参数传递给其他函数时，与普通函数相比，lambda更受欢迎。

{{< /alert >}}

***
## lambda函数的类型

在上面的例子中，我们在需要的地方定义了lambda。lambda的这种用法有时称为函数字面值。

然而，在使用的同一行中编写lambda有时会使代码更难阅读。就像我们可以用字面值（或函数指针）初始化变量以供以后使用一样，我们也可以定义初始化lambda变量，然后在以后使用它。命名的lambda和良好的函数名可以使代码更容易阅读。

例如，在下面的片段中，我们使用std::all_of检查数组的所有元素是否为偶数:

```C++
// Bad: 需要阅读lambda函数内部，才能知道发生了什么
return std::all_of(array.begin(), array.end(), [](int i){ return ((i % 2) == 0); });
```

我们可以通过以下方式提高其可读性:

```C++
// Good: 将lambda函数存储在一个命名变量中，增加可读性
auto isEven{
  [](int i)
  {
    return (i % 2) == 0;
  }
};

return std::all_of(array.begin(), array.end(), isEven);
```

请注意最后一行的内容的含义:“返回数组中的所有元素是否为偶数”

但isEven的类型是什么？

事实是，lambda函数没有我们可以显式使用的类型。当我们编写lambda时，编译器将为lambda生成唯一类型，这个类型不为我们公开。

尽管我们不知道lambda的类型，但有几种存储lambda以供后期定义使用的方法。如果lambda有一个空的捕获子句（括号[]之间没有任何内容），可以使用普通函数指针。或者通过auto关键字（即使lambda具有非空的捕获子句）。

```C++
#include <functional>

int main()
{
  // 常规的函数指针. 只有没有捕获子句时使用 (空 []).
  double (*addNumbers1)(double, double){
    [](double a, double b) {
      return a + b;
    }
  };

  addNumbers1(1, 2);

  // 使用 std::function. 可以有非空的捕获子句 (下节讨论).
  std::function addNumbers2{ // 注: C++17 之前, 需要使用 std::function<double(double, double)>
    [](double a, double b) {
      return a + b;
    }
  };

  addNumbers2(3, 4);

  // 使用 auto. 按 lambda的真正类型进行存储
  auto addNumbers3{
    [](double a, double b) {
      return a + b;
    }
  };

  addNumbers3(5, 6);

  return 0;
}
```

使用lambda的实际真正类型的唯一方法是通过auto。与std::function相比，auto的优点是没有额外开销。

如果我们想将lambda传递给函数怎么办？有4个选项:

```C++
#include <functional>
#include <iostream>

// Case 1:  使用 `std::function` 参数
void repeat1(int repetitions, const std::function<void(int)>& fn)
{
    for (int i{ 0 }; i < repetitions; ++i)
        fn(i);
}

// Case 2: 使用函数模板
template <typename T>
void repeat2(int repetitions, const T& fn)
{
    for (int i{ 0 }; i < repetitions; ++i)
        fn(i);
}

// Case 3: 使用缩写的函数模板 (C++20)
void repeat3(int repetitions, const auto& fn)
{
    for (int i{ 0 }; i < repetitions; ++i)
        fn(i);
}

// Case 4: 使用函数指针 (只适用没有捕获列表的lambda)
void repeat4(int repetitions, void (*fn)(int))
{
    for (int i{ 0 }; i < repetitions; ++i)
        fn(i);   
}

int main()
{
    auto lambda = [](int i)
    {
        std::cout << i << '\n';
    };

    repeat1(3, lambda);
    repeat2(3, lambda);
    repeat3(3, lambda);
    repeat4(3, lambda);

    return 0;
}
```

在案例1中，我们的函数参数是一个std::function。这很好，因为我们可以显式地看到std::function的参数和返回类型是什么。然而，这要求每当调用函数时隐式转换lambda，这增加了一些开销。如果需要，该方法还具有可分离声明（在头文件中）和实现（在.cpp文件中）的优点。

在案例2中，使用了一个具有模板类型参数T的函数模板。当调用该函数时，将实例化一个函数，其中T与lambda的实际类型匹配。这是更有效率的，但T的参数和返回类型并不明显。

在案例3中，我们使用C++20的auto来调用缩写的函数模板语法。这将生成与情况2相同的函数模板。

在情况4中，函数参数是函数指针。由于没有捕获的lambda将隐式转换为函数指针，因此可以将没有捕获的lambda传递给该函数。

{{< alert success >}}
**关键点**

将lambda存储在变量中为我们提供了一种为lambda提供有用名称的方法，这有助于提高代码的可读性。

将lambda存储在变量中还为我们提供了一种多次使用该lambda的方法。

{{< /alert >}}

{{< alert success >}}
**对于高级读者**

实际上，lambda不是函数（这是它们避免C++不支持嵌套函数的限制的方式）。它们是一种特殊的对象，称为函子（functor）。它是包含"重载运算符()"的对象，使它们像函数一样可调用。

{{< /alert >}}

{{< alert success >}}
**最佳实践**

在变量中存储lambda时，请使用auto作为变量的类型。

将lambda传递给函数时:

1. 如果支持C++20，请使用auto作为参数的类型。
2. 否则，请使用具有类型模板参数或std::function参数的函数（如果lambda没有捕获，则使用函数指针）。

{{< /alert >}}

***
## 泛型lambda

在大多数情况下，lambda参数的工作规则与常规函数参数相同。

一个值得注意的例外是，自从C++14以来，我们被允许对参数使用auto（注意:在C++20中，普通函数也可以对参数使用auto）。当lambda具有一个或多个auto参数时，编译器将自动推导lambda调用时需要的参数类型。

由于具有一个或多个auto参数的lambda可以潜在地与各种类型一起工作，因此它们被称为泛型lambdas。

让我们看一看泛型lambda:

```C++
#include <algorithm>
#include <array>
#include <iostream>
#include <string_view>

int main()
{
  constexpr std::array months{ // C++17 之前使用 std::array<const char*, 12>
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
  };

  // 寻找开头字母一样的相邻月份
  const auto sameLetter{ std::adjacent_find(months.begin(), months.end(),
                                      [](const auto& a, const auto& b) {
                                        return a[0] == b[0];
                                      }) };

  // 检查是否存在
  if (sameLetter != months.end())
  {
    // std::next 返回 下一个迭代器
    std::cout << *sameLetter << " and " << *std::next(sameLetter)
              << " start with the same letter\n";
  }

  return 0;
}
```

输出:

```C++
June and July start with the same letter
```

在上面的示例中，我们使用auto参数通过常量引用捕获字符串。由于所有字符串类型都允许通过操作符[]访问其单个字符，因此我们不需要关心用户是在传递std::string、C样式字符串还是其他内容。这允许我们编写一个可以接受其中任何一个的lambda，这意味着如果我们在几个月后更改类型，就不必重写lambda。

然而，auto并不总是最好的选择。考虑:

```C++
#include <algorithm>
#include <array>
#include <iostream>
#include <string_view>

int main()
{
  constexpr std::array months{ // C++17 之前使用 std::array<const char*, 12>
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
  };

  // 判断多少个月份的字母长度为5
  const auto fiveLetterMonths{ std::count_if(months.begin(), months.end(),
                                       [](std::string_view str) {
                                         return str.length() == 5;
                                       }) };

  std::cout << "There are " << fiveLetterMonths << " months with 5 letters\n";

  return 0;
}
```

输出:

```C++
There are 2 months with 5 letters
```

在本例中，使用auto将str推导const char*的类型。C样式的字符串不容易使用（除了使用操作符[]）。在这种情况下，我们更喜欢将参数显式定义为std::string_view，这允许我们更容易地处理底层数据（例如，我们可以查看string_view的长度，即使用户传入了C样式数组）。

{{< alert success >}}
**对于高级读者**

在lambda的上下文中使用时，auto只是模板参数的简写。

{{< /alert >}}

***
## Constexpr lambda

从C++17开始，如果计算结果满足常量表达式的要求，则lambda是隐式constexpr。这通常需要两件事:

1. lambda必须没有捕获，或者所有捕获都必须是constexpr。
2. lambda调用的函数必须是constexpr。注意，许多标准库算法和数学函数直到C++20或C++23才成为constexpr。


在上面的示例中，我们的lambda在C++17中不会隐式为constexpr，但在C++20中会是（因为在C++20中将std::count_if设置为consterpr）。这意味着在C++20中，我们可以制作constexpr fiveLetterMonths:

```C++
  constexpr auto fiveLetterMonths{ std::count_if(months.begin(), months.end(),
                                       [](std::string_view str) {
                                         return str.length() == 5;
                                       }) };
```

***
## 泛型lambda和静态变量

在前面函数模板实例化中，我们讨论了当函数模板包含静态局部变量时，从该模板实例的每个函数将拥有自己的独立静态局部变量。如果这不是您预期的行为，则可能会导致问题。

泛型lambda的工作方式相同:将为auto解析为的每个不同类型生成唯一的lambda。

以下示例显示了一个泛型lambda如何转变为两个不同的lambda:

```C++
#include <algorithm>
#include <array>
#include <iostream>
#include <string_view>

int main()
{
  // 打印的同时，并记录打印了多少次
  auto print{
    [](auto value) {
      static int callCount{ 0 };
      std::cout << callCount++ << ": " << value << '\n';
    }
  };

  print("hello"); // 0: hello
  print("world"); // 1: world

  print(1); // 0: 1
  print(2); // 1: 2

  print("ding dong"); // 2: ding dong

  return 0;
}
```

输出

```C++
0: hello
1: world
0: 1
1: 2
2: ding dong
```

在上面的示例中，我们定义了一个lambda，然后用两个不同的参数（字符串和整数）调用它。这将生成lambda的两个不同版本（一个具有字符串参数，另一个具有整数参数）。

大多数时候，这是无关紧要的。然而，请注意，如果泛型lambda使用静态变量，则这些变量不会在生成的lambda之间共享。

我们可以在上面的示例中看到这一点，其中每个类型（字符串和整数）都有自己的唯一计数！尽管我们只编写了一次lambda，但生成了两个lambda——每个lambda都有自己的callCount版本。要在两个生成的lambda之间共享计数器，我们必须在lambda之外定义全局变量或静态局部变量。正如您在前面的课程中所知道的，全局和静态局部变量都可能导致问题，并使代码更难理解。在下一课中讨论lambda捕获后，我们可以优化这类的写法。

***
## 返回类型推导和尾部返回类型

如果使用返回类型推导，则从lambda内的return语句中推导出lambda的返回类型，并且lambda中的所有返回语句都必须返回相同的类型（否则编译器将不知道使用哪个）。

例如:

```C++
#include <iostream>

int main()
{
  auto divide{ [](int x, int y, bool intDivision) { // 注: 未声明返回类型
    if (intDivision)
      return x / y; // return 的类型是 int
    else
      return static_cast<double>(x) / y; // 错误: return 的类型与上一个return的类型不同
  } };

  std::cout << divide(3, 2, true) << '\n';
  std::cout << divide(3, 2, false) << '\n';

  return 0;
}
```

这会产生编译错误，因为第一个返回语句的返回类型（int）与第二个返回语句（double）的返回类型不匹配。

在返回不同类型的情况下，我们有两个选项:

1. 显示的转换return语句的返回值类型
2. 显式的声明lambda函数的返回值类型，让编译器隐式的转换return的结果

第二种情况通常是更好的选择:

```C++
#include <iostream>

int main()
{
  // 注: 显示声明返回值类型为double
  auto divide{ [](int x, int y, bool intDivision) -> double {
    if (intDivision)
      return x / y; // 计算结果会隐式的转换为double
    else
      return static_cast<double>(x) / y;
  } };

  std::cout << divide(3, 2, true) << '\n';
  std::cout << divide(3, 2, false) << '\n';

  return 0;
}
```

这样，如果您决定更改返回类型，（通常）只需要更改lambda的返回类型，而不需要修改lambda函数主体。

***
## 标准库函数对象

对于常见的操作（例如加法、求反或比较），您不需要编写自己的lambda，因为标准库附带了许多可以替代的基本可调用对象。这些在\<functional\>头文件中定义。

在以下示例中:

```C++
#include <algorithm>
#include <array>
#include <iostream>

bool greater(int a, int b)
{
  // 如果a大于b，那么a排在b前面
  return a > b;
}

int main()
{
  std::array arr{ 13, 90, 99, 5, 40, 80 };

  // 传递 greater 给 std::sort
  std::sort(arr.begin(), arr.end(), greater);

  for (int i : arr)
  {
    std::cout << i << ' ';
  }

  std::cout << '\n';

  return 0;
}
```

输出

```C++
99 90 80 40 13 5
```

我们可以使用std::greater:

```C++
#include <algorithm>
#include <array>
#include <iostream>
#include <functional> // for std::greater

int main()
{
  std::array arr{ 13, 90, 99, 5, 40, 80 };

  // 传递 std::greater 给 std::sort
  std::sort(arr.begin(), arr.end(), std::greater{}); // 注: 需要加括号，来传递一个对象

  for (int i : arr)
  {
    std::cout << i << ' ';
  }

  std::cout << '\n';

  return 0;
}
```

输出

```C++
99 90 80 40 13 5
```

***
## 结论

与使用循环的解决方案相比，Lambda和算法库似乎有些复杂。然而，这种组合可以在短短几行代码中实现一些非常强大的操作，并且比编写自己的循环更具可读性。此外，算法库还具有强大且易于使用的并行计算能力，这是循环无法实现的。升级使用库函数的源代码比升级使用循环的代码容易。

Lambda非常棒，但它们并不能在所有情况下取代常规函数。对于复杂或者需要可重用的情况，首选常规函数。

***

