---
title: "goto语句"
date: 2024-01-02T10:33:49+08:00
---

我们将讨论的下一种控制流语句是无条件跳转。无条件跳转会导致执行跳转到代码中的另一个位置。术语“无条件”意味着跳转总是发生（不像if语句或switch语句，跳转仅根据表达式的结果有条件地发生）。

在C++中，无条件跳转是通过goto语句实现的，跳转到的位置是通过使用语句标签来标识的。下面是goto语句和语句标签的示例：

```C++
#include <iostream>
#include <cmath> // 引用 sqrt() 函数

int main()
{
    double x{};
tryAgain: // 这是标签语句
    std::cout << "Enter a non-negative number: "; 
    std::cin >> x;

    if (x < 0.0)
        goto tryAgain; // 这是goto语句

    std::cout << "The square root of " << x << " is " << std::sqrt(x) << '\n';
    return 0;
}
```

在此程序中，要求用户输入一个非负数。如果输入负数，程序将使用goto语句跳回tryAgain标签。然后再次要求用户输入新数字。这样，我们可以不断地要求用户输入，直到输入有效的内容。

下面是该程序的示例运行：

```C++
Enter a non-negative number: -4
Enter a non-negative number: 4
The square root of 4 is 2
```

***
## 标签语句具有函数作用域

字前面，我们讨论了两种作用域：局部（代码块）作用域和文件（全局）作用域。语句标签使用第三种作用域：函数作用域，这意味着标签在整个函数中都是可见的，甚至在其声明点之前也是可见的。goto语句及其对应的语句标签必须出现在同一函数中。

虽然上面的示例显示了向后跳转（到函数中的前一点）的goto语句，但goto语句也可以向前跳转：

```C++
#include <iostream>

void printCats(bool skip)
{
    if (skip)
        goto end; // jump forward; statement label 'end' is visible here due to it having function scope
    
    std::cout << "cats\n";
end:
    ; // statement labels must be associated with a statement
}

int main()
{
    printCats(true);  // jumps over the print statement and doesn't print anything
    printCats(false); // prints "cats"

    return 0;
}
```

这将打印：

除了向前跳，在上面的程序中还有几个有趣的事情值得一提。

首先，注意语句标签必须与语句相关联（因此它们的名称是：它们标记语句）。因为函数的末尾没有语句，所以我们必须使用null语句，因此我们有一个要标记的语句。其次，我们能够跳到标有end的语句，即使由于语句标签具有函数作用域，我们还没有声明end。不需要语句标签的前向声明。第三，值得明确指出的是，上面的程序格式很差——使用if语句跳过print语句比使用goto语句跳过它要好。

跳转有两个主要限制：只能在单个函数的边界内跳转（不能跳出一个函数跳入另一个函数），如果向前跳转，则不能在跳转到的位置仍在作用域内的任何变量的初始化上向前跳转。例如：

```C++
int main()
{
    goto skip;   // error: this jump is illegal because...
    int x { 5 }; // this initialized variable is still in scope at statement label 'skip'
skip:
    x += 3;      // what would this even evaluate to if x wasn't initialized?
    return 0;
}
```

请注意，您可以在变量初始化上向后跳转，当执行初始化时，变量将被重新初始化。

***
## 避免使用goto

在C++（以及其他现代高级语言）中，避免使用goto。著名计算机科学家埃德格·迪克斯特拉（Edsger W.Dijkstra）在一篇著名但难于阅读的论文《被认为有害的走到声明》（Go to Statement）中阐述了避免走到的理由。goto的主要问题是它允许程序员随意地在代码中跳跃。这创造了一种不那么亲切地被称为意大利面条代码的东西。意大利面条代码是具有类似于一碗意大利面条的执行路径的代码（所有的都是纠结和扭曲的），这使得遵循这种代码的逻辑极其困难。

正如Dijkstra有点幽默地说的那样，“程序员的质量是他们生成的程序中go-to语句密度的递减函数”。

几乎任何使用goto语句编写的代码都可以使用C++中的其他构造（如if语句和循环）更清楚地编写。一个值得注意的例外是，当您需要退出嵌套循环而不是整个函数时——在这种情况下，转到循环后面可能是最干净的解决方案。

{{< alert success >}}
**最佳实践**

避免goto语句（除非替代方案对代码可读性的影响明显）。

{{< /alert >}}

***
