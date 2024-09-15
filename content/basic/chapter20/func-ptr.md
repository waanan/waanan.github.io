---
title: "函数指针"
date: 2024-08-20T10:49:32+08:00
---

指针是一个保存另一个变量地址的变量。函数指针类似，只是它们不是指向变量，而是指向函数！

考虑以下函数：

```C++
int foo()
{
    return 5;
}
```

标识符foo是函数的名称。但函数是什么类型的呢？函数有自己的左值函数类型——在本例中，是一种返回整数而不带参数的函数类型。就像变量一样，函数存在于内存中的指定地址。

调用函数时（通过「（）」运算符），跳转到被调用函数的地址开始执行：

```C++
int foo() // 假设foo的代码开始于 0x002717f0
{
    return 5;
}

int main()
{
    foo(); // 跳转到 0x002717f0 执行

    return 0;
}
```

在编程生涯的某个时刻（如果您还没有），您可能会犯一个简单的错误：

```C++
#include <iostream>

int foo() // 假设foo的代码开始于 0x002717f0
{
    return 5;
}

int main()
{
    std::cout << foo << '\n'; // 想要调用 foo(), 但却打印了它的地址!

    return 0;
}
```

我们没有调用函数foo()并打印返回值，而是无意中将函数foo直接发送到std::cout。在这种情况下会发生什么？

运算符<<不知道如何输出函数指针（因为可能有无限多的函数指针）。标准规定，在这种情况下，foo应该转换为bool（操作符<<知道如何打印）。由于foo的函数指针是非空指针，因此它的计算结果应该始终为true。因此，应打印：

```C++
1
```

就像可以声明指向普通变量的非常量指针一样，也可以声明指向函数的非常量指针。在本课的其余部分中，我们将研究这些函数指针及其用法。函数指针是一个相当高级的主题，仅寻找C++基础知识的人可以安全地跳过本课的其余部分。

***
## 指向函数的指针

创建非const函数指针的语法是C++中最丑陋的语法之一：

```C++
// fcnPtr 是一个指针，指向无参数返回int的函数
int (*fcnPtr)();
```

在上面的代码片段中，fcnPtr是指向没有参数并返回整数的函数的指针。fcnPtr可以指向与此类型匹配的任何函数。

出于优先级原因，\*fcnPtr周围的括号是必要的，因为「int* fcnPatr();」将被解释为名为fcnPtra的函数的前向声明，该函数不接受参数，并返回指向整数的指针。

要制作const函数指针，const放在星号后面：

```C++
int (*const fcnPtr)();
```

如果将const放在int之前，则表示所指向的函数将返回const int。

{{< alert success >}}
**提示**

函数指针语法可能很难理解。以下文章演示了一种解析此类声明的方法：

1. https://c-faq.com/decl/spiral.anderson.html
2. https://web.archive.org/web/20110818081319/http://ieng9.ucsd.edu/~cs30x/rt_lt.rule.html

{{< /alert >}}

***
## 将函数分配给函数指针

函数指针可以用函数初始化（并且可以为非const函数指针分配函数）。与变量指针一样，我们也可以使用&foo来获得指向foo的函数指针。

```C++
int foo()
{
    return 5;
}

int goo()
{
    return 6;
}

int main()
{
    int (*fcnPtr)(){ &foo }; // fcnPtr 指向 foo
    fcnPtr = &goo; // fcnPtr 现在指向 goo

    return 0;
}
```

一个常见的错误是这样做：

```C++
fcnPtr = goo();
```

这试图将函数goo()调用的返回值（类型为int）分配给fcnPtr（需要类型为int(*) ()的值），这不是我们想要的。我们希望为fcnPtr分配函数goo的地址，而不是函数goo()的返回值。因此不需要括号。

请注意，函数指针的类型（参数和返回类型）必须与函数的类型匹配。下面是一些这样的例子：

```C++
// 函数原型
int foo();
double goo();
int hoo(int x);

// 函数指针初始化
int (*fcnPtr1)(){ &foo };    // okay
int (*fcnPtr2)(){ &goo };    // 错误 -- 返回类型不匹配!
double (*fcnPtr4)(){ &goo }; // okay
fcnPtr1 = &hoo;              // 错误 -- fcnPtr1 没有参数, 但 hoo() 有
int (*fcnPtr3)(int){ &hoo }; // okay
```

与基本类型不同，如果需要，C++将隐式地将函数转换为函数指针（因此不需要使用 操作符& 来获取函数的地址）。然而，函数指针不能转换为void指针，反之亦然（尽管某些编译器（如Visual Studio）可能允许这样做）。

```C++
	// 函数原型
	int foo();

	// 函数指针初始化
	int (*fcnPtr5)() { foo }; // okay, foo 隐式转换为函数指针
	void* vPtr { foo };       // not okay, 但某些编译器允许
```

