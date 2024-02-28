---
title: "通过指针传递函数参数（第2部分）"
date: 2024-02-19T14:35:47+08:00
---

## 传递地址的“可选”参数

传递地址的一个更常见的用法是允许函数接受“可选”参数：

```C++
#include <iostream>
#include <string>

void greet(std::string* name=nullptr)
{
    std::cout << "Hello ";
    std::cout << (name ? *name : "guest") << '\n';
}

int main()
{
    greet(); // 这里还不知道用户名

    std::string joe{ "Joe" };
    greet(&joe); // 现在知道用户是Joe

    return 0;
}
```

此示例打印：

```C++
Hello guest
Hello Joe
```

在这个程序中，greet()函数有一个由地址传递的参数，默认为nullptr。在main()中，调用该函数两次。第一次调用时，不知道用户是谁，因此在没有参数的情况下调用greet()。name参数默认为nullptr，greet函数打印“guest”。对于第二个调用，现在有一个有效的用户，因此调用greet(&joe)。name参数接收joe的地址，并可以使用它来打印名称“joe”。

然而，在许多情况下，函数重载是实现相同结果的更好的替代方法：

```C++
#include <iostream>
#include <string>
#include <string_view>

void greet(std::string_view name)
{
    std::cout << "Hello " << name << '\n';
}

void greet()
{
    greet("guest");
}

int main()
{
    greet(); // 这里还不知道用户名

    std::string joe{ "Joe" };
    greet(joe); // 现在知道用户是Joe

    return 0;
}
```

这有许多优点：不再需要担心解引用空指针，并且如果需要，可以传入字符串字面值。

***
## 更改指针参数指向的内容

当向函数传递地址时，该地址将复制到指针参数中（这很好，因为复制地址很快）。现在考虑以下程序：

```C++
#include <iostream>

// ptr被赋值但未被使用，[[maybe_unused]]让编译器不要告警
void nullify([[maybe_unused]] int* ptr2) 
{
    ptr2 = nullptr; // 将ptr指向空指针
}

int main()
{
    int x{ 5 };
    int* ptr{ &x }; // ptr 指向 x

    std::cout << "ptr is " << (ptr ? "non-null\n" : "null\n");

    nullify(ptr);

    std::cout << "ptr is " << (ptr ? "non-null\n" : "null\n");
    return 0;
}
```

该程序打印：

```C++
ptr is non-null
ptr is non-null
```

正如所看到的，更改指针参数ptr2存储的地址不会影响原来指针ptr所保存的地址（ptr仍然指向x）。当调用函数nullify()时，ptr2接收传入地址的副本（在本例中，是ptr持有的地址，即x的地址）。当函数更改ptr2指向的内容时，这仅影响ptr2持有的副本。

那么，如果想允许函数改变原来的指针ptr所指向的地址，该怎么办？

***
## 通过引用传递指针？

就像可以通过引用传递普通变量一样，也可以通过引用来传递指针。下面是与上面类似的程序，ptr2更改为对指针的引用：

```C++
#include <iostream>

void nullify(int*& refptr) // refptr 现在是指针的引用
{
    refptr = nullptr; // 传入的指针，指向nullptr
}

int main()
{
    int x{ 5 };
    int* ptr{ &x }; // ptr 指向 x

    std::cout << "ptr is " << (ptr ? "non-null\n" : "null\n");

    nullify(ptr);

    std::cout << "ptr is " << (ptr ? "non-null\n" : "null\n");
    return 0;
}
```

该程序打印：

```C++
ptr is non-null
ptr is null
```

因为refptr现在是指针的引用，所以当ptr传递给函数时，refptr绑定到ptr。这意味着对refptr的任何更改都是对ptr的更改。

{{< alert success >}}
**旁白**

由于对指针的引用相当少见，因此很容易混淆语法（它是int*&还是int&*？）。好消息是，后一种写法，编译器将报错，因为您不能有指向引用的指针（因为指针必须包含对象的地址，而引用不是对象）。

{{< /alert >}}

***
## 为什么不再推荐使用0或NULL表示空指针（可选）

0可以解释为整数，也可以解释为空指针。具体哪一个可能是模棱两可的——在一些情况下，编译器可能会假设我们是指一个，而我们是本意是另一个，程序可能会因此产生预期外的执行结果。

