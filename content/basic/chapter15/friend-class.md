---
title: "友元类和友元成员函数"
date: 2024-06-24T18:56:16+08:00
---

## 友元类

友元类是可以访问另一个类的私有成员和受保护成员的类。

下面是一个示例：

```C++
#include <iostream>

class Storage
{
private:
    int m_nValue {};
    double m_dValue {};
public:
    Storage(int nValue, double dValue)
       : m_nValue { nValue }, m_dValue { dValue }
    { }

    // 设置 Display 是 Storage 的友元类
    friend class Display;
};

class Display
{
private:
    bool m_displayIntFirst {};

public:
    Display(bool displayIntFirst)
         : m_displayIntFirst { displayIntFirst }
    {
    }

    // 因为 Display 是 Storage 的友元, Display 中可以访问 Storage 的所有成员
    void displayStorage(const Storage& storage)
    {
        if (m_displayIntFirst)
            std::cout << storage.m_nValue << ' ' << storage.m_dValue << '\n';
        else // 首先显示 double 值
            std::cout << storage.m_dValue << ' ' << storage.m_nValue << '\n';
    }

    void setDisplayIntFirst(bool b)
    {
         m_displayIntFirst = b;
    }
};

int main()
{
    Storage storage { 5, 6.7 };
    Display display { false };

    display.displayStorage(storage);

    display.setDisplayIntFirst(true);
    display.displayStorage(storage);

    return 0;
}
```

由于Display类是Storage的友元，因此Display中可以访问任何Storage对象的私有成员。

该程序产生以下结果：

```C++
6.7 5
5 6.7
```

关于友元类的一些附加说明。

首先，尽管Display是Storage的友元，但Display不能访问Storage对象的*this指针（因为*this实际上是一个函数参数）。

第二，友元不是对等的。仅仅因为Display是Storage的友元，并不意味着Storage也是Display的朋友。如果希望两个类成为彼此的友元，则两者都必须将对方声明为友元。

友元也是不可传递的。如果A类是B的友元，而B是C的友元，这并不意味着A是C的友元。

友元类可以充当前向声明。这意味着不需要在将类绑定到友元之前去向前声明它。在上面的示例中，「friend class Display;」同时充当Display的向前声明和友元声明。

{{< alert success >}}
**对于高级读者**

友元也是不可继承的。如果B是A的友元，则从B派生的类不是A的友元。

{{< /alert >}}

***
## 友元成员函数

可以将单个成员函数设置为友元，而不是将整个类设置为友元。这类似于使非成员函数成为友元，只是改为使用成员函数。

然而，在现实中，这可能比预期的要复杂一些。让我们转换前面的示例，使Display::displayStorage成为友元成员函数。您可以尝试这样的操作：

```C++
#include <iostream>

class Display; // 前向声明 Display

class Storage
{
private:
	int m_nValue {};
	double m_dValue {};
public:
	Storage(int nValue, double dValue)
		: m_nValue { nValue }, m_dValue { dValue }
	{
	}

	// 让 Display::displayStorage 成员函数成为 Storage 的友元函数
	friend void Display::displayStorage(const Storage& storage); // 编译失败: Storage 这里看不到 Display 类的定义
};

class Display
{
private:
	bool m_displayIntFirst {};

public:
	Display(bool displayIntFirst)
		: m_displayIntFirst { displayIntFirst }
	{
	}

	void displayStorage(const Storage& storage)
	{
		if (m_displayIntFirst)
			std::cout << storage.m_nValue << ' ' << storage.m_dValue << '\n';
		else
			std::cout << storage.m_dValue << ' ' << storage.m_nValue << '\n';
	}
};

int main()
{
    Storage storage { 5, 6.7 };
    Display display { false };
    display.displayStorage(storage);

    return 0;
}
```

然而，这是行不通的。为了使单个成员函数成为友元，编译器必须看到友元成员函数类的完整定义（而不仅仅是前向声明）。由于类Storage尚未看到类Display的完整定义，因此编译器将在尝试使成员函数成为友元时出错。