函数指针也可以初始化或分配值nullptr:

```C++
int (*fcnptr)() { nullptr }; // okay
```

***
## 使用函数指针调用函数

使用函数指针可以做的另一件主要事情是使用它来实际调用函数。有两种方法可以做到这一点。第一种是通过显式解引用：

```C++
int foo(int x)
{
    return x;
}

int main()
{
    int (*fcnPtr)(int){ &foo }; // 使用foo初始化fcnPtr
    (*fcnPtr)(5); // 通过 fcnPtr 调用函数 foo(5)

    return 0;
}
```

第二种方法是通过隐式解引用：

```C++
int foo(int x)
{
    return x;
}

int main()
{
    int (*fcnPtr)(int){ &foo }; // 使用foo初始化fcnPtr
    fcnPtr(5); // 通过 fcnPtr 调用函数 foo(5)

    return 0;
}
```

正如您所看到的，隐式解引用方法看起来就像普通函数调用——这是您所期望的，因为普通函数名无论如何都是函数的指针！然而，一些较旧的编译器不支持隐式解引用函数指针，但所有现代编译器都应该支持。

还要注意，因为函数指针可以设置为nullptr，所以最好在调用函数指针之前断言或条件测试函数指针是否为nullptr。就像普通指针一样，解引用null函数指针会导致未定义的行为。

```C++
int foo(int x)
{
    return x;
}

int main()
{
    int (*fcnPtr)(int){ &foo }; // 使用foo初始化fcnPtr
    if (fcnPtr) // 确保 fcnPtr 不为空指针    
        fcnPtr(5); // 否则可能导致未定义的行为

    return 0;
}
```

***
## 默认参数不适用于通过函数指针调用的函数

当编译器遇到具有默认参数的函数调用时，它重写函数调用以传递默认参数。这个过程发生在编译时，因此只能应用于可以在编译时解析的函数。

然而，当通过函数指针调用函数时，函数调用在运行时解析。在这种情况下，不会重写函数调用以传递默认参数。

这意味着我们可以使用函数指针来消除由于默认参数而不明确的函数调用的歧义。在下面的示例中，我们展示了两种方法：

```C++
#include <iostream>

void print(int x)
{
    std::cout << "print(int)\n";
}

void print(int x, int y = 10)
{
    std::cout << "print(int, int)\n";
}

int main()
{
//    print(1); // 有歧义的函数调用

    // 拆分的写法
    using vnptr = void(*)(int); // 定义函数类型 void(int) 的别名
    vnptr pi { print }; // 使用 print 初始化 pi 函数指针
    pi(1); // 通过函数指针调用 print(int)

    // 简洁的写法
    static_cast<void(*)(int)>(print)(1); // 调用只有一个参数的 void(int)
    
    return 0;
}
```

{{< alert success >}}
**关键点**

由于解析发生在运行时，因此当通过函数指针调用函数时，不会解析默认参数。

{{< /alert >}}

***
## 将函数作为参数传递给其他函数

使用函数指针最有用的事情之一是将函数作为参数传递给另一个函数。用作另一个函数的参数的函数有时称为回调函数。

考虑这样一种情况：您正在编写一个函数来执行任务（例如对数组进行排序），但您希望用户能够定义如何执行该任务的特定部分（例如数组是按升序还是降序排序）。让我们更仔细地看一下这个专门应用于排序的问题，作为一个可以推广到其他类似问题的例子。

许多基于比较的排序算法都在类似的概念上工作：排序算法迭代数字列表，对数字对进行比较，并根据这些比较的结果对数字重新排序。因此，通过改变比较方式，我们可以改变算法排序的方式，而不会影响其余的排序代码。

下面是之前中的选择排序例程：

```C++
#include <utility> // for std::swap

void SelectionSort(int* array, int size)
{
    if (!array)
        return;

    // 遍历数组的每个元素
    for (int startIndex{ 0 }; startIndex < (size - 1); ++startIndex)
    {
        // smallestIndex 记录遍历时遇到的最小元素的下标
        int smallestIndex{ startIndex };
 
        // 在剩余数组里寻找更小的元素 (从 startIndex+1 开始)
        for (int currentIndex{ startIndex + 1 }; currentIndex < size; ++currentIndex)
        {
            // 如果当前元素比之前记录的更小
            if (array[smallestIndex] > array[currentIndex]) // 在这里进行比较
            {
                // 那么它就是我们需要的最小的
                smallestIndex = currentIndex;
            }
        }
 
        // 将最小的元素与开时位置时的元素互换
        std::swap(array[startIndex], array[smallestIndex]);
    }
}
```

让我们将该比较的逻辑替换为一个函数来进行比较。因为我们的比较函数将比较两个整数，并返回一个布尔值来指示是否应该交换元素，所以它将如下所示：