语言标准未定义预处理器宏NULL的定义。它可以定义为0、0L、((void*)0) 或完全其它的东西。

在函数重载简介中，讨论了函数可以重载（多个函数可以具有相同的名称，只要它们可以通过参数的数量或类型来区分）。编译器通过实际函数调用时传入的值来区分具体调用哪个函数。

使用0或NULL时，这可能会导致问题：

```C++
#include <iostream>
#include <cstddef> // for NULL

void print(int x) // 这个函数接收int参数
{
	std::cout << "print(int): " << x << '\n';
}

void print(int* ptr) // 这个函数接收int指针
{
	std::cout << "print(int*): " << (ptr ? "non-null\n" : "null\n");
}

int main()
{
	int x{ 5 };
	int* ptr{ &x };

	print(ptr);  // 永远调用 print(int*) 因为ptr是类型 int*
	print(0);    // 永远调用 print(int) 因为0是int (希望这是我们预期的行为)

	print(NULL); // 这个语句可能有如下的行为:
	// 调用 print(int) (Visual Studio 上)
	// 调用 print(int*)
	// 编译报错，无法明确匹配函数 (gcc 与 Clang 上)

	print(nullptr); // 永远调用 print(int*)

	return 0;
}
```

在作者的计算机上（使用Visual Studio），将打印：

```C++
print(int*): non-null
print(int): 0
print(int): 0
print(int*): null
```

当将整数值0作为参数传递时，编译器会选择print(int)而不是print(int*)。当我们打算用NULL作为空指针参数调用print(int*)时，这可能有意外的结果。

在NULL被定义为值0的情况下，print(NULL)将调用print(int)，而不是像您可能期望的调用print(int*)。在NULL未定义为0的情况下，可能会导致其他行为，如调用print(int*)或编译错误。

使用nullptr可以消除这种模糊性（它总是调用print(int*)），因为nullptr只匹配指针类型。

***
## std::nullptr_t（可选）

由于nullptr可以与函数重载中的整数值区分开来，因此它必须具有不同的类型。那么nullptr是什么类型的呢？答案是，nullptr具有类型std::nullptr_t（在头文件 cstddef 中定义）。std::nullptr_t只能保存一个值：nullptr！虽然这看起来有点傻，但它在一种情况下是有用的。如果希望编写只接受nullptr参数的函数，可以将该参数类型设置为std::nullptr_t。

```C++
#include <iostream>
#include <cstddef> // for std::nullptr_t

void print(std::nullptr_t)
{
    std::cout << "in print(std::nullptr_t)\n";
}

void print(int*)
{
    std::cout << "in print(int*)\n";
}

int main()
{
    print(nullptr); // 调用 print(std::nullptr_t)

    int x { 5 };
    int* ptr { &x };

    print(ptr); // 调用 print(int*)

    ptr = nullptr;
    print(ptr); // 调用 print(int*) (因为 ptr 类型是 int*)

    return 0;
}
```

在上面的示例中，函数调用print(nullptr)解析为函数print(std::nullptr_t)而不是 print(int*)，因为它不需要转换。

一种可能有点令人困惑的情况是，当ptr持有nullptr值时调用print(ptr)。记住，函数重载匹配的是类型，而不是值，并且ptr的类型是int*。因此，print(int*)将被匹配。在这种情况下，不会考虑print(std::nullptr_t)，因为指针类型不会隐式转换为std::nullptr_t。

您可能永远不需要使用这个，但知道这一点很好，以防万一。

***
## 也许所有的参数都只是传递值

既然您已经理解了通过引用传递、地址和值之间的基本区别，那么让我们来了解一下简化主义者。：）

虽然编译器通常可以完全优化引用，但在某些情况下，这是不可能的，并且实际上需要引用。引用通常由编译器使用指针来实现。这意味着在幕后，按引用传递本质上只是一个传递指针（对引用的访问执行隐式指针解引用）。

在上一课中，提到了传递地址只是将地址从调用者复制到被调用的函数——它只是按值传递地址。

因此，我们可以得出结论，C++确实按值传递所有内容！传递地址（和引用）的能力在于，可以解引用传递的地址来更改参数指向的对象，这是使用普通值作为参数所不能做到的！

***
