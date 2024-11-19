---
title: "指向派生对象的基类指针和引用"
date: 2024-11-04T13:14:53+08:00
---

在前一章中，您学习了如何使用继承从现有类派生新类的所有内容。在本章中，我们将关注继承最重要和最强大的方面之一——虚拟函数。

但在我们讨论什么是虚函数之前，让我们首先为为什么需要它们设置一个表。

在关于派生类的构造的一章中，您了解到创建派生类时，它由多个部分组成：每个继承类一个部分，自身一个部分。

例如，这里有一个简单的例子：

#include<string_view>ClassBase{protected:intm_value{}；public:Base（int value）：m_value{value}{}标准：：string_view getName（）常量{return“Base”；}int getValue（）常量}return m_value；}}；派生类：public Base{public:Derived（int value）：Base{value}{}std:：string_view getName（）const{return“Deriveed”；}int getValueDoubled（）const{returnm_value*2；}}；

当我们创建衍生对象时，它包含基础零件（首先构造）和衍生零件（其次构造）。记住，继承意味着两个类之间的is-a关系。由于衍生是基础，因此衍生包含基础零件是适当的。

指针、引用和派生类

应该很直观，我们可以设置派生指针和对派生对象的引用：

#include<iostream>intmain（）{derived-derived{5}；std:：cout<<“derived是”<<derived.getName（）<<“并且具有值”<<derived.getValue（）<<'\n'；派生的&r派生的{派生}；std:：cout<<“rDerived是一个”<<rDerivered.getName（）<<“并且具有值”<<r Derived.getValue（）<<'\n'；派生*p派生{&Derived}；std:：cout<<“pDerived是一个”<<pDerivered->getName（）<<“并且具有值”<<pDerived->getValue（）<<'\n'；返回0；}

这会产生以下输出：

derived是derived，值为5 rDeriveed是Derive，值为5pDeriveD是Derivated，值为5.

然而，由于derived.有一个Base部分，一个更有趣的问题是C++是否允许我们设置对DerivedObject的Base指针或引用。事实证明，我们可以

#include<iostream>intmain（）{派生派生{5}；//这些都是合法的！基&rBase{派生}；//rBase是左值引用（不是右值引用）Base*pBase{&derived}；std:：cout<<“derived是”<<derived.getName（）<<“并且具有值”<<derived.getValue（）<<'\n'；std:：cout<<“rBase是一个”<<rBase.getName（）<<“并且具有值”<<r Base.getValue（）<<'\n'；std:：cout<<“pBase是”<<pBase->getName（）<<“并且具有值”<<pBase->getValue（）<<'\n'；返回0；}

这会产生结果：

derived是一个derived，值为5 rBase是一个Base，值为5pBase是Base，并且值为5。

这个结果可能不是您最初期望的那样！

结果是，由于rBase和pBase是Base引用和指针，因此它们只能看到Base的成员（或Base继承的任何类）。因此，即使派生对象的Derived:：getName（）阴影（隐藏）Base:：getName。因此，它们调用Base:：getName（），这就是rBase和pBase报告它们是Base而不是Derived的原因。

请注意，这也意味着不能使用rBase或pBase调用Derived:：getValueDoubled（）。他们在Derived中看不到任何内容。

这里是另一个稍微复杂一些的示例，我们将在下一课中构建：

#include<iostream>#incluse<string_view>#inclassAnimal{protected:std:：string m_name；//我们将此构造函数设置为受保护的，因为//我们不希望人们直接创建Animal对象，//但我们仍然希望派生类能够使用它。Animal；Animal&operator=（const Animal&）=删除；public:std:：string_view getName（）const{return m_name；}标准：：string_view speak（）const{返回“？？”；}}；类Cat:public Animal{public:Cat（std:：string_view-name）：动物{name}{}标准：：string-view-speak（）常量{return“喵”；}}；类Dog:public Animal{public:Dog（std:：string_view-name）：动物{name}{}标准：：string-view-speak（）常量{return“Woof”；}}；int main（）{常量猫{“Fred”}；std:：cout<<“cat被命名为”<<cat.getName（）<<“，它说“<<cat.speak（）<<'\n'；常数狗{“嘉宝”}；std:：cout<<“dog被命名为”<<dog.getName（）<<“，它说：”<<dog.speak（）<<'\n'；常量动物*pAnimal{&cat}；std:：cout<<“pAnimal被命名为”<<pAnimal->getName（）<<“，它说：”<<pAnimal->speak（）<<'\n'；p动物=&dog；std:：cout<<“pAnimal被命名为”<<pAnimal->getName（）<<“，它说：”<<pAnimal->speak（）<<'\n'；返回0；}

