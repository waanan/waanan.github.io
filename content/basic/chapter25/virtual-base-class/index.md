---
title: "虚基类"
date: 2024-11-04T13:14:53+08:00
---

最上一章，讨论多重继承中，我们研究了“菱形继承问题”。在本节中，我们将继续讨论。

注意：本节是一个高级主题，可以跳过或略读。

***
## 菱形继承问题

下面是上一课中的示例（使用一些构造函数），说明问题：

```C++
#include <iostream>

class PoweredDevice
{
public:
    PoweredDevice(int power)
    {
		std::cout << "PoweredDevice: " << power << '\n';
    }
};

class Scanner: public PoweredDevice
{
public:
    Scanner(int scanner, int power)
        : PoweredDevice{ power }
    {
		std::cout << "Scanner: " << scanner << '\n';
    }
};

class Printer: public PoweredDevice
{
public:
    Printer(int printer, int power)
        : PoweredDevice{ power }
    {
		std::cout << "Printer: " << printer << '\n';
    }
};

class Copier: public Scanner, public Printer
{
public:
    Copier(int scanner, int printer, int power)
        : Scanner{ scanner, power }, Printer{ printer, power }
    {
    }
};
```

尽管您可能希望获得如下所示的继承关系图：

{{< img src="./PoweredDevice.gif" title="期望的继承情况">}}

但是如果要创建Copier类对象，默认情况下，您将得到PoweredDevice类的两个副本——一个来自Printer，一个来自Scanner。它具有以下结构：

{{< img src="./PoweredDevice2.gif" title="实际的继承情况">}}

我们可以创建一个简短的示例来展示这一点：

```C++
int main()
{
    Copier copier{ 1, 2, 3 };

    return 0;
}
```

这将产生以下结果：

```C++
PoweredDevice: 3
Scanner: 1
PoweredDevice: 3
Printer: 2
```

如您所见，PoweredDevice构造了两次。

虽然这通常是需要的，但在其他时候，您可能只希望Scanner和Printer共享PoweredDevice的一个副本。

***
## 虚基类

要共享基类，只需在派生类的继承列表中插入“virtual”关键字。这将创建所谓的虚基类，这意味着只继承一次基类对象。基类对象在继承树中的所有对象之间共享，并且它只构造一次。下面是一个示例（为了简单起见，没有构造函数），展示了如何使用virtual关键字创建共享基类：

```C++
class PoweredDevice
{
};

class Scanner: virtual public PoweredDevice
{
};

class Printer: virtual public PoweredDevice
{
};

class Copier: public Scanner, public Printer
{
};
```

现在，当您创建Copier类对象时，每个Copier只能获得PoweredDevice的一个副本，该副本将由Scanner和Printer共享。

然而，这又导致了一个问题：如果Scanner和Printer共享PoweredDevice基类，谁负责创建它？答案是Copier。Copier构造函数负责创建PoweredDevice。因此，这允许Copier调用非直接父构造函数的一次：

```C++
#include <iostream>

class PoweredDevice
{
public:
    PoweredDevice(int power)
    {
		std::cout << "PoweredDevice: " << power << '\n';
    }
};

class Scanner: virtual public PoweredDevice // 注: PoweredDevice 是虚基类
{
public:
    Scanner(int scanner, int power)
        : PoweredDevice{ power } // 为了创建Scanner，必须有这一行，但当前情况下会被忽略
    {
		std::cout << "Scanner: " << scanner << '\n';
    }
};

class Printer: virtual public PoweredDevice // 注: PoweredDevice 是虚基类
{
public:
    Printer(int printer, int power)
        : PoweredDevice{ power } // 为了创建Scanner，必须有这一行，但当前情况下会被忽略
    {
		std::cout << "Printer: " << printer << '\n';
    }
};

class Copier: public Scanner, public Printer
{
public:
    Copier(int scanner, int printer, int power)
        : PoweredDevice{ power }, // PoweredDevice 在这里被构造
        Scanner{ scanner, power }, Printer{ printer, power }
    {
    }
};
```

这一次，再次运行前面的示例：

```C++
int main()
{
    Copier copier{ 1, 2, 3 };

    return 0;
}
```

生成结果：

```C++
PoweredDevice: 3
Scanner: 1
Printer: 2
```

如您所见，PoweredDevice仅构造一次。

有一些细节。

首先，对于大多数派生类的构造函数，虚基类总是在非虚基类之前创建，这确保所有基类都是在其派生类之前创建的。

其次，请注意，Scanner和Printer构造函数仍然调用PoweredDevice构造函数。创建Copier实例时，这些构造函数调用被忽略，因为Copier负责创建PoweredDevice，而不是Scanner和Printer。然而，如果我们要创建Scanner或Printer的实例，则将使用这些构造函数调用，并应用常规继承规则。

第三，如果类继承了一个或多个具有虚父类的类，则最底层派生的类负责构造虚基类。在这种情况下，Copier继承Printer和Scanner，两者都具有PoweredDevice虚拟基类。Copier是最底层派生的类，负责创建PoweredDevice。请注意，即使在单个继承的情况下也是如此：如果Copier单独从Printer继承，并且Printer实际上是从PoweredDevice继承的，则Copier仍然负责创建PoweredDevice。

第四，继承虚基类的所有类都将具有虚函数表，因此类的实例将多一个指针。

因为Scanner和Printer实际上是从PoweredDevice派生的，而Copier将仅构造一个PoweredDevice子对象。Scanner和Printer都需要知道如何找到PoweredDevice子对象，以便它们可以访问其成员（因为它们毕竟是从中派生的）。这通常通过一些虚函数表魔术来完成（它本质上存储从每个子类到PoweredDevice子对象的偏移量）。

***

{{< prevnext prev="/basic/chapter25/abstract-class/" next="/basic/chapter25/object-slice/" >}}
25.6 纯虚函数、抽象基类和接口类
<--->
25.8 对象切片（Object slicing）
{{< /prevnext >}}
