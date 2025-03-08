---
title: "流的状态和输入验证"
date: 2025-03-02T00:53:53+08:00
---

## 流的状态

ios_base类包含多个状态标志，用于通知使用流时可能发生的各种情况：

|  标志 | 含义  |
|  ----  | ----  |
| goodbit | 一切正常 |
| badbit | 一些致命错误发生 (例如，尝试读取文件结尾之后的数据) |
| eofbit | 读取文件到了结尾 |
| failbit | 非致命错误发生 (例如，尝试读取int，但输入了字符) |

尽管这些标志存在于ios_base中，但由于ios是从ios_base派生的，并且ios更短一点，因此它们通常通过ios访问（例如，std::ios::failbit）。

ios还提供了许多成员函数，以便方便地访问这些状态：

| 成员函数 | 含义  |
|  ----  | ----  |
| good() | 如果状态为goodbit（当前stream一切正常），返回true |
| bad() | 如果状态为badbit（发生致命错误），返回true |
| eof() | 如果状态为eofbit（读到文件结尾），返回true |
| fail() | 如果状态为failbit（发生非致命错误），返回true |
| clear() | 清空stream上的所有标志，并设置为 goodbit |
| clear(state) | 清空stream上的所有标志，并设置为传入的state |
| rdstate() | 返回当前设置的标志 |
| setstate(state) | 设置传入的state到stream上 |


最常见的处理位是failbit，它是在用户输入无效输入时设置的。例如，考虑以下程序：

```C++
std::cout << "Enter your age: ";
int age {};
std::cin >> age;
```

请注意，该程序需要用户输入整数。然而，如果用户输入非数字数据，如“Alex”，cin将无法提取数据，并且将设置failbit。

如果发生错误，并且stream被设置为goodbit以外的任何值，则将忽略该stream上的后续操作。可以通过调用clear()函数来清除此条件。

***
## 输入验证

输入验证是检查用户输入是否满足某组标准的过程。输入验证通常可以分为两种类型：字符串和数字。

对于字符串验证，我们将所有用户输入作为字符串，然后根据字符串的格式是否适当来接受或拒绝该字符串。例如，如果我们要求用户输入电话号码，我们可能希望确保他们输入的数据有十个数字。在大多数语言（特别是像Perl和PHP这样的脚本语言）中，这是通过正则表达式完成的。C++标准库也有一个正则表达式库。由于与手动字符串验证相比，正则表达式速度较慢，因此只有在性能（编译时和运行时）不受关注或手动验证过于繁琐的情况下才应使用它们。

对于数值验证，我们通常关注的是确保用户输入的数字在特定范围内（例如，在0和20之间）。然而，与字符串验证不同，用户可以输入根本不是数字的东西——我们也需要处理这些情况。

为了帮助我们，C++提供了许多有用的函数，我们可以使用这些函数来确定特定的字符是数字还是字母。cctype头文件中存在以下函数：

| 函数 | 含义  |
|  ----  | ----  |
| std::isalnum(int) | 如果参数是字母或数字字符，返回非0值 |
| std::isalpha(int) | 如果参数是字母字符，返回非0值 |
| std::iscntrl(int) | 如果参数是控制字符，返回非0值 |
| std::isdigit(int) | 如果参数是数字字符，返回非0值 |
| std::isgraph(int) | 如果参数是可打印但非空白字符，返回非0值 |
| std::isprint(int) | 如果参数是可打印（包括空白）字符，返回非0值 |
| std::ispunct(int) | 如果参数不是字母也不是数字字符，返回非0值	|
| std::isspace(int) | 如果参数是空白字符，返回非0值 |
| std::isxdigit(int) | 如果参数是十六进制字符(0-9, a-f, A-F)，返回非0值 |

***
## 字符串验证

让我们通过要求用户输入他们的名字来进行一个简单的字符串验证。我们的验证标准是用户只输入字母字符或空格。如果遇到任何其他情况，输入将被拒绝。

对于可变长度输入，验证字符串的最佳方法（除了使用正则表达式库）是逐个处理字符串的每个字符，并确保它符合验证标准。这就是std::all_of的功能。

