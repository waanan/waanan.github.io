---
title: "Lambda捕获"
date: 2024-08-20T10:49:32+08:00
---

## 捕获子句和按值捕获

在上一课，我们介绍了以下示例：

```C++
#include <algorithm>
#include <array>
#include <iostream>
#include <string_view>

int main()
{
  std::array<std::string_view, 4> arr{ "apple", "banana", "walnut", "lemon" };

  auto found{ std::find_if(arr.begin(), arr.end(),
                           [](std::string_view str)
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

现在，让我们修改nut示例，并让用户选择要搜索的子字符串。这并不像你预期的那样直观。

```C++
#include <algorithm>
#include <array>
#include <iostream>
#include <string_view>
#include <string>

int main()
{
  std::array<std::string_view, 4> arr{ "apple", "banana", "walnut", "lemon" };

  // 询问用户需要搜索的字符串.
  std::cout << "search for: ";

  std::string search{};
  std::cin >> search;

  auto found{ std::find_if(arr.begin(), arr.end(), [](std::string_view str) {
    // 搜索 @search 而不是 "nut".
    return str.find(search) != std::string_view::npos; // 错误: search 无法在此作用域内使用
  }) };

  if (found == arr.end())
  {
    std::cout << "Not found\n";
  }
  else
  {
    std::cout << "Found " << *found << '\n';
  }

  return 0;
}
```

此代码无法编译。与嵌套块不同，在嵌套块中可以访问外部块中的任何标识符，而lambda只能访问在lambda外部定义的某些类型的对象。这包括：

1. 具有静态（或线程局部）存储期的对象（这包括全局变量和静态局部变量）
2. constexpr对象（显式或隐式）

由于search不满足这些要求，所以lambda无法看到它。

要从lambda中访问search，我们需要使用捕获子句。

***
## 捕获子句

捕获子句用于（间接）为lambda提供对外层作用域中可用的变量的访问，而lambda通常无权访问这些变量。我们所需要做的只是将要从lambda中访问的实体列为捕获子句的一部分。在这种情况下，我们希望让lambda访问变量search的值，因此将其添加到捕获子句中：

```C++
#include <algorithm>
#include <array>
#include <iostream>
#include <string_view>
#include <string>

int main()
{
  std::array<std::string_view, 4> arr{ "apple", "banana", "walnut", "lemon" };

  std::cout << "search for: ";

  std::string search{};
  std::cin >> search;

  // 捕获 @search                                   vvvvvv
  auto found{ std::find_if(arr.begin(), arr.end(), [search](std::string_view str) {
    return str.find(search) != std::string_view::npos;
  }) };

  if (found == arr.end())
  {
    std::cout << "Not found\n";
  }
  else
  {
    std::cout << "Found " << *found << '\n';
  }

  return 0;
}
```

用户现在可以搜索数组的元素。

输出

```C++
search for: nana
Found banana
```

***
## 那么捕获实际上是如何工作的呢？

虽然上面示例中的lambda看起来像是直接访问main的search变量的值，但情况并非如此。Lambda可能看起来像嵌套块，但它们的工作方式略有不同。

当执行lambda定义时，对于lambda捕获的每个变量，在lambda中创建该变量的克隆变量（具有相同的名称）。此时，这些克隆的变量从同名的外部作用域的变量初始化。

因此，在上面的示例中，当创建lambda对象时，lambda获得自己的克隆变量search。这个克隆的search与main的search具有相同的值，因此它的行为就像访问main的search一样。

虽然这些克隆的变量具有相同的名称，但它们不一定具有与原始变量相同的类型。我们将在本课接下来的部分中探索这一点。

{{< alert success >}}
**关键点**

lambda的捕获变量是外部作用域变量的副本，而不是实际变量。

{{< /alert >}}

{{< alert success >}}
**对于高级读者**

尽管lambda看起来像函数，但它们实际上是可以像函数一样调用的对象（这些被称为functors——我们将在以后的课程中讨论如何从头开始创建自己的functor）。

当编译器遇到lambda定义时，它为lambda创建自定义对象定义。每个捕获的变量都成为对象的数据成员。

在运行时，当遇到lambda定义时，将实例化lambda对象，并在此时初始化lambda的成员。

{{< /alert >}}

***
## 默认情况下，捕获被视为常量

调用lambda时，调用lambda对象operator()。默认情况下，此运算符()将捕获视为常量，这意味着不允许lambda修改这些捕获。

在下面的例子中，我们捕获可变ammo并尝试减少它。

```C++
#include <iostream>

