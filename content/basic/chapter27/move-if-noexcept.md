---
title: "标准：：move_if_noexcept"
date: 2025-02-12T14:07:59+08:00
---

在之前，我们介绍了std:∶move，它将其左值参数强制转换为右值，以便我们可以调用移动语义。在上一节，我们介绍了noexcept。本课程以这两个概念为基础。

我们还讨论了强异常保证，它保证如果函数被异常中断，则不会泄漏内存，并且不会更改程序状态。特别是，所有构造函数都应该支持强异常保证，以便在对象构造失败时，程序的其余部分不会处于被更改状态。

***
## 移动构造函数与异常问题

考虑这样的情况，我们正在复制某个对象，但由于某种原因（例如，机器内存不足），复制失败。在这种情况下，被复制的对象不会受到任何伤害，因为不需要修改源对象来创建副本。我们可以丢弃失败的副本，继续前进。强保证得到支持。

现在考虑这样一种情况，即我们正在移动一个对象。移动操作将给定资源的所有权从源对象转移到目标对象。如果在所有权转移发生后，移动操作被异常中断，则源对象将保持在修改状态。如果源对象是临时对象，并且在移动后仍将被丢弃，则这不是问题——但对于非临时对象，我们现在已经损坏了源对象。为了遵守强异常保证，我们需要将资源移回源对象，但如果第一次移动失败，那么同样不能保证移回将成功。

如何为move构造函数提供强异常保证？很简单，避免在移动构造函数的函数体中抛出异常，但移动构造函数可以调用其他可能抛出异常的构造函数。以std::pair的移动构造函数为例，它必须尝试将源pair中的每个子对象移动到新的对对象中。

```C++
// std::pair 的样例移动构造函数定义
// 输入 'old' pair, 然后移动构造新 pair 的 'first' 和 'second'
template <typename T1, typename T2>
pair<T1,T2>::pair(pair&& old)
  : first(std::move(old.first)),
    second(std::move(old.second))
{}
```

现在让我们使用两个类MoveClass和CopyClass，我们将使用它们配对来演示移动构造函数的强异常保证：

```C++
#include <iostream>
#include <utility> // For std::pair, std::make_pair, std::move, std::move_if_noexcept
#include <stdexcept> // std::runtime_error

class MoveClass
{
private:
  int* m_resource{};

public:
  MoveClass() = default;

  MoveClass(int resource)
    : m_resource{ new int{ resource } }
  {}

  // 拷贝构造函数
  MoveClass(const MoveClass& that)
  {
    // 深拷贝
    if (that.m_resource != nullptr)
    {
      m_resource = new int{ *that.m_resource };
    }
  }

  // 移动构造函数
  MoveClass(MoveClass&& that) noexcept
    : m_resource{ that.m_resource }
  {
    that.m_resource = nullptr;
  }

  ~MoveClass()
  {
    std::cout << "destroying " << *this << '\n';

    delete m_resource;
  }

  friend std::ostream& operator<<(std::ostream& out, const MoveClass& moveClass)
  {
    out << "MoveClass(";

    if (moveClass.m_resource == nullptr)
    {
      out << "empty";
    }
    else
    {
      out << *moveClass.m_resource;
    }

    out << ')';
    
    return out;
  }
};


class CopyClass
{
public:
  bool m_throw{};

  CopyClass() = default;

  // 如果 m_throw 是 true，那么抛出异常
  CopyClass(const CopyClass& that)
    : m_throw{ that.m_throw }
  {
    if (m_throw)
    {
      throw std::runtime_error{ "abort!" };
    }
  }
};

int main()
{
  // 这里定义 std::pair 没有任何问题:
  std::pair my_pair{ MoveClass{ 13 }, CopyClass{} };

  std::cout << "my_pair.first: " << my_pair.first << '\n';

  // 单当我们尝试调用移动语义时会发生问题
  try
  {
    my_pair.second.m_throw = true; // 设置拷贝构造函数会抛出异常

    // 下一行会抛出异常
    std::pair moved_pair{ std::move(my_pair) }; // 稍后注释这一行
    // std::pair moved_pair{ std::move_if_noexcept(my_pair) }; // 稍后取消这一行的注释

    std::cout << "moved pair exists\n"; // 不会打印
  }
  catch (const std::exception& ex)
  {
      std::cerr << "Error found: " << ex.what() << '\n';
  }

  std::cout << "my_pair.first: " << my_pair.first << '\n';

  return 0;
}
```