幸运的是，通过将类Display的定义移动到类Storage的定义之前（在同一文件中，或者将Display的含义移动到头文件中，并在定义Storage之前引用它），可以很容易地解决这个问题。

```C++
#include <iostream>

class Display
{
private:
	bool m_displayIntFirst {};

public:
	Display(bool displayIntFirst)
		: m_displayIntFirst { displayIntFirst }
	{
	}

	void displayStorage(const Storage& storage) // 编译失败: 编译器不知道 Storage 是啥东西
	{
		if (m_displayIntFirst)
			std::cout << storage.m_nValue << ' ' << storage.m_dValue << '\n';
		else // display double first
			std::cout << storage.m_dValue << ' ' << storage.m_nValue << '\n';
	}
};

class Storage
{
private:
	int m_nValue {};
	double m_dValue {};
public:
	Storage(int nValue, double dValue)
		: m_nValue { nValue }, m_dValue { dValue }
	{
	}

	// 让 Display::displayStorage 成员函数成为 Storage 的友元函数
	friend void Display::displayStorage(const Storage& storage); // okay now
};

int main()
{
    Storage storage { 5, 6.7 };
    Display display { false };
    display.displayStorage(storage);

    return 0;
}
```

然而，现在有另一个问题。因为成员函数Display::displayStorage() 使用Storage作为引用参数，并且刚刚将Storage的定义移到Display的定义之下，编译器将抱怨它不知道Storage是什么。不能通过重新排列定义顺序来修复此问题，因为这样将撤消以前的修复。

幸运的是，通过几个简单的步骤，这也是可以修复的。首先，可以添加类Storage作为前向声明，以便编译器在看到类的完整定义之前可以引用Storage。

其次，可以在Storage类的完整定义之后，将 Display::displayStorage() 的定义移出该类。

下面是它的样子：

```C++
#include <iostream>

class Storage; // 前向声明 Storage

class Display
{
private:
	bool m_displayIntFirst {};

public:
	Display(bool displayIntFirst)
		: m_displayIntFirst { displayIntFirst }
	{
	}

	void displayStorage(const Storage& storage); // 这一行需要看到 Storage 的前向声明
};

class Storage // Storage 的完整定义
{
private:
	int m_nValue {};
	double m_dValue {};
public:
	Storage(int nValue, double dValue)
		: m_nValue { nValue }, m_dValue { dValue }
	{
	}

	// 让 Display::displayStorage 成员函数成为 Storage 的友元函数
	// 需要看到 Display 类的完整定义
	friend void Display::displayStorage(const Storage& storage);
};

// 现在来定义 Display::displayStorage
// 需要看到 Storage 的完整定义 (因为要访问 Storage 的成员)
void Display::displayStorage(const Storage& storage)
{
	if (m_displayIntFirst)
		std::cout << storage.m_nValue << ' ' << storage.m_dValue << '\n';
	else
		std::cout << storage.m_dValue << ' ' << storage.m_nValue << '\n';
}

int main()
{
    Storage storage { 5, 6.7 };
    Display display { false };
    display.displayStorage(storage);

    return 0;
}
```

现在一切都将正确编译：类Storage的前向声明足以满足Display类中Display::displayStorage()的声明。Display的完整定义满足了将Display::displayStorage()声明为Storage的友元。类Storage的完整定义足以满足成员函数Display::displayStorage() 的定义。

如果这有点令人困惑，请参阅上面程序中的注释。关键点是类前向声明满足对类的引用。然而，访问类的成员需要编译器看到完整的类定义。

这看起来像是一种痛苦。幸运的是，因为这是我们试图在单个文件中完成所有事情，才不得不这样做。更好的解决方案是将每个类定义放在单独的头文件中，成员函数定义放在相应的.cpp文件中。这样，所有的类定义都将在.cpp文件中可用，并且不需要重新排列类或函数！

***

{{< prevnext prev="/basic/chapter15/friend-no-member-func/" next="/basic/chapter15/ref-qulify/" >}}
15.7 友元非成员函数
<--->
15.9 引用限定符
{{< /prevnext >}}