int main()
{
  int ammo{ 10 };

  // 定义 lambda 捕获 ammo.
  auto shoot{
    [ammo]() {
      // 非法, ammo 不能被修改.
      --ammo;

      std::cout << "Pew! " << ammo << " shot(s) left.\n";
    }
  };

  // 调用lambda
  shoot();

  std::cout << ammo << " shot(s) left\n";

  return 0;
}
```

上面的代码不会编译，因为ammo在lambda中被视为const。

***
## 可修改的捕获

为了允许修改捕获的变量，我们可以将lambda标记为mutable：

```C++
#include <iostream>

int main()
{
  int ammo{ 10 };

  auto shoot{
    [ammo]() mutable { // 现在是 mutable
      // 允许修改 ammo 
      --ammo;

      std::cout << "Pew! " << ammo << " shot(s) left.\n";
    }
  };

  shoot();
  shoot();

  std::cout << ammo << " shot(s) left\n";

  return 0;
}
```

输出：

```C++
Pew! 9 shot(s) left.
Pew! 8 shot(s) left.
10 shot(s) left
```

虽然现在可以编译，但仍然存在逻辑错误。发生了什么事？当shoot被创建时，它捕获了一个ammo的副本。当lambda将ammo从10减少到9到8时，它会减少自己的副本，而不是main()中的原始ammo值。

请注意，在对lambda的调用之间，保存着它内部ammo的值！

{{< alert success >}}
**警告**

因为捕获的变量是lambda对象的成员，所以它们的值在对lambda的多个调用中被持久化！

{{< /alert >}}

***
## 通过引用捕获

就像函数可以更改通过引用传递的参数的值一样，我们也可以通过引用捕获变量，以允许lambda影响参数的值。

为了通过引用捕获变量，我们在捕获中的变量名前面加上一个与号（&）。与通过值捕获的变量不同，通过引用捕获的变量是非常量，除非它们捕获的变量为常量。每当您希望通过引用将参数传递给函数时（例如，对于非基本类型），应首选通过引用捕获而不是通过值捕获。

下面是上面的代码，其中包含通过引用捕获的ammo：

```C++
#include <iostream>

int main()
{
  int ammo{ 10 };

  auto shoot{
    // 不需要标记为 mutable
    [&ammo]() { // &ammo 因为着 ammo 按引用捕获
      // 修改 ammo 会影响 main 中的 ammo
      --ammo;

      std::cout << "Pew! " << ammo << " shot(s) left.\n";
    }
  };

  shoot();

  std::cout << ammo << " shot(s) left\n";

  return 0;
}
```

这会产生预期的答案：

```C++
Pew! 9 shot(s) left.
9 shot(s) left
```

现在，让我们使用引用捕获来计算std::sort在对数组进行排序时进行了多少比较。

```C++
#include <algorithm>
#include <array>
#include <iostream>
#include <string_view>

struct Car
{
  std::string_view make{};
  std::string_view model{};
};

int main()
{
  std::array<Car, 3> cars{ { { "Volkswagen", "Golf" },
                             { "Toyota", "Corolla" },
                             { "Honda", "Civic" } } };

  int comparisons{ 0 };

  std::sort(cars.begin(), cars.end(),
    // 按引用捕获 @comparisons
    [&comparisons](const auto& a, const auto& b) {
      // 可以修改main函数中的comparisons
      ++comparisons;

      // Sort the cars by their make.
      return a.make < b.make;
  });

  std::cout << "Comparisons: " << comparisons << '\n';

  for (const auto& car : cars)
  {
    std::cout << car.make << ' ' << car.model << '\n';
  }

  return 0;
}
```

可能的输出

```C++
Comparisons: 2
Honda Civic
Toyota Corolla
Volkswagen Golf
```

***
## 捕获多个变量

可以通过用逗号分隔多个变量来捕获它们。这可以包括通过值或引用捕获的变量的组合：

```C++
int health{ 33 };
int armor{ 100 };
std::vector<CEnemy> enemies{};

// 按值捕获 health 和 armor, 按引用捕获 enemies.
[health, armor, &enemies](){};
```

***
## 默认捕获

必须显式列出要捕获的变量可能会很麻烦。如果修改lambda，可能会忘记添加或删除捕获的变量。幸运的是，我们可以利用编译器的帮助来自动生成需要捕获的变量列表。

默认捕获会自动捕获lambda中用到的所有变量。

要按值捕获所有使用的变量，请使用“=”。要通过引用捕获所有使用的变量，请使用“&”。

下面是使用默认按值捕获的示例：

```C++
#include <algorithm>
#include <array>
#include <iostream>