上述程序打印：


```C++
destroying MoveClass(empty)
my_pair.first: MoveClass(13)
destroying MoveClass(13)
Error found: abort!
my_pair.first: MoveClass(empty)
destroying MoveClass(empty)
```

让我们来看看发生了什么。打印的第一行显示了用于初始化my_pair的临时MoveClass对象在执行my_pair实例化语句后立即被销毁。它是空的，因为my_pair中的MoveClass子对象是由它移动构造的，下一行显示了my_pair.first包含值为13的MoveClass对象。

它在第三行变得有趣。我们通过调用CopyClass的拷贝构造函数来创建moved_pair，但由于我们更改了布尔标志，该拷贝构造引发了异常。moved_pair的构造被异常中止，其已构造的成员被销毁。在这种情况下，MoveClass成员被销毁，打印销毁MoveClass(13)变量。接下来我们看到"Error found: abort!"消息，由main()打印。

当我们再次尝试打印my_pair.first时，它显示MoveClass成员为空。由于moved_pair是用std::move初始化的，因此MoveClass成员（具有移动构造函数）被move走了，my_pair.first为null。

最后，在main()的末尾销毁了my_pair。

总结上述结果：std::pair的移动构造函数使用了CopyClass的抛出异常的拷贝构造函数。此拷贝构造函数引发了异常，导致moved_pair的创建中止，my_pair.first永久损坏。未实现强异常保证。

***
## 使用std::move_if_noexcept解决该问题

请注意，如果std::pair试图进行复制而不是移动，则可以避免上述问题。在这种情况下，moved_pair将无法成功构造，但my_pair不会被更改。

但复制而不是移动具有性能成本，我们不想为所有对象支付该成本--理想情况下，如果可以安全地进行移动，我们希望进行移动，否则需要进行复制。

幸运的是，C++有两种机制，当组合使用时，让我们正好做到这一点。首先，因为noexcept函数不抛出异常，所以它们隐式地满足强异常保证的标准。

其次，我们可以使用标准库函数std::move_if_noexcept()来自动选择应该执行移动还是复制。std::move_if_noexcept是std::move的对应项，并以相同的方式使用。

如果编译器判断，作为参数传递给std::move_if_noexcept的对象在移动构造时不会引发异常（或者，如果该对象是仅移动的，并且没有拷贝构造函数），则std::move_if_noexcept的执行效果将与std::move()相同（并返回转换为右值的对象）。否则，std::move_if_noexcept将返回对象的正常左值引用。

{{< alert success >}}
**关键点**

如果对象具有noexcept移动构造函数，则std::move_if_noexcept将返回可移动的右值，否则它将返回可复制的左值。我们可以将noexcept说明符与std::move_if_noexcept结合使用，以仅在存在强异常保证时使用移动语义（否则使用复制语义）。

{{< /alert >}}

让我们按如下所示更新前一示例中的代码：

```C++
//std::pair moved_pair{std::move(my_pair)}; // 现在注释这一行
std::pair moved_pair{std::move_if_noexcept(my_pair)}; // 取消这一行的注释
```

再次运行该程序将打印：

```C++
destroying MoveClass(empty)
my_pair.first: MoveClass(13)
destroying MoveClass(13)
Error found: abort!
my_pair.first: MoveClass(13)
destroying MoveClass(13)
```

可以看到，在引发异常后，子对象my_pair.first仍然指向值13。

std::pair的移动构造函数不是noexcept（到C++20为止），因此std::move_if_noexcept将my_pair作为左值引用返回。这会导致通过拷贝构造函数（而不是移动构造函数）创建moved_pair。拷贝构造函数可以安全地抛出异常，因为它不会修改源对象。

标准库通常使用std::move_if_noexcept来优化noexcept函数的调用。例如，如果元素类型具有noexcept移动构造函数，则std::vector::resize()将使用移动语义，否则将使用复制语义。这意味着std::vector通常在具有noexcept移动构造函数的对象上运行得更快。

{{< alert success >}}
**警告**

如果类型具有抛出异常的移动语义和删除的复制语义（拷贝构造函数和拷贝赋值操作符不可用），则std::move_if_noexcept将放弃强保证并调用移动语义。这种对强保证的有条件放弃在标准库容器类中无处不在，因为它们经常使用std::move_if_noexcept。

{{< /alert >}}

