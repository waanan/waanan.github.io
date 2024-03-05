---
title: "通过指针传递函数参数"
date: 2024-02-19T14:35:47+08:00
---

在前面的课程中，介绍了将参数传递给函数的两种不同方法：通过值传递和通过引用传递。

下面是一个示例程序，它显示了通过值和引用传递的std::string对象：

```C++
#include <iostream>
#include <string>

void printByValue(std::string val) // 函数参数是 str 的拷贝
{
    std::cout << val << '\n'; // 通过拷贝打印
}

void printByReference(const std::string& ref) // 函数参数是 str 的引用
{
    std::cout << ref << '\n'; // 通过引用打印
}

int main()
{
    std::string str{ "Hello, world!" };
    
    printByValue(str); // 通过值传递str的拷贝
    printByReference(str); // 通过引用传递str，不会制作副本

    return 0;
}
```

当通过值传递str时，函数参数val接收str的副本。所以对val的任何更改都是对副本而不是原始值的更改。

当通过引用传递str时，引用参数ref绑定到实际对象。这样可以避免复制。因为引用参数是常量，所以不允许更改ref。但如果ref是非常量的，则对ref所做的任何更改都将同步更改str。

在这两种情况下，调用者都提供要作为参数传递给函数调用的实际对象（str）。

***
## 通过地址传递函数参数

C++提供了第三种将值传递给函数的方法，通过传递指针。调用方提供对象的地址（通过指针），而不是提供对象作为参数。该指针（保存对象的地址）被复制到被调用函数的指针参数中（该函数现在也保存对象的位置）。然后，该函数可以解引用该指针，以通过其地址访问被传递的对象。

下面是上述程序的另一个版本，添加了一个传递指针的函数：

```C++
#include <iostream>
#include <string>

void printByValue(std::string val) // 函数参数是 str 的拷贝
{
    std::cout << val << '\n'; // 通过拷贝打印
}

void printByReference(const std::string& ref) // 函数参数是 str 的引用
{
    std::cout << ref << '\n'; // 通过引用打印
}

void printByAddress(const std::string* ptr) // 函数参数是 str 的地址
{
    std::cout << *ptr << '\n'; // 通过解引用指针打印
}

int main()
{
    std::string str{ "Hello, world!" };
    
    printByValue(str); // 通过值传递str的拷贝
    printByReference(str); // 通过引用传递str，不会制作副本
    printByAddress(&str); // 通过地址传递str，不会制作副本

    return 0;
}
```

请注意这三个版本的相似性。让我们更详细地研究传递地址版本。

首先，因为我们希望printByAddress()函数使用传递地址，所以将函数参数设置为一个名为ptr的指针。由于printByAddress()将以只读方式使用ptr，因此ptr是指向常量值的指针。

```C++
void printByAddress(const std::string* ptr)
{
    std::cout << *ptr << '\n'; // 通过解引用指针打印
}
```

在printByAddress()函数中，我们解引用ptr参数以访问所指向对象的值。

其次，当调用函数时，不能只传入str对象——需要传入str的地址。最简单的方法是使用取址操作符（&）获取保存str地址的指针：

```C++
printByAddress(&str); // 使用取址操作符 (&) 获取保存str地址的指针
```

执行此调用时，&str将创建一个指针，保存str的地址。然后，将该指针复制到函数参数ptr中。因为ptr现在保存str的地址，所以当函数解引用ptr时，它将获得str的值，该函数将该值打印到控制台。

我们在上例中使用取址操作符来获取str的地址，但如果已经有一个保存str地址的指针变量，则可以改用它：

```C++
int main()
{
    std::string str{ "Hello, world!" };
    
    printByValue(str); // 通过值传递str的拷贝
    printByReference(str); // 通过引用传递str，不会制作副本
    printByAddress(&str); // 通过地址传递str，不会制作副本

    std::string* ptr { &str }; // 定义一个指针变量保存str的地址
    printByAddress(ptr); // 通过地址传递str，不会制作副本 

    return 0;
}
```

***
## 传递地址不会复制所指向的对象

考虑以下语句：

```C++
std::string str{ "Hello, world!" };
printByAddress(&str); // 使用取址操作符 (&) 获取保存str地址的指针
```

复制std::string是昂贵的，因此希望避免这种情况。当按地址传递std::string时，不是复制实际的std::string对象——只是将指针（保存对象的地址）从调用者复制到被调用的函数。由于地址通常只有4或8个字节，因此指针仅为4或8字节，因此复制指针总是很快的。

因此，就像通过引用传递参数一样，通过地址传递参数也是快速的，并避免了复制对象。

***
## 通过地址传递参数允许函数修改参数的值

当通过地址传递对象时，函数内可以通过解引用来访问该地址上的对象。如果函数参数是指向非常量的指针，则函数可以通过指针修改对应的对象：