```C++
#include <algorithm> // std::all_of
#include <cctype> // std::isalpha, std::isspace
#include <iostream>
#include <ranges>
#include <string>
#include <string_view>

bool isValidName(std::string_view name)
{
  return std::ranges::all_of(name, [](char ch) {
    return std::isalpha(ch) || std::isspace(ch);
  });

  // 在 C++20 之前, 没有 ranges 库，使用如下代码
  // return std::all_of(name.begin(), name.end(), [](char ch) {
  //    return std::isalpha(ch) || std::isspace(ch);
  // });
}

int main()
{
  std::string name{};

  do
  {
    std::cout << "Enter your name: ";
    std::getline(std::cin, name); // 读取一整行, 包括其中的空格
  } while (!isValidName(name));

  std::cout << "Hello " << name << "!\n";
}
```

注意，这段代码并不完美：用户可以说他们的名字是“asfwjweosdiweao”或其他一些胡言乱语，或者更糟的是，只是一堆空格。我们可以通过改进验证标准来稍微解决这个问题，使其仅接受包含至少一个字符和最多一个空格的字符串。

现在，让我们来看另一个例子，我们将要求用户输入他们的电话号码。与用户名（长度可变，每个字符的验证标准相同）不同，电话号码是固定长度的，但验证标准因字符的位置而异。因此，我们将采取不同的方法来验证电话号码输入。在这种情况下，我们将编写一个函数，该函数将根据预定的模板检查用户的输入，以查看它是否匹配。模板的工作方式如下：

‘#’将匹配用户输入中的任何数字字符。
‘@’将匹配用户输入中的任何字母字符。
‘_’将匹配任何空白。
‘？’将匹配任何内容。
否则，用户输入和模板中的字符必须完全匹配。

因此，如果我们要求函数匹配模板“（###）###-####”，这意味着我们希望用户输入一个“（”字符、三个数字字符、一个“）”字符、一个空格、三个数字字符、一个破折号和四个数字字符。如果这些东西中的任何一个不匹配，输入将被拒绝。

代码如下：

```C++
#include <algorithm> // std::equal
#include <cctype> // std::isdigit, std::isspace, std::isalpha
#include <iostream>
#include <map>
#include <ranges>
#include <string>
#include <string_view>

bool inputMatches(std::string_view input, std::string_view pattern)
{
    if (input.length() != pattern.length())
    {
        return false;
    }

    // 这里定义了匹配规则
    // 每一个字符，都映射到一个判定函数，来判断是否满足规则
    static const std::map<char, int (*)(int)> validators{
      { '#', &std::isdigit },
      { '_', &std::isspace },
      { '@', &std::isalpha },
      { '?', [](int) { return 1; } }
    };

    // 在 C++20 之前, 使用如下
    // return std::equal(input.begin(), input.end(), pattern.begin(), [](char ch, char mask) -> bool {
    // ...

    return std::ranges::equal(input, pattern, [](char ch, char mask) -> bool {
        auto found{ validators.find(mask) };
        
        if (found != validators.end())
        {
            // 如果判定字符是合法的
            // 调用对应的函数
            return (*found->second)(ch);
        }

        // 否则，判断是否能精准的匹配
        return ch == mask;
        }); // lambda 结尾
}

int main()
{
    std::string phoneNumber{};

    do
    {
        std::cout << "Enter a phone number (###) ###-####: ";
        std::getline(std::cin, phoneNumber);
    } while (!inputMatches(phoneNumber, "(###) ###-####"));

    std::cout << "You entered: " << phoneNumber << '\n';
}
```

使用此函数，我们可以强制用户精确匹配我们的特定格式。然而，该函数仍然受到几个约束：如果用户输入了‘#’、‘_’、‘@’、‘?’，该函数将无法正常验证，因为这些符号已被赋予特殊含义。此外，与正则表达式不同，没有表示“可以输入可变数量的字符”的模板符号。因此，这样的模板不能用于确保用户输入由空白分隔的两个单词，因为它不能处理单词长度可变的事实。对于此类问题，使用正则表达式，或者特殊编写的函数更为合适。

***
## 数字验证

处理数值输入时，显而易见的方法是使用提取操作符将输入提取为数值类型。通过检查故障位，我们可以知道用户是否输入了数字。

让我们试试这种方法：

```C++
#include <iostream>
#include <limits>

int main()
{
    int age{};

    while (true)
    {
        std::cout << "Enter your age: ";
        std::cin >> age;

        if (std::cin.fail()) // 如果没能提取成功
        {
            std::cin.clear(); // 将状态设置回 goodbit，这样才能使用 ignore()
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); // 清空掉stream中的数据
            continue; // 再次重试
        }

        if (age <= 0) // 确保用户输入的年龄是正数
            continue;

        break;
    }

    std::cout << "You entered: " << age << '\n';
}
```

