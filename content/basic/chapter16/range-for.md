---
title: "基于范围的for循环（range for / for each）"
date: 2024-07-08T11:10:28+08:00
---

前面展示了使用for循环迭代数组的每个元素的示例，其中使用循环变量作为索引。下面是一个这样的例子：

```C++
#include <iostream>
#include <vector>

int main()
{
    std::vector fibonacci { 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89 };

    std::size_t length { fibonacci.size() };
    for (std::size_t index { 0 }; index < length; ++index)
       std::cout << fibonacci[index] << ' ';

    std::cout << '\n';

    return 0;
}
```

尽管for循环提供了一种方便而灵活的方法来迭代数组，但它们也很容易搞乱，容易出现索引超出正常界限的错误，并且容易出现数组索引变量的符号问题。

由于遍历数组是一件很常见的事情，C++支持另一种类型的for循环，称为基于范围的for循环（有时也称为for each循环），该循环允许遍历容器，而不必执行显式索引。基于范围的for循环更简单、更安全，并且可以与C++中的所有常见数组类型（包括std::vector、std:∶array和C样式数组）一起使用。

***
## 基于范围的for循环

基于范围的for语句的语法如下所示：

```C++
for (元素声明 : 数组对象)
   语句;
```

当遇到基于范围的for循环时，循环将迭代“数组对象”中的每个元素。对于每个迭代，当前数组元素的值将被分配给“元素声明”中声明的变量，然后执行语句。

为了获得最佳结果，“元素声明”应该与数组元素具有相同的类型，否则将发生类型转换。

下面是一个简单的示例，使用基于范围的for循环来打印名为fibonacci的数组中的所有元素：

```C++
#include <iostream>
#include <vector>

int main()
{
    std::vector fibonacci { 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89 };

    for (int num : fibonacci) // 迭代 fibonacci 里的每个元素，将其拷贝到 `num`
       std::cout << num << ' '; // 打印 `num` 的值

    std::cout << '\n';

    return 0;
}
```

这将打印：

```C++
0 1 1 2 3 5 8 13 21 34 55 89
```

注意，这个例子不需要我们使用数组的长度，也不需要索引数组！

让我们仔细看看这是如何工作的。这个基于范围的for循环将在fibonacci的所有元素中执行。对于第一次迭代，变量num被分配为第一个元素（0）的值。然后，程序执行关联的语句，该语句将num（0）的值打印到控制台。对于第二次迭代，为num分配第二个元素（1）的值。关联的语句再次执行，打印1。基于范围的for循环继续依次迭代每个数组元素，为每个元素执行关联的语句，直到数组中没有剩余的元素可以迭代。此时，循环终止，程序继续执行（打印换行，然后将0返回到操作系统）。

由于num被分配了数组元素的值，这意味着复制了数组元素（对于某些类型，这可能很昂贵）。

{{< alert success >}}
**关键点**

声明的元素（上例中的num）不是数组索引。相反，它被分配为被迭代的数组元素的值。

{{< /alert >}}

{{< alert success >}}
**最佳实践**

遍历容器时，优先使用基于范围的for循环。

{{< /alert >}}

***
## 使用auto关键字进行类型自动推导

因为元素声明应该与数组元素具有相同的类型（以防止发生类型转换），所以这是使用auto关键字的理想情况，让编译器为我们推断数组元素的类型。这样，就不必冗余地指定类型，也不会有意外输入错误。

下面是与上面相同的示例，但使用auto作为num的类型：

```C++
#include <iostream>
#include <vector>

int main()
{
    std::vector fibonacci { 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89 };

    for (auto num : fibonacci) // 编译器将会自动推导 num 的类型是 `int`
       std::cout << num << ' ';

    std::cout << '\n';

    return 0;
}
```

由于std::vector fibonacci具有int类型的元素，因此num将被推断为int。

使用auto的另一个好处是，如果数组的元素类型曾经更新过（例如，从int改成long），auto将自动推断更新的元素类型，确保它们保持同步（并防止发生类型转换）。

{{< alert success >}}
**最佳实践**

将类型演绎（auto）与基于范围的for循环一起使用，以使编译器推断数组元素的类型。

{{< /alert >}}

***
## 尽量避免使用拷贝

考虑以下基于范围的for循环，它在std::string数组上迭代：

```C++
#include <iostream>
#include <string>
#include <vector>

int main()
{
    std::vector<std::string> words{ "peter", "likes", "frozen", "yogurt" };

    for (auto word : words)
        std::cout << word << ' ';

    std::cout << '\n';

    return 0;
}
```

对于这个循环的每个迭代，words数组中的下一个std::string元素将被分配（复制）到变量word中。复制std::string的开销很大，这就是为什么我们通常通过常量引用将std:∶string传递给函数的原因。我们希望避免复制成本高昂的东西，除非确实需要副本。在当前情况下，我们只是打印副本的值，然后副本被销毁。如果可以避免复制，而只是引用实际的数组元素，那将更好。

