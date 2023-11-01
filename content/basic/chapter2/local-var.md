---
title: "局部变量"
date: 2023-10-09T20:06:10+08:00
---

***
## 局部变量

在函数体中定义的变量称为局部变量（全局变量将在未来的章节中讨论）：

```C++
int add(int x, int y)
{
    int z{ x + y }; // z 是局部变量

    return z;
}
```

函数参数通常也被认为是局部变量：

```C++
int add(int x, int y) // 函数参数x y 是局部变量
{
    int z{ x + y };

    return z;
}
```

在本课中，我们将更详细地了解局部变量的一些属性。

***
## 生命周期

在对象和变量简介中，我们讨论了变量定义（如int x），在执行该语句时实例化（创建）变量。与此类似，函数参数在函数被调用时创建和初始化，函数体中的变量在定义点创建和初始化。

例如：

```C++
int add(int x, int y) // x y 在这里被创建和初始化
{ 
    int z{ x + y }; // z 在这里被创建和初始化

    return z;
}
```

自然，后续问题是，“那么实例化变量何时被销毁？”。局部变量在定义它的花括号内的末尾以与创建相反的顺序销毁（对于函数参数，在函数的末尾）。

```C++
int add(int x, int y)
{ 
    int z{ x + y };

    return z;
} // z, y, and x 在这里被销毁
```

就像一个人的一生被定义为他们出生和死亡之间一样，一个变量实例的生命周期被定义为它的创建和销毁之间的时间。请注意，变量的创建和销毁发生在程序运行时（称为运行时），而不是在编译时。因此，生命周期是一个运行时属性。

下面是一个稍微复杂的程序，演示名为x的变量的生命周期：

```C++
#include <iostream>

void doSomething()
{
    std::cout << "Hello!\n";
}

int main()
{
    int x{ 0 }; // x 生命周期从这里开始

    doSomething(); // 在函数调用时，x仍然存活

    return 0;
} // x 生命周期到这里结束
```

在上面的程序中，x的生命周期从定义点运行到函数main的末尾。这包括执行函数doSomething期间所花费的时间。

{{< alert success >}}
**对于高级读者**

以上关于创建、初始化和销毁的规则是保证。也就是说，必须在定义点创建和初始化对象，并在定义对象的花括号集末尾之前销毁对象（或者，对于函数参数，在函数末尾）。

实际上，C++规范为编译器提供了很大的灵活性，可以自行决定何时创建和销毁局部变量。为了优化代码，可以提前创建对象，也可以稍后销毁对象。通常，局部变量是在输入函数时创建的，而在退出函数时以相反的创建顺序销毁。在以后的课程中，当我们讨论调用堆栈时，我们将更详细地讨论这一点。

{{< /alert >}}

***
## 局部变量作用域

变量的作用域确定了在源代码中可以看到和使用变量的位置。当一个变量可以被看到和使用时，我们说它在作用域内。当一个变量看不见，不能被使用，我们说它超出作用范围。作用域是编译时属性，当变量不在作用域时尝试使用它将导致编译错误。

局部变量的作用域从变量定义点开始，到定义它的花括号集的末尾（或者对于函数参数，在函数的末尾）。这确保了变量不能在定义点之前使用（即使编译器选择在定义点前创建它们）。在一个函数中定义的局部变量的作用域也不在其他任何函数的范围内。

下面是一个程序，演示名为x的变量的作用域：

```C++
#include <iostream>

// x 不在 doSomething 函数内可见
void doSomething()
{
    std::cout << "Hello!\n";
}

int main()
{
    // 在这里x 不能被使用

    int x{ 0 }; // 从这里到函数末尾，x可以被使用

    doSomething();

    return 0;
} // 这里到了x 的作用域的末尾
```

在上面的程序中，变量x在定义点进入它的作用域，在main函数的末尾退出。请注意，变量x不在函数doSomething内可见，即使函数main调用了函数doSomething。

***
## 作用域与生命周期

作用域与生命周期，可能会让新程序员感到困惑。

变量不在作用域内，即无法在代码中访问它。在上面的示例中，x从其定义点到主函数的末尾都在作用域内。

生命周期，代表变量实例化后的实例的存活时间。局部变量实例的生命周期在其超出范围的点结束，因此局部变量在此时被销毁。

在生命周期内的变量，不一定在对应代码的作用域内。

注意，并不是所有类型的变量实例都在超出作用域时被销毁。我们将在以后的课程中看到这些示例。

***
## 另一个例子

这里有一个稍微复杂一些的例子。记住，生命周期是一个运行时属性，范围是一个编译时属性，因此尽管我们在同一个程序中讨论这两个属性，但它们在不同的点上强制执行。

```C++
#include <iostream>

int add(int x, int y) // x and y are created and enter scope here
{
    // x and y are visible/usable within this function only
    return x + y;
} // y and x go out of scope and are destroyed here

int main()
{
    int a{ 5 }; // a is created, initialized, and enters scope here
    int b{ 6 }; // b is created, initialized, and enters scope here

    // a and b are usable within this function only
    std::cout << add(a, b) << '\n'; // calls function add() with x=5 and y=6

    return 0;
} // b and a go out of scope and are destroyed here
```