这就产生了结果：

猫叫弗雷德，它说喵喵的狗叫嘉宝，它说Woof pAnimal叫弗雷德。它说？？？pAnimal被命名为Garbo，它说？？？

我们在这里看到了相同的问题。因为pAnimal是一个Animal指针，所以它只能看到类的Animal部分。因此，pAnimal->speak（）调用Animal:：speak。

用于指向基类的指针和引用

现在您可能会说，“上面的示例似乎有点傻。当我可以只使用派生对象时，为什么要设置指向派生对象基类的指示器或引用？”事实证明，有许多很好的原因。

首先，假设您想编写一个打印动物名称和声音的函数。如果不使用指向基类的指针，则必须使用重载函数来编写它，例如：

void report（const Cat&Cat）{std:：cout<<Cat.getName（）<<“says”<<Cat.speak（）<<'\n'；}void report[const Dog&Dog）{std:：cout<<Dog.getName（）<<“saws”<Dog.speak（。

您必须编写30个几乎相同的函数！此外，如果你添加了一种新的动物类型，你也必须为它编写一个新的函数。考虑到唯一的实际差异是参数的类型，这是一个巨大的时间浪费。然而，由于猫和狗是从动物衍生而来的，猫和狗有一个动物部分。因此，我们应该能够这样做是有意义的：

void report（const Animal&rAnimal）{std:：cout<<rAnimal.getName（）<<“says”<<r动物.speak（）<<'\n'；}

这将允许我们传入从Animal派生的任何类，甚至是我们在编写函数后创建的类！不是每个派生类一个函数，而是得到一个可以与从Animal派生的所有类一起工作的函数！

当然，问题是，由于rAnimal是一个Animal引用，因此rAnimal.speak（）将调用Animal:：speak。

其次，假设您有3只猫和3只狗，您希望将它们放在一个数组中以便于访问。由于数组只能保存一种类型的对象，没有指向基类的指针或引用，因此您必须为每个派生类型创建不同的数组，如下所示：

上面的intmain（）{constauto&cats{std:：to_array<Cat>（{{“Fred”}，{“Misty”}、{“Zeke”}}）}；常量自动狗（&D）{std:：to_array<Dog>（{{“Garbo”}，{“Pooky”}、{“Truffle”}}）}；//在C++20//const std:：array<Cat之前，3>cats{{{“Fred”}，{“Misty”}、{“Zeke”}}；//const std:：array<狗，3>狗{{“Garbo”}，{“Pooky”}、{“块菌”}}}；for（const auto&cat:cats）{std:：cout<<cat.getName（）<<“says”<<cat.speak（）<<'\n'；}for（const-auto&dog:dogs）{std:：cout<<dog.getName（）<<“saws”<<dog.speak（

现在，考虑一下如果你有30种不同类型的动物会发生什么。你需要30个阵列，每种动物一个！然而，由于猫和狗都是从Animal派生而来的，因此我们应该能够这样做：

#include<array>#incluse<iostream>//上面例子中的猫和狗int main（）{const Cat fred{“fred”}；常量猫薄雾{“薄雾”}；常数Cat zeke{“zeke”}；const Dog garbo{“garbo”}；const小狗{“pooky”}；const狗松露{“松露”}；//设置一个指向动物的指针数组，并将这些指针设置为我们的猫和狗对象const auto animals{std:：to_array<const Animal*>（{&fred，&garbo，&misty，&pooky，&truffle，&zeke}）}；//在C++20之前，显式指定数组大小//const std:：array<const Animal*，6>animals{&fred，&garbo，&misty，&pooky，&truffle，&zeke}；for（const-auto-animal:animals）{std:：cout<<animal->getName（）<<“says”<<animal->speak（）<<'\n'；}返回0；}

在编译和执行时，不幸的是，数组“animals”的每个元素都是指向Animal的指针，这意味着Animal->speak（）将调用Animal:：speak。

输出是

弗雷德说的？？？嘉宝说？？？米丝蒂说？？？普奇说？？？松露说？？？Zeke说？？？

尽管这两种技术都可以为我们节省大量的时间和精力，但它们有相同的问题。基类的指针或引用调用函数的基版本，而不是派生版本。如果有某种方法可以使这些基指针调用函数的派生版本而不是基版本……

想猜一猜虚拟函数是用于什么的吗？

***