幸运的是，可以通过将“元素声明”设置为（const）引用来实现这一点：

```C++
#include <iostream>
#include <string>
#include <vector>

int main()
{
    std::vector<std::string> words{ "peter", "likes", "frozen", "yogurt" };

    for (const auto& word : words) // word 现在是常量引用
        std::cout << word << ' ';

    std::cout << '\n';

    return 0;
}
```

在上面的示例中，word现在是常量引用。在该循环的每次迭代中，word将绑定到下一个数组元素。这允许访问数组元素的值，而不必制作昂贵的副本。

如果引用是非常量的，则它也可以用于更改数组中的值（如果“元素声明”是值的副本，则这是不可能的）。

***
## 什么时候使用 auto，auto& 或 const auto&

通常，可廉价复制类型使用auto，需要更改的对象使用 auto&， 昂贵地复制类型使用 const auto&。但对于基于范围的for循环，许多开发人员认为最好始终使用const auto&，因为它更经得起未来的考验。

例如，考虑以下示例：

```C++
#include <iostream>
#include <string_view>
#include <vector>

int main()
{
    std::vector<std::string_view> words{ "peter", "likes", "frozen", "yogurt" }; // 元素是 std::string_view

    for (auto word : words) // string_view 通常按值传递，所以这里使用auto
        std::cout << word << ' ';

    std::cout << '\n';

    return 0;
}
```

在这个例子中，有一个包含std::string_view对象的std:∶vector。由于std::string_view通常通过值传递，因此使用auto似乎是合适的。

但考虑一下，如果后来将words更新为std::string数组，会发生什么情况。

```C++
#include <iostream>
#include <string>
#include <vector>

int main()
{
    std::vector<std::string> words{ "peter", "likes", "frozen", "yogurt" }; // 这里修改了

    for (auto word : words) // 可能这里也需要修改了
        std::cout << word << ' ';

    std::cout << '\n';

    return 0;
}
```

基于范围的for循环将很好地编译和执行，但word现在将被推断为std::string，并且由于我们使用的是auto，因此循环将无声地制作std::string元素的昂贵副本。性能受到了巨大的影响！

有两种合理的方法可以确保不会发生这种情况：

1. 不要在基于范围的for循环中使用类型推导。如果我们显式地将元素类型指定为std::string_view，那么当数组稍后更新为std::string时，std::string元素将隐式转换为std::string_ view，这没有问题。如果数组被更新为其他不可转换的类型，编译器将出错，并且我们可以确定此时应该做什么。
2. 当您不想处理副本时，在基于范围的for循环中使用类型推导时，请始终使用 const auto& 而不是auto。通过引用而不是通过值访问元素的性能损失可能很小，并且如果元素类型后来被更改为复制成本高昂的类型，这将使我们在以后的道路上免受潜在的重大性能损失。

***
## 其它标准容器类型

基于范围的循环适用于各种数组类型，包括C样式数组、std::array、std::vector、链表、树和map。后面的还未讲到，因此如果您不知道这些是什么，请不要担心。请记住，基于范围的for循环提供了一种灵活而通用的方法来迭代，而不仅仅是std::vector:

```C++
#include <array>
#include <iostream>

int main()
{
    std::array fibonacci{ 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89 }; // 这里使用 std::array

    for (auto number : fibonacci)
    {
        std::cout << number << ' ';
    }

    std::cout << '\n';

    return 0;
}
```

***
## 获取当前元素的索引

基于范围的for循环不提供获取当前元素的数组索引的直接方法。这是因为基于范围的for循环可以迭代的许多结构（如std::list）不支持索引。

然而，由于基于范围的for循环总是向前迭代，并且不跳过元素，因此您始终可以声明（并操作）自己的计数器。然而，如果要这样做，您应该考虑是否最好使用原始for循环，而不是基于范围的for循环。

***
## 基于范围的反向循环（C++20）

基于范围的循环仅按向前顺序迭代。然而，在某些情况下，我们希望以相反的顺序遍历数组。在C++20之前，基于范围的for循环不能轻易用于此目的，必须采用其他解决方案。

然而，从C++20开始，您可以使用Ranges库的std::views::reverse功能来创建可以遍历的元素的反向视图：

```C++
#include <iostream>
#include <ranges> // C++20
#include <string_view>
#include <vector>

int main()
{
    std::vector<std::string_view> words{ "Alex", "Bobby", "Chad", "Dave" }; // 按字母表排序

    for (const auto& word : std::views::reverse(words)) // 创建一个反向的视图
        std::cout << word << ' ';

    std::cout << '\n';

    return 0;
}
```

这将打印：

```C++
Dave
Chad
Bobby
Alex
```

我们还没有介绍range库，所以现在认为这是一个有用的魔术。

***
