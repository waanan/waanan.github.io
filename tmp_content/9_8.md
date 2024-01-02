---
title: "Do while语句"
date: 2024-01-02T10:33:49+08:00
---

考虑这样一种情况，我们想向用户显示一个菜单，并要求他们进行选择——如果用户选择了无效的选择，则再次询问他们。显然，菜单和选择应该进入某种循环中（因此我们可以一直询问用户，直到他们输入有效的输入），但我们应该选择哪种循环？

由于while循环预先评估条件，因此这是一个尴尬的选择。我们可以这样解决问题：

```C++
#include <iostream>

int main()
{
    // selection must be declared outside while-loop, so we can use it later
    int selection{ 0 };

    while (selection != 1 && selection != 2 &&
        selection != 3 && selection != 4)
    {
        std::cout << "Please make a selection: \n";
        std::cout << "1) Addition\n";
        std::cout << "2) Subtraction\n";
        std::cout << "3) Multiplication\n";
        std::cout << "4) Division\n";
        std::cin >> selection;
    }

    // do something with selection here
    // such as a switch statement

    std::cout << "You selected option #" << selection << '\n';

    return 0;
}
```

但这只是因为用于选择的初始值0不在有效值集（1、2、3或4）中。如果0是有效的选择怎么办？我们必须选择一个不同的初始化器来表示“无效”——现在我们在代码中引入了幻数（5.2——文字）。

相反，我们可以添加一个新变量来跟踪有效性，如下所示：

```C++
#include <iostream>

int main()
{
    int selection { 0 };
    bool invalid { true }; // new variable just to gate the loop

    while (invalid)
    {
        std::cout << "Please make a selection: \n";
        std::cout << "1) Addition\n";
        std::cout << "2) Subtraction\n";
        std::cout << "3) Multiplication\n";
        std::cout << "4) Division\n";

        std::cin >> selection;
        invalid = (selection != 1 && selection != 2 &&
            selection != 3 && selection != 4);
    }

    // do something with selection here
    // such as a switch statement

    std::cout << "You selected option #" << selection << '\n';

    return 0;
}
```

虽然这避免了幻数，但它引入了一个新变量，只是为了确保循环运行一次，这增加了复杂性和额外错误的可能性。

***
## Do while语句

为了帮助解决上述问题，C++提供了do-while语句：

do-while语句是一个循环构造，其工作方式类似于while循环，但该语句始终至少执行一次。执行语句后，do-while循环检查条件。如果条件的计算结果为true，则执行路径跳回到do-while循环的顶部，并再次执行它。

下面是上面使用do-while循环而不是while环的示例：

```C++
#include <iostream>

int main()
{
    // selection must be declared outside of the do-while-loop, so we can use it later
    int selection{};

    do
    {
        std::cout << "Please make a selection: \n";
        std::cout << "1) Addition\n";
        std::cout << "2) Subtraction\n";
        std::cout << "3) Multiplication\n";
        std::cout << "4) Division\n";
        std::cin >> selection;
    }
    while (selection != 1 && selection != 2 &&
        selection != 3 && selection != 4);

    // do something with selection here
    // such as a switch statement

    std::cout << "You selected option #" << selection << '\n';

    return 0;
}
```

通过这种方式，我们避免了幻数和额外的变量。

在上面的例子中值得讨论的一件事是，选择变量必须在do块之外声明。如果选择变量要在do块内声明，则当do块终止时，它将被销毁，这发生在条件求值之前。但我们需要while条件中的变量——因此，选择变量必须在do块之外声明（即使它后来没有在函数体中使用）。

在实践中，do-while循环并不常用。将条件放在循环的底部会模糊循环条件，这可能导致错误。因此，许多开发人员建议完全避免do-while循环。我们将采取更温和的立场，并主张在给予平等选择时，优先选择while循环而不是do。

{{< alert success >}}
**最佳做法**

当给予平等的选择时，循环优先于do。

{{< /alert >}}