如果用户输入整数，则提取将成功。std::cin.fail（）将计算为false，跳过条件，并且（假设用户输入了一个正数），我们将命中break语句，退出循环。

如果用户输入以字母开头的输入，则提取将失败。std::cin.fail()将计算为true，将进入条件。在条件块的末尾，执行continue语句，该语句将跳回到while循环的顶部，用户将被要求再次输入。

然而，还有一种情况我们尚未测试，那就是用户输入一个以数字开头但随后包含字母的字符串（例如“34abcd56”）。在这种情况下，起始数字（34）将被提取到age中，字符串的其余部分（“abcd56”）将留在输入流中，并且不会设置故障位。这会导致两个潜在问题：

1. 如果我们认为这是有效输入，但其实在stream中残留垃圾数据
2. 如果我们认为这是无效输入，需要进行拒绝

让我们解决第一个问题。这很容易：

```C++
#include <iostream>
#include <limits>

int main()
{
    int age{};

    while (true)
    {
        std::cout << "Enter your age: ";
        std::cin >> age;

        if (std::cin.fail()) // 如果没能提取成功
        {
            std::cin.clear(); // 将状态设置回 goodbit，这样才能使用 ignore()
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); // 清空掉stream中的数据
            continue; // 再次重试
        }

        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); // 清空掉stream中的额外数据

        if (age <= 0) // 确保用户输入的年龄是正数
            continue;

      break;
    }

    std::cout << "You entered: " << age << '\n';
}
```

如果您不希望这样的输入有效，我们将不得不做一些额外的工作。幸运的是，前面的解决方案使我们走到了一半。我们可以使用gcount()函数来确定忽略了多少个字符。如果输入有效，gcount()应该返回1（被丢弃的换行符）。如果返回大于1，则用户输入了未正确提取的内容，我们应该要求他们输入新的输入。下面是一个例子：

```C++
#include <iostream>
#include <limits>

int main()
{
    int age{};

    while (true)
    {
        std::cout << "Enter your age: ";
        std::cin >> age;

        if (std::cin.fail()) // 如果没能提取成功
        {
            std::cin.clear(); // 将状态设置回 goodbit，这样才能使用 ignore()
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); // 清空掉stream中的数据
            continue; // 再次重试
        }

        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); // 清空掉stream中的额外数据
        if (std::cin.gcount() > 1) // 如果清空掉的字符超过一个
        {
            continue; // 认为输入不合法
        }

        if (age <= 0) // 确保用户输入的年龄是正数
        {
            continue;
        }

        break;
    }

    std::cout << "You entered: " << age << '\n';
}
```

***
## 作为字符串的数字验证

为了得到一个简单的值，上面的示例做了相当多的工作！处理数字输入的另一种方法是将其作为字符串读入，然后尝试将其转换为数字类型。以下程序使用该方法：

```C++
#include <charconv> // std::from_chars
#include <iostream>
#include <limits>
#include <optional>
#include <string>
#include <string_view>

// std::optional<int> 返回int，或者无数据
std::optional<int> extractAge(std::string_view age)
{
    int result{};
    const auto end{ age.data() + age.length() }; // 找到C样式字符串的结尾

    // 尝试将 age 解析为一个 int
    // 如果失败
    if (std::from_chars(age.data(), end, result).ec != std::errc{})
    {
        return {}; // 什么也不返回
    }

    if (result <= 0) // 确保用户输入的年龄是正数
    {
        return {}; // 什么也不返回
    }

    return result; // 返回提取结果
}

int main()
{
    int age{};

    while (true)
    {
        std::cout << "Enter your age: ";
        std::string strAge{};

        // 尝试读一行数据
        if (!std::getline(std::cin >> std::ws, strAge))
        {
            // 如果失败了，清空输入，再次重试
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');    
            continue;
        }

        // 尝试提取年龄
        auto extracted{ extractAge(strAge) };

        // 如果提起失败，再次重试
        if (!extracted)
            continue;

        age = *extracted; // 获取提取的值
        break;
    }

  std::cout << "You entered: " << age << '\n';
}
```

这种方法是否比直接的数字提取进行更多的工作，取决于您的验证参数和限制。

正如您所看到的，在C++中进行输入验证是一项大量的工作。幸运的是，许多这样的任务（例如，作为字符串进行数字验证）可以很容易地转换为可以在各种情况下重用的函数。

***