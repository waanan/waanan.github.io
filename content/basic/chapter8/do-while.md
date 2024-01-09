---
title: "Do while语句"
date: 2024-01-02T10:33:49+08:00
---

考虑这样一种情况，我们想向用户显示一个菜单，并要求他们进行选择——如果用户选择了无效的选项，则再次询问他们。显然，菜单和选择应该写在某种循环中（需要一直询问用户，直到他们输入有效的选项），但我们应该选择哪种循环？

由于while循环预先计算条件表达式，因此与先进行选择操作不方便适配。可以这样解决问题：

```C++
#include <iostream>

int main()
{
    // 选项需要在循环外定义, 以便稍后使用
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

    // 处理用户的选择
    // 例如可以使用switch语句

    std::cout << "You selected option #" << selection << '\n';

    return 0;
}
```

但这只是因为用于选择的初始值0不在有效值集合（1、2、3或4）中。如果0是有效的选择怎么办？那必须选择一个不同的初始值来表示“无效项”——在代码中引入魔数。

或者，添加一个新变量来跟踪用户是否输入有效值，如下所示：

```C++
#include <iostream>

int main()
{
    int selection { 0 };
    bool invalid { true }; // 新变量，来代表用户是否输入有效值

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

    // 处理用户的选择
    // 例如可以使用switch语句

    std::cout << "You selected option #" << selection << '\n';

    return 0;
}
```

虽然这避免了魔数，但它引入了一个新变量，只是为了确保循环运行一次，这增加了复杂性和额外错误的可能性。

***
## Do while语句

为了帮助解决上述问题，C++提供了do-while语句：

```C++
do
    语句; // 可以是单条语句，或代码块
while (条件表达式);
```

do-while语句是一个循环语句，其工作方式类似于while循环，但该语句至少执行一次。执行语句后，do-while循环检查条件。如果条件的计算结果为true，则执行路径跳回到do-while循环的顶部，并再次执行它。

下面是使用do-while改造上面程序的示例：

```C++
#include <iostream>

int main()
{
    // 选项需要在循环外定义, 以便稍后使用
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

    // 处理用户的选择
    // 例如可以使用switch语句

    std::cout << "You selected option #" << selection << '\n';

    return 0;
}
```

通过这种方式，我们避免了魔数和额外的变量。

在上面的例子中值得讨论的一件事是，selection变量必须在do代码块之外声明。如果selection变量要在do代码块内声明，则当代码块终止时，变量将被销毁，这发生在条件表达式求值之前。因此，selection变量必须在do代码块之外声明（即使它没有在后面的函数体中使用）。

在实践中，do-while语句并不常用。将条件放在循环的底部会模糊循环条件，可能导致错误。因此，许多开发人员建议完全避免do-while循环。这里采取更温和的立场，并主张在给予平等选择时，优先选择while循环而不是do-while。

***