参数x和y是在调用add函数时创建的，只能在函数add中看到/使用，并在add结束时销毁。变量a和b是在函数main中创建的，只能在函数main.中看到/使用，并在main的末尾销毁。

为了增强您对所有这些如何结合在一起的理解，让我们更详细地跟踪这个程序。按顺序发生以下情况：

1. 执行从main的顶部开始。
2. 创建主变量a并给定值5。
3. 创建主变量b并给定值6。
4. 使用参数值5和6调用函数add。
5. 创建add参数x和y，并分别用值5和6进行初始化。
6. 计算表达式x+y以产生值11。
7. add将值11复制回调用方main。
8. 添加参数y和x被破坏。
9. main将11打印到控制台。
10. main将0返回到操作系统。
11. 主要变量b和a被破坏。


我们完成了。

注意，如果函数add被调用两次，则参数x和y将被创建和销毁两次——每次调用一次。在具有许多函数和函数调用的程序中，变量经常被创建和销毁。

***
## 功能分离

在上面的例子中，很容易看出变量a和b是与x和y不同的变量。

现在考虑以下类似的程序：

```C++
#include <iostream>

int add(int x, int y) // add's x and y are created and enter scope here
{
    // add's x and y are visible/usable within this function only
    return x + y;
} // add's y and x go out of scope and are destroyed here

int main()
{
    int x{ 5 }; // main's x is created, initialized, and enters scope here
    int y{ 6 }; // main's y is created, initialized, and enters scope here

    // main's x and y are usable within this function only
    std::cout << add(x, y) << '\n'; // calls function add() with x=5 and y=6

    return 0;
} // main's y and x go out of scope and are destroyed here
```

在这个例子中，我们所做的就是将函数main中变量a和b的名称更改为x和y。这个程序的编译和运行是相同的，即使函数main和add都有名为x和y的变量。为什么这样做？

首先，我们需要认识到，即使函数main和add都有名为x和y的变量，但这些变量是不同的。函数main中的x和y与函数add中的x和y没有任何关系——它们碰巧共享相同的名称。

其次，当函数main内部时，名称x和y指的是main的局部范围变量x和y。这些变量只能在main内部看到（和使用）。类似地，在函数add中，名称x和y指的是函数参数x和y，它们只能在add中看到（和使用）。

简而言之，add和main都不知道另一个函数有同名的变量。因为作用域不重叠，所以编译器总是很清楚在任何时候引用了哪个x和y。

在未来的一章中，我们将更多地讨论局部范围和其他类型的范围。

{{< alert success >}}
**关键洞察力**

用于函数体中声明的函数参数或变量的名称仅在声明它们的函数中可见。这意味着可以在不考虑其他函数中变量的名称的情况下命名函数中的局部变量。这有助于保持功能的独立性。

{{< /alert >}}

***
## 定义局部变量的位置

在现代C++中，最佳实践是函数体中的局部变量应定义为接近其首次使用时的合理值：

```C++
#include <iostream>

int main()
{
	std::cout << "Enter an integer: ";
	int x{}; // x defined here
	std::cin >> x; // and used here

	std::cout << "Enter another integer: ";
	int y{}; // y defined here
	std::cin >> y; // and used here

	int sum{ x + y }; // sum can be initialized with intended value
	std::cout << "The sum is: " << sum << '\n';

	return 0;
}
```

在上面的示例中，每个变量都是在首次使用之前定义的。没有必要对此严格要求——如果您更喜欢交换第5行和第6行，那没关系。

{{< alert success >}}
**最佳做法**

将局部变量定义为尽可能接近其首次使用。

{{< /alert >}}

{{< alert success >}}
**作为旁白…**

由于较旧、更原始的编译器的限制，C语言过去要求在函数的顶部定义所有局部变量。使用该样式的等效C++程序如下所示：

```C++
#include <iostream>

int main()
{
	int x{}, y{}, sum{}; // how are these used?

	std::cout << "Enter an integer: ";
	std::cin >> x;

	std::cout << "Enter another integer: ";
	std::cin >> y;

	sum = x + y;
	std::cout << "The sum is: " << sum << '\n';

	return 0;
}
```

由于以下几个原因，此样式不是最佳的：

1. 在定义时，这些变量的预期用途并不明显。您必须扫描整个函数，以确定在何处以及如何使用每个函数。
2. 函数顶部可能没有预期的初始化值（例如，我们无法将总和初始化为其预期值，因为我们还不知道x和y的值）。
3. 变量的初始值设定项和它的首次使用之间可能有许多行。如果我们不记得它是用什么值初始化的，我们将不得不向后滚动到函数的顶部，这会分散注意力。


在C99语言标准中取消了此限制。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter2/func-arg/" next="/" >}}
2.3 函数参数简介
<--->
主页
{{< /prevnext >}}