int main()
{
  std::array areas{ 100, 25, 121, 40, 56 };

  int width{};
  int height{};

  std::cout << "Enter width and height: ";
  std::cin >> width >> height;

  auto found{ std::find_if(areas.begin(), areas.end(),
                           [=](int knownArea) { // 按值捕获 width 和 height 
                             return width * height == knownArea; // 因为他们在这里被使用了
                           }) };

  if (found == areas.end())
  {
    std::cout << "I don't know this area :(\n";
  }
  else
  {
    std::cout << "Area found :)\n";
  }

  return 0;
}
```

默认捕获可以与正常捕获混合。我们可以通过值捕获一些变量，通过引用捕获其他变量，但每个变量只能捕获一次。

```C++
int health{ 33 };
int armor{ 100 };
std::vector<CEnemy> enemies{};

// health 与 armor 按值捕获, enemies 按引用捕获.
[health, armor, &enemies](){};

// enemies 按引用捕获，其余全按值捕获
[=, &enemies](){};

// armor 按值捕获，其余全按引用捕获
[&, armor](){};

// 非法, armor被按引用捕获了两次
[&, &armor](){};

// 非法, armor被按值捕获了两次
[=, armor](){};

// 非法, armor 出现了两次
[armor, &health, &armor](){};

// 非法, 默认捕获需要时捕获列表中的第一位
[armor, &](){};
```

***
## 在lambda捕获中定义新变量

有时，我们希望捕获稍微修改的变量，或者声明一个仅在lambda范围内可见的新变量。我们可以通过在lambda捕获中定义变量而不指定其类型来实现这一点。

```C++
#include <array>
#include <iostream>
#include <algorithm>

int main()
{
  std::array areas{ 100, 25, 121, 40, 56 };

  int width{};
  int height{};

  std::cout << "Enter width and height: ";
  std::cin >> width >> height;

  // 使用userArea，从捕获的width和height计算
  auto found{ std::find_if(areas.begin(), areas.end(),
                           // 新声明的变量userArea只在lambda内可见
                           // userArea 的类型被自动推导为 int.
                           [userArea{ width * height }](int knownArea) {
                             return userArea == knownArea;
                           }) };

  if (found == areas.end())
  {
    std::cout << "I don't know this area :(\n";
  }
  else
  {
    std::cout << "Area found :)\n";
  }

  return 0;
}
```

定义lambda时，userArea将仅计算一次。计算的面积存储在lambda对象中，并且对于每个调用都是相同的。如果lambda是可变的，并且修改了捕获中定义的变量，则原始值将被覆盖。

{{< alert success >}}
**最佳实践**

仅当变量的值较短且类型明显时，才在捕获中初始化变量。否则，最好在lambda之外定义变量并捕获它。

{{< /alert >}}

***
## 悬空捕获的变量

变量在定义lambda的点捕获。如果引用捕获的变量在lambda之前死亡，则lambda将保留一个悬空引用。

例如：

```C++
#include <iostream>
#include <string>

// 返回一个lambda
auto makeWalrus(const std::string& name)
{
  // 按引用捕获name并返回lambda
  return [&]() {
    std::cout << "I am a walrus, my name is " << name << '\n'; // 未定义的行为
  };
}

int main()
{
  // 创建一个新的 walrus， name 是 Roofus.
  // sayName 是 makeWalrus 返回的lambda
  auto sayName{ makeWalrus("Roofus") };

  // 调用 makeWalrus 返回的lambda.
  sayName();

  return 0;
}
```

对makeWalrus的调用从字符串字面值“Roofus”创建临时std::string。makeWalrus中的lambda通过引用捕获临时字符串。当makeWalrus返回时，临时字符串死亡，但lambda仍然引用它。然后，当我们调用sayName时，将访问悬挂引用，导致未定义的行为。

请注意，如果name通过值传递给makeWalrus，也会发生这种情况。变量name仍然在makeWalrus的末尾死亡，lambda保留了一个悬空的引用。

如果希望在使用lambda时捕获的名称有效，则需要改为按值捕获它（显式或使用默认的按值捕获）。

{{< alert success >}}
**警告**

通过引用捕获变量时要格外小心，特别是使用默认按引用捕获时。捕获的变量必须比lamdba寿命长。

{{< /alert >}}

***
## 可变lambda的意外副本

因为lambda是对象，所以可以复制它们。在某些情况下，这可能会导致问题。考虑以下代码：

```C++
#include <iostream>