```C++
bool ascending(int x, int y)
{
    return x > y; // 如果第一个元素比第二个元素大，那么就需要进行交换
}
```

下面是使用ascending()函数进行比较的选择排序示例：

```C++
#include <utility> // for std::swap

void SelectionSort(int* array, int size)
{
    if (!array)
        return;

    // 遍历数组的每个元素
    for (int startIndex{ 0 }; startIndex < (size - 1); ++startIndex)
    {
        // smallestIndex 记录遍历时遇到的最小元素的下标
        int smallestIndex{ startIndex };
 
        // 在剩余数组里寻找更小的元素 (从 startIndex+1 开始)
        for (int currentIndex{ startIndex + 1 }; currentIndex < size; ++currentIndex)
        {
            //  如果当前元素比之前记录的更小
            if (ascending(array[smallestIndex], array[currentIndex])) // 在这里进行比较
            {
                // 那么它就是我们需要的最小的
                smallestIndex = currentIndex;
            }
        }
 
        // 将最小的元素与开时位置时的元素互换
        std::swap(array[startIndex], array[smallestIndex]);
    }
}
```

现在，为了让调用方决定如何进行排序，而不是使用我们自己的硬编码比较函数，我们将允许调用方提供自己的排序函数！这是通过函数指针完成的。

由于调用方的比较函数将比较两个整数并返回布尔值，因此指向此类函数的指针将如下所示：

```C++
bool (*comparisonFcn)(int, int);
```

因此，我们将允许调用者向排序程序传递一个指向其所需比较函数的指针作为第三个参数，然后使用调用者的函数进行比较。

下面是使用函数指针参数进行用户定义的比较的选择排序的完整示例，以及如何调用它的示例：

```C++
#include <utility> // for std::swap
#include <iostream>

// 注意用户定义的比较函数时第三个参数
void selectionSort(int* array, int size, bool (*comparisonFcn)(int, int))
{
    if (!array || !comparisonFcn)
        return;

    // 遍历数组的每个元素
    for (int startIndex{ 0 }; startIndex < (size - 1); ++startIndex)
    {
        // bestIndex 记录遇到的最大/最小的元素的位置
        int bestIndex{ startIndex };
 
        // 在剩余数组里寻找更大/更小的元素 (从 startIndex+1 开始)
        for (int currentIndex{ startIndex + 1 }; currentIndex < size; ++currentIndex)
        {
            // 如果当前元素比之前记录的更大/更小
            if (comparisonFcn(array[bestIndex], array[currentIndex])) // 在这里进行比较
            {
                // 那么它就是我们需要的最大/最小的
                bestIndex = currentIndex;
            }
        }
 
        // 将最大/最小的元素与开时位置时的元素互换
        std::swap(array[startIndex], array[bestIndex]);
    }
}

// 这是按升序进行比较的函数
// (与前面定义的 ascending() 一样)
bool ascending(int x, int y)
{
    return x > y; //  如果第一个元素比第二个元素大，那么就需要进行交换
}

// 这是按降序进行比较的函数
bool descending(int x, int y)
{
    return x < y; //  如果第一个元素比第二个元素小，那么就需要进行交换
}

// 这个函数打印数组里的元素
void printArray(int* array, int size)
{
    if (!array)
        return;

    for (int index{ 0 }; index < size; ++index)
    {
        std::cout << array[index] << ' ';
    }
    
    std::cout << '\n';
}

int main()
{
    int array[9]{ 3, 7, 9, 5, 6, 1, 8, 2, 4 };

    // 使用 descending() 按降序进行排序
    selectionSort(array, 9, descending);
    printArray(array, 9);

    // 使用 ascending() 按升序进行排序
    selectionSort(array, 9, ascending);
    printArray(array, 9);

    return 0;
}
```

该程序生成结果：

```C++
9 8 7 6 5 4 3 2 1
1 2 3 4 5 6 7 8 9
```

这很酷吧。函数的行为，依据调用者提供的函数指针而改变。

调用者甚至可以定义自己的“奇怪”比较函数：

```C++
bool evensFirst(int x, int y)
{
	// 如果 x 是偶数 y 是奇数, x 排在前面 (无需交换)
	if ((x % 2 == 0) && !(y % 2 == 0))
		return false;
 
	// 如果 x 是奇数 y 是偶数, y 排在前面 (需要交换)
	if (!(x % 2 == 0) && (y % 2 == 0))
		return true;

        // 否则按照升序排序
	return ascending(x, y);
}

int main()
{
    int array[9]{ 3, 7, 9, 5, 6, 1, 8, 2, 4 };

    selectionSort(array, 9, evensFirst);
    printArray(array, 9);

    return 0;
}
```

上面的代码段生成以下结果：