```C++
#include <iostream>

void changeValue(int* ptr) // note: ptr 指向非const
{
    *ptr = 6; // 将对应的值改成 6
}

int main()
{
    int x{ 5 };

    std::cout << "x = " << x << '\n';

    changeValue(&x); // 将x的地址传递给这个函数

    std::cout << "x = " << x << '\n';

    return 0;
}
```

这将打印：

```C++
x = 5
x = 6
```

如您所见，参数被修改，并且即使在changeValue()完成运行后，这种修改仍然存在。

如果函数不应修改传入的对象，则可以将函数参数设置为指向常量的指针：

```C++
void changeValue(const int* ptr) // note: ptr 现在指向const对象
{
    *ptr = 6; // error: 不能修改const对象
}
```

***
## 空指针检查

现在考虑一下这个看起来相当正常的程序：

```C++
#include <iostream>

void print(int* ptr)
{
	std::cout << *ptr << '\n';
}

int main()
{
	int x{ 5 };
	print(&x);

	int* myPtr {};
	print(myPtr);

	return 0;
}
```

当这个程序运行时，它将打印值5，然后很可能崩溃。

在对print(myPtr)的调用中，myPtr是空指针，因此函数参数ptr也将是空指针。当此空指针在函数体中解引用时，将产生未定义的行为。

通过地址传递参数时，在解引用之前，应注意确保指针不是空指针。一种方法是使用条件语句：

```C++
#include <iostream>

void print(int* ptr)
{
    if (ptr) // 检查ptr是否为空指针
    {
        std::cout << *ptr << '\n';
    }
}

int main()
{
	int x{ 5 };
	
	print(&x);
	print(nullptr);

	return 0;
}
```

在上面的程序中，检查ptr，以确保它在解引用之前不为nullptr。虽然这对于这样一个简单的函数来说是好用的，但在更复杂的函数中，这可能导致冗余逻辑（多次测试ptr是否为nullptr）或函数的逻辑嵌套。

在大多数情况下，相反的做法更有效：如果为空，快速返回：

```C++
#include <iostream>

void print(int* ptr)
{
    if (!ptr) // 如果ptr为空，快速返回给调用函数
        return;

    // 执行到这里，可以确保ptr不为空指针
    // 后续不要检查了

    std::cout << *ptr << '\n';
}

int main()
{
	int x{ 5 };
	
	print(&x);
	print(nullptr);

	return 0;
}
```

如果不应将空指针传递给函数，则可以使用断言（因为断言旨在记录不应该发生的事情）：

```C++
#include <iostream>
#include <cassert>

void print(const int* ptr)
{
	assert(ptr); // 如果传了一个空指针，立即停止执行 (因为这种情况不应该发生)

	// (可选) 生产模式下，可能不希望程序崩溃，进行一定的容错处理
	if (!ptr)
		return;

	std::cout << *ptr << '\n';
}

int main()
{
	int x{ 5 };
	
	print(&x);
	print(nullptr);

	return 0;
}
```

***
## 首选常量引用

注意，上面示例中的函数print()不能很好地处理空值——它实际上只是中止了函数。有鉴于此，为什么允许用户传入空值呢？传递引用具有与传递地址相同的好处，而不会有无意中解引用空指针的风险。

与传递地址相比，传递常量引用还有一些其他优势。

首先，因为通过地址传递的对象必须有地址，所以只有左值可以通过地址传递（因为右值没有地址）。传递常量引用更灵活，因为它可以接受左值和右值：

```C++
#include <iostream>

void printByValue(int val) // 函数参数是实际传入值的拷贝
{
    std::cout << val << '\n'; // 打印拷贝
}

void printByReference(const int& ref) // 函数参数是传入值绑定的引用
{
    std::cout << ref << '\n'; // 通过引用打印
}

void printByAddress(const int* ptr) // 函数参数是传入值的地址
{
    std::cout << *ptr << '\n'; // 通过解引用指针打印
}

int main()
{
    printByValue(5);     // 有效 (但生成了拷贝)
    printByReference(5); // 有效 (因为参数是常量引用)
    printByAddress(&5);  // 错误: 无法获取右值的地址

    return 0;
}
```

其次，通过引用传递的语法是自然的，因为可以只传入字面值常量或对象。通过传递地址传递参数，代码最终被与号（&）和星号（*）弄得乱七八糟。

在现代C++中，大多数用传递地址完成的事情都可以通过其他方法更好地完成。遵循这条常见的格言：“可以时通过引用传递参数，必须时才通过地址传递参数”。

{{< alert success >}}
**最佳实践**

除非您有特定的理由使用指针传递参数，否则首选引用。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter12/const-ptr/" next="/basic/chapter12/pointer-func-arg-two/" >}}
12.8 指针与常量
<--->
12.10 通过指针传递函数参数（第2部分）
{{< /prevnext >}}