int main()
{
  int i{ 0 };

  // 创建一个新的 lambda 名称为 count
  auto count{ [i]() mutable {
    std::cout << ++i << '\n';
  } };

  count(); // 调用 count

  auto otherCount{ count }; // 创建 count 的副本

  // 调用 count 和 副本
  count();
  otherCount();

  return 0;
}
```

输出

```C++
1
2
2
```

代码不是打印1、2、3，而是打印2两次。当我们创建otherCount作为count的副本时，我们创建了count当前状态的副本。count的i是1，所以otherCount的i也是1。由于otherCount是count的副本，因此它们每个都有自己的i。

现在，让我们看一个稍微不太明显的例子：

```C++
#include <iostream>
#include <functional>

void myInvoke(const std::function<void()>& fn)
{
    fn();
}

int main()
{
    int i{ 0 };

    // 递增并打印存储的 @i.
    auto count{ [i]() mutable {
      std::cout << ++i << '\n';
    } };

    myInvoke(count);
    myInvoke(count);
    myInvoke(count);

    return 0;
}
```

输出：

```C++
1
1
1
```

这以更模糊的形式展示了与前面示例相同的问题。

当我们调用myInvoke(count)时，编译器将看到count（具有lambda类型）与引用参数类型（std::function\<void()\>）的类型不匹配。它将把lambda转换为临时std::function，以便引用参数可以绑定到它，这将制作lambda的副本。因此，对fn()的调用实际上是在lambda的副本上执行的，该副本作为临时std::function的一部分存在，而不是实际的lambda。

如果我们需要传递可变的lambda，并希望避免无意中复制的可能性，则有两种选择。一种选择是改用非捕获lambda——在上面的例子中，我们可以删除捕获并改用静态局部变量来跟踪状态。但静态局部变量可能很难跟踪，并使代码的可读性降低。一个更好的选择是首先防止复制我们的lambda。但由于我们不能影响std::function（或其他标准库函数或对象）的实现方式，我们如何才能做到这一点？

一个选项是立即将lambda放入std::function中。这样，当我们调用myInvoke()时，引用参数fn可以绑定到我们的std::function，并且不会生成临时副本：

```C++
#include <iostream>
#include <functional>

void myInvoke(const std::function<void()>& fn)
{
    fn();
}

int main()
{
    int i{ 0 };

    // 递增并打印存储的 @i.
    std::function count{ [i]() mutable { // lambda 存储在 std::function
      std::cout << ++i << '\n';
    } };

    myInvoke(count); // 调用时不会创建副本
    myInvoke(count); // 调用时不会创建副本
    myInvoke(count); // 调用时不会创建副本

    return 0;
}
```

产出现在如预期：

```C++
1
2
3
```

另一种解决方案是使用引用包装器。C++提供了一种方便的类型（作为\<functional\>头文件的一部分），称为std::reference_wrapper，它允许我们像传递引用一样传递普通类型。为了更方便，可以使用std::ref()函数创建std::reference_wrapper。通过将lambda包装在std::reference_wrapper中，每当任何人试图复制我们的lambda时，他们都会复制reference_ wrapper（避免复制lambda）。

下面是我们使用std:：ref更新的代码：

```C++
#include <iostream>
#include <functional> // 引入 std::reference_wrapper 和 std::ref

void myInvoke(const std::function<void()>& fn)
{
    fn();
}

int main()
{
    int i{ 0 };

    // 递增并打印存储的 @i.
    auto count{ [i]() mutable {
      std::cout << ++i << '\n';
    } };

    // std::ref(count) 确保count行为象引用一样
    // 任何拷贝count的行为，就像是拷贝了count的引用
    // 这样只会有一个count存在
    myInvoke(std::ref(count));
    myInvoke(std::ref(count));
    myInvoke(std::ref(count));

    return 0;
}
```

产出现在如预期：

```C++
1
2
3
```

该方法的有趣之处在于，即使myInvoke按值（而不是按引用）获取fn，它也可以工作！

{{< alert success >}}
**规则**

标准库函数可能会复制函数对象（提示：lambda是函数对象）。如果要为lambda提供可变的捕获变量，请使用std::ref通过引用传递它们。

{{< /alert >}}

{{< alert success >}}
**最佳实践**

尽量避免可变lambdas。不可变的lambdas更容易理解，并且不会受到上述问题的影响，可变lambda以及在添加并行执行时出现的更危险的问题。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter20/lambda/" next="/basic/chapter20/summary/" >}}
20.5 lambda（匿名函数）简介
<--->
20.7 第20章总结
{{< /prevnext >}}