```C++
2 4 6 8 1 3 5 7 9
```

如您所见，在此上下文中使用函数指针提供了一种很好的方法，允许调用方将自己的函数“挂钩”到您以前编写和测试的东西中，这有助于促进代码重用！以前，如果希望按降序对一个数组进行排序，并按升序对另一个数组排序，则需要多个版本的排序函数。现在，您可以有一个版本，可以按调用方希望的任何方式进行排序！

注意：如果函数参数是函数类型，则它将被转换为指向函数类型的指针。这意味着：

```C++
void selectionSort(int* array, int size, bool (*comparisonFcn)(int, int))
```

可以等效为：

```C++
void selectionSort(int* array, int size, bool comparisonFcn(int, int))
```

这仅适用于函数参数，因此用途有限。在非函数参数的位置，后者被解释为向前声明：

```C++
    bool (*ptr)(int, int); // 定义函数指针 ptr
    bool fcn(int, int);    // 函数 fcn 的前向声明
```

***
## 提供默认函数

如果您要允许调用者将函数作为参数传入，那么为调用者提供一些标准函数以方便他们使用通常是有用的。例如，在上面的选择排序示例中，提供ascending()和descending()函数以及selectionSort()函数将使调用者的工作变得更轻松，因为他们不必每次想使用它们时都重写ascenting()或descending()。

您甚至可以将其中一个设置为默认参数：

```C++
// 默认按照升序排序
void selectionSort(int* array, int size, bool (*comparisonFcn)(int, int) = ascending);
```

在这种情况下，只要用户正常调用selectionSort（而不是通过函数指针），comparionFcn参数将默认为ascending。您需要确保在这之前声明ascending函数。

***
## 使用类型别名使函数指针更漂亮

让我们面对它——函数指针的语法很难看。然而，类型别名可以用于使函数的指针看起来更像正常变量：

```C++
using ValidateFunction = bool(*)(int, int);
```

这定义了一个名为“ValidateFunction”的类型别名，它是一个指向接受两个int并返回布尔值的函数的指针。

我们可以修改函数的定义：

```C++
bool validate(int x, int y, bool (*fcnPtr)(int, int)); // 丑陋
```

改为：

```C++
bool validate(int x, int y, ValidateFunction pfcn) // 干净
```

***
## 使用std::function

定义和存储函数指针的另一种方法是使用std::function，它是标准库\<functional\>头文件的一部分。要使用此方法定义函数指针，请声明一个std::function对象，如下所示：

```C++
#include <functional>
bool validate(int x, int y, std::function<bool(int, int)> fcn); // std::function 是一个接收两个int返回一个bool的函数
```

如您所见，返回类型和参数都放在尖括号内，参数放在括号内。如果没有参数，括号可以保留为空。

使用std::function更新前面的示例

```C++
#include <functional>
#include <iostream>

int foo()
{
    return 5;
}

int goo()
{
    return 6;
}

int main()
{
    std::function<int()> fcnPtr{ &foo }; // 声明函数指针
    fcnPtr = &goo; // fcnPtr 现在指向函数 goo
    std::cout << fcnPtr() << '\n'; // 和之前调用方式一致

    std::function fcnPtr2{ &foo }; // 也可以使用 CTAD 去自动推导类型

    return 0;
}
```

类型别名或std::function有助于提高可读性：

```C++
using ValidateFunctionRaw = bool(*)(int, int); // 函数指针类型的别名
using ValidateFunction = std::function<bool(int, int)>; // std::function的类型别名
```

还要注意，std::function只允许通过隐式解引用（例如，fcnPtr()）调用函数，而不允许通过显式解引用调用函数（例如，(*fcnPtra)() ）。

定义类型别名时，必须显式指定模板参数。在这种情况下，我们不能使用CTAD，因为没有初始化值可以从中推导模板参数。

***
## 函数指针的类型推导

就像auto关键字可以用于推断正常变量的类型一样，auto关键字也可以推断函数指针的类型。

```C++
#include <iostream>

int foo(int x)
{
	return x;
}

int main()
{
	auto fcnPtr{ &foo };
	std::cout << fcnPtr(5) << '\n';

	return 0;
}
```

这与您期望的完全一样，并且语法非常干净。当然，缺点是关于函数的参数类型和返回类型的所有细节都是隐藏的，因此在调用函数或使用其返回值时更容易出错。

***
## 结论

函数指针主要在希望将函数存储在数组（或其他结构）中，或者需要将函数传递给另一个函数时有用。由于声明函数指针的原始语法难看且容易出错，因此建议使用std::function。在函数指针类型仅使用一次的地方（例如，单个参数或返回值），可以直接使用std::function。在多次使用函数指针类型的地方，最好选择std::function的类型别名（以防止重复输入）。

***
