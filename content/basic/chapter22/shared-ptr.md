---
title: "std::shared_ptr"
date: 2024-08-23T14:54:42+08:00
---

std::unique_ptr被设计为单独拥有和管理资源，而std::shared_ptr旨在解决需要多个智能指针共同拥有资源的情况。

这意味着可以让多个std::shared_ptr指向同一资源。在std::shared_ptr内部会跟踪有多少个std::shared_ptr正在共享资源。只要有至少有一个std::shared_ptr指向该资源，资源就不会被释放，即使单个std::shared_ptr被销毁。一旦管理资源的最后一个std::shared_ptr超出作用域（或重新分配置了其它数据），资源将被释放。

与std::unique_ptr一样，std::shared_ptr也存在于\<memory\>头文件中。

```C++
#include <iostream>
#include <memory> // for std::shared_ptr

class Resource
{
public:
	Resource() { std::cout << "Resource acquired\n"; }
	~Resource() { std::cout << "Resource destroyed\n"; }
};

int main()
{
	// 动态分配一个 Resource 对象，并将所有权赋给 std::shared_ptr
	Resource* res { new Resource };
	std::shared_ptr<Resource> ptr1{ res };
	{
		std::shared_ptr<Resource> ptr2 { ptr1 }; // 让另外的 std::shared_ptr 也指向相同的资源

		std::cout << "Killing one shared pointer\n";
	} // ptr2 超出作用域, 但资源仍被ptr1持有

	std::cout << "Killing another shared pointer\n";

	return 0;
} // ptr1 超出作用域, 分配的 Resource 被销毁
```

这将打印：

```C++
Resource acquired
Killing one shared pointer
Killing another shared pointer
Resource destroyed
```

在上面的代码中，我们创建了一个动态Resource对象，并设置了一个名为ptr1的std::shared_ptr来管理它。在嵌套块中，使用拷贝构造函数来创建指向同一资源的第二个std:∶shared_ptr（ptr2）。当ptr2超出作用域时，不会释放资源，因为ptr1仍然指向资源。当ptr1超出作用域时，ptr1注意到不再有std::shared_ptr管理资源，因此它释放了资源。

请注意，我们从第一个shared_ptr创建了第二个shared_ptr。这很重要。考虑以下类似的程序：

```C++
#include <iostream>
#include <memory> // for std::shared_ptr

class Resource
{
public:
	Resource() { std::cout << "Resource acquired\n"; }
	~Resource() { std::cout << "Resource destroyed\n"; }
};

int main()
{
	Resource* res { new Resource };
	std::shared_ptr<Resource> ptr1 { res };
	{
		std::shared_ptr<Resource> ptr2 { res }; // 直接从res创建 ptr2 

		std::cout << "Killing one shared pointer\n";
	} // ptr2 超出作用域, 分配的资源被销毁

	std::cout << "Killing another shared pointer\n";

	return 0;
} // ptr1 超出作用域, 分配的资源被再次销毁
```

该程序打印：

```C++
Resource acquired
Killing one shared pointer
Resource destroyed
Killing another shared pointer
Resource destroyed
```

然后崩溃（至少在作者的机器上）。

这里的区别是，独立地创建了两个std::shared_ptr。因此，即使它们都指向相同的资源，它们也不会意识到彼此。当ptr2超出作用域时，它认为自己是资源的唯一所有者，并释放它。当ptr1以后超出作用域，它也会这样想，并再次尝试删除资源。然后坏事发生了。

幸运的是，这是很容易避免的：如果需要将多个std::shared_ptr指向给定的资源，请复制现有的std::shared_ptr。

就像std::unique_ptr一样，std::shared_ptr可以是空指针，因此在使用之前请检查其是否有效。

***
## std::make_shared

C++14中的std::make_unique()可以用于创建std::unique_ptr，与其类似，std::make_shared() 可以（并且应该）用于生成std::shared_ptr。std::make_shared() 在C++11中可用。

下面是使用std::make_shared()的实例：

```C++
#include <iostream>
#include <memory> // for std::shared_ptr

class Resource
{
public:
	Resource() { std::cout << "Resource acquired\n"; }
	~Resource() { std::cout << "Resource destroyed\n"; }
};

int main()
{
	// 动态分配一个 Resource 对象并将所有权交给 std::shared_ptr
	auto ptr1 { std::make_shared<Resource>() };
	{
		auto ptr2 { ptr1 }; // 从 ptr1 创建 ptr2

		std::cout << "Killing one shared pointer\n";
	} // ptr2 超出作用域, 但资源仍被ptr1持有

	std::cout << "Killing another shared pointer\n";

	return 0;
} // ptr1 超出作用域, 分配的 Resource 被销毁
```

使用std::make_shared() 的原因与std::make_unique() 一样。

***
## 挖掘std::shared_ptr

与在内部使用单个指针的std::unique_ptr不同，std::shared_ptr在内部使用两个指针。一个指针指向被管理的资源。另一个指向“控制块”，这是一个动态分配的对象，它跟踪一系列内容，包括有多少std::shared_ptr指向资源。当通过std::shared_ptr构造函数创建std::shared_ptr时，托管对象（通过传入）和控制块（构造函数创建）的内存将分别分配。然而，当使用std::make_shared()时，可以将其优化为单次内存分配，从而获得更好的性能。

这也解释了为什么单独创建两个指向同一资源的std::shared_ptr会给我们带来麻烦。每个std::shared_ptr都有一个指向资源的指针。然而，每个std::shared_ptr将独立地分配自己的控制块，这将表明它是唯一拥有该资源的指针。因此，当该std::shared_ptr超出作用域时，它将释放该资源，而没有意识到还有其他std::shared_ptr也在尝试管理该资源。

然而，当使用拷贝赋值克隆std::shared_ptr时，可以适当地更新控制块中的数据，以指示现在有额外的std::shared_ptr共同管理资源。

***
## 可以从unique_ptr创建shared_ptr

shared_ptr的构造函数可以接收右值unique_ptr。std::unique_ptr的内容将移动到std::shared_ptr。

然而，无法安全地将std::shared_ptr转换为std::unique_ptr。这意味着，如果您要创建一个返回智能指针的函数，那么最好返回一个std::unique_ptr，并在适当的时候将其分配给std::shared_ptr。

***
## std::shared_ptr的风险

std::shared_ptr具有与std::unique_ptr相同的一些挑战——如果未正确处置std::shared_ptr（或者是因为它是动态分配的，但从未删除，或者是动态分配但从未删除的对象的一部分），则它所管理的资源也不会被释放。使用std::unique_ptr，您只需担心一个智能指针是否被正确释放。使用std::shared_ptr，您必须担心所有智能指针是否被正确释放。如果管理资源的任何std::shared_ptr未正确销毁，则不会正确释放该资源。

***
## std::shared_ptr和数组

在C++17和更早版本中，std::shared_ptr不支持管理数组，不能用于管理C样式的数组。从C++20开始，std::shared_ptr开始支持数组。

***
## 结论

std::shared_ptr是为多个智能指针共同管理同一资源的情况而设计的。当管理资源的最后一个std::shared_ptr被销毁时，将释放该资源。

***

{{< prevnext prev="/basic/chapter22/unique-ptr/" next="/basic/chapter22/circle-ref/" >}}
22.4 std::unique_ptr
<--->
22.6 std::shared_ptr的循环依赖性问题和std::weak_ptr
{{< /prevnext >}}
