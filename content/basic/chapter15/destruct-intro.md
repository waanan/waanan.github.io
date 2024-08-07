---
title: "析构函数简介"
date: 2024-06-24T18:56:16+08:00
---

## 清理问题

假设您正在编写一个程序，该程序需要通过网络发送一些数据。然而，建立与服务器的连接是昂贵的，因此您希望收集一组数据，然后一次性发送所有数据。这样的类可以如下结构：

```C++
class NetworkData
{
private:
    std::string m_serverName{};
    DataStore m_data{};

public:
	NetworkData(std::string_view serverName)
		: m_serverName { serverName }
	{
	}

	void addData(std::string_view data)
	{
		m_data.add(data);
	}

	void sendData()
	{
		// 连接服务器
		// 发送数据
		// 清理数据
	}
};

int main()
{
    NetworkData n("someipAddress");

    n.addData("somedata1");
    n.addData("somedata2");

    n.sendData();

    return 0;
}
```

然而，此NetworkData存在潜在问题。它依赖于在程序关闭之前显式调用 sendData()。如果NetworkData的用户忘记执行此操作，则数据将不会发送到服务器，并在程序退出时丢失。现在，你可能会说，“嗯，记住这样做并不难！”在这种情况下，你是对的。但考虑一个稍微复杂的示例，如此函数：

```C++
bool someFunction()
{
    NetworkData n("someipAddress");

    n.addData("somedata1");
    n.addData("somedata2");

    if (someCondition)
        return false;

    n.sendData();
    return true;
}
```

在这种情况下，如果someCondition为true，则函数将提前返回，并且不会调用 sendData() 。这是一个更容易犯的错误，因为 sendData() 调用存在，但程序并不是在所有情况下都调用它。

概括下这个问题，使用资源的类（通常是内存，但有时是文件、数据库、网络连接等…），它们的类对象在销毁之前必须显式地发送或关闭。或者在其他情况下，可能希望在销毁对象之前保留一些记录，例如将信息写入日志文件。术语“清理”通常用于指类在销毁类的对象之前必须执行的任何任务，以便符合预期行为。如果必须依赖类的用户来确保在销毁对象之前调用执行清理的函数，那么代码是非常容易出错的。

但为什么要求用户确保这一点？如果对象正在被销毁，则我们知道需要在该点执行清理。清理应该自动进行吗？

***
## 析构函数

在前面我们介绍了构造函数，它们是在创建非聚合类类型的对象时调用的特殊成员函数。构造函数用于初始化成员变量，并执行所需的任何其他设置任务，以确保类的对象可以使用。

类似地，类具有另一种类型的特殊成员函数，该函数在销毁非聚合类类型的对象时自动调用。该函数称为析构函数。析构函数被设计为允许类在销毁类的对象之前进行任何必要的清理。

***
## 析构函数命名

与构造函数一样，析构函数具有特定的命名规则：

1. 构造函数的名字需要与类名一致，同时需要带一个前缀波浪号（ ~ ）
2. 析构函数不能有参数
3. 析构函数不能有返回类型

类只能有一个析构函数。

通常，您不应该显式调用析构函数（因为当对象被销毁时它将自动调用），因为很少有情况下您希望多次清理对象。

析构函数可以安全地调用其他成员函数，因为对象直到析构函数执行后才被销毁。

***
## 析构函数示例

```C++
#include <iostream>

class Simple
{
private:
    int m_id {};

public:
    Simple(int id)
        : m_id { id }
    {
        std::cout << "Constructing Simple " << m_id << '\n';
    }

    ~Simple() // 这里是析构函数
    {
        std::cout << "Destructing Simple " << m_id << '\n';
    }

    int getID() const { return m_id; }
};

int main()
{
    // 分配一个 Simple 对象
    Simple simple1{ 1 };
    {
        Simple simple2{ 2 };
    } // simple2 在这里销毁

    return 0;
} // simple1 在这里销毁
```

该程序产生以下结果：

```C++
Constructing Simple 1
Constructing Simple 2
Destructing Simple 2
Destructing Simple 1
```

请注意，当销毁每个Simple对象时，都调用析构函数，该析构函数打印一条消息。“Destructing Simple 1”打印在“Destructing Simple 2”之后，因为simple2在代码块结束时被销毁，而simple1直到main()结束才被销毁。

记住，静态变量（包括全局变量和静态局部变量）在程序启动时构造，在程序关闭时销毁。

***
## 改进NetworkData程序

回到本课顶部的示例，通过让析构函数调用 sendData() 函数，可以消除用户显式调用 sendData() 的需要：

```C++
class NetworkData
{
private:
    std::string m_serverName{};
    DataStore m_data{};

public:
	NetworkData(std::string_view serverName)
		: m_serverName { serverName }
	{
	}

	~NetworkData()
	{
		sendData(); // 确保对象被销毁时，所有的数据自动发送
	}

	void addData(std::string_view data)
	{
		m_data.add(data);
	}

	void sendData()
	{
		// 连接服务器
		// 发送数据
		// 清理数据
	}
};

int main()
{
    NetworkData n("someipAddress");

    n.addData("somedata1");
    n.addData("somedata2");

    return 0;
}
```

有了这样的析构函数，NetworkData对象将始终在销毁对象之前发送它所拥有的任何数据！清理会自动进行，这意味着出现错误的可能性更小，需要考虑的事情也更少。

***
## 隐式析构函数

如果非聚合类类型对象没有用户声明的析构函数，则编译器将生成具有空逻辑的析构函数。这个析构函数被称为隐式析构函数，它实际上只是一个占位符。

如果类不需要在销毁时进行任何清理，那么完全不定义析构函数是可以的，让编译器为类生成隐式析构函数。

***
## 关于std::exit() 函数的警告

在前面，我们讨论了std::exit() 函数，可以用于立即终止程序。当程序立即终止时，程序就结束了。局部变量不会被销毁，因此不会调用析构函数。在这种情况下，如果您依赖于析构函数来执行必要的清理工作，请谨慎。

{{< alert success >}}
**对于高级读者**

未处理的异常也将导致程序终止，并且在执行此操作之前可能不会展开堆栈。如果堆栈展开没有发生，则在程序终止之前不会调用析构函数。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter15/nest-type/" next="/basic/chapter15/class-tmplate-with-member-func/" >}}
15.2 嵌套类型（成员类型）
<--->
15.4 具有成员函数的类模板
{{< /prevnext >}}
