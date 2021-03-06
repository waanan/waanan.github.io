---
layout: post
title:  EOPL,前言
date:   2020-06-23 22:00:00 +0800
categories: eopl
---

* content
{:toc}

## 前言
作者: Hal Abelson

本书主要着重讲述如下基本概念:

*一个编程语言的解释器只是另外一段程序而已。*

听起来是否显而易见？但是却隐藏着深刻的逻辑。如果你是一个计算机理论学家，解释器的概念会让你想起「哥德尔」的不完备定律，「图灵」的通用计算器理论，又或是「冯·诺伊曼」的程序存储的思想。如果你是程序员，掌握解释器的思想会是一种巨大的力量源泉，会让你对于程序的认识有一个真正的改变。

在学习解释器之前，我编写过大量的语言，其中一些相当复杂。例如，我用「PL/I」语言编写数据存取和管理系统。当我编程时，将「PL/I」语言当作语言设计者建立的不可更改的规则集合。我的工作不是去更改这些规则，甚至不是去理解这些规则，而是从厚厚的编程手册中，挑选出这个或那个特性。我从来没想过程序语言的底层数据结构是什么，是否也可以去修改语言设计者选择的一些特性。我也不知道如何创造嵌入的子语言来帮助我组织代码，所以整个程序像是一个大大的拼图，每一片都必须恰好拼对地方，而不是像一组语言集合，可以有机的结合在一起。如果你不明白解释器，你仍然可以编程，甚至可以成为一个不错的程序员，但是永远也无法成为大师。

作为程序员的你，需要学习解释器有如下三个原因：

首先，你可能会在一定程度上实现一个解释器，这可能并不是通用的解释器。因为几乎所有人与复杂系统(绘图程序，信息存取系统)的交互，都包含了类似解释器的结构。这些程序可能包含复杂的单独的操作-在屏幕上渲染一块区域，或者执行数据库查询-解释器是你将复杂的操作组合成有用的模式的胶水。能否将一个操作的结果当作另外一个操作的输入？能否对一系列的操作命名？名称是全局的还是局部的？能否向一系列的操作传递参数，并给输入命名？诸如此类。不论单独的指令多么复杂，多么炫目，通常是将这些指令组合起来的胶水的质量决定了系统的能力。很容易就能发现单独的指令质量很高，但是代码的组织方式很糟糕的程序。比如说，我的「PL/I」数据库程序就是这样的。

其次，那些不是解释器的程序都有一些类似解释器的重要部分。如果你去看一个复杂的计算机救援系统，你会发现一个地理位置识别语言，一个图像解释器，一个规则控制解释器，一个面向对象语言解释器组合在一起。管理复杂程序的一个有力的手段，就是将程序作为一些程序语言的集合，不同的语言提供了对程序中不同元素的管理。选择合适的语言做合适的事情，理解不同语言实现的权衡。这是我们研究解释器的意义。

最后，显式的去修改语言的结构是一种越来越重要的编程技术。在面向对象语言中设计并且操作类的继承结构就是这样一种趋势。可能一个不可避免的结果是我们的程序越来越复杂 - 更加的对语言进行理解可能能帮助我们面对这种复杂度。考虑如下一个基本概念，解释器是一个程序。但是这个程序是用其它语言写的，其它语言的解释器又是用来另外一个语言写的，最后这个语言的解释器是它自己。。。可能程序和编程语言的区别只是一种错误的划分，未来的程序员不会觉得他们在写程序，而是再为每个应用创建一个新的语言。


Friedman 和 Wand的这本书将会改变程序语言课程。本书的核心是一系列的解释器。初始是一个抽象的高级语言，然后逐渐的往里面增加语言特性，直到最后到达带状态的机器。你可以运行这些代码，研究并且进行修改。自行定义变量作用域，参数传递，控制结构等特性。

在学习完语言的执行后，作者会向我们展示在不运行程序的情况下，如何去分析程序。其中两章会讲到类型检查与类型推导，以及这些特性如何与现代的面向对象语言交互。

本书采用了Scheme语言。Scheme有着Lisp一样统一的语法和的数据抽样能力以及Algol一样的词法作用域和块状的代码结构。但是一个强大的工具只有在掌握它的人手上才能产生出力量。本书中的解释器都是可执行的模型，我认为这些解释器和分析器，将是许多程序系统的核心。

想掌握解释器并不容易。对于应用开发程序员来说，程序语言设计者是相当遥远。在设计应用程序时，你思考需要执行的特定任务，考虑需要包含的特性。但是在设计一个语言时，你需要考虑各种人想要开发的各种不同的应用以及实现它们的方式。你的语言是静态作用域还是动态作用域，还是两者皆有？是否需要有继承？函数调用时是传址还是传值？continuations是显式还是隐式？这完全取决于你期望语言如何被使用，什么样的程序用它来写更容易，什么程序用它来写更复杂。

此外，解释器也是极其精巧的程序。一行代码的简单改动，会导致目标语言执行行为的极大不同。世界上极少的人，能够看一眼一个新的解释器，就能预测这个解释器在执行相对简单的程序上的行为。所以，学习解释器时，最好能运行它们，先用它们去执行简单的表达式，然后是更复杂的表达式。添加调试信息。修改解释器，加入你自己的设计。尝试去真正的掌握这些程序，而不是走马观花的有个模糊印象。

如果你做到了这些，你会改变对编程的看法以及对自己作为程序员的看法。你会发现自己成为了程序语言的设计者，而不是使用者。是你选择一个语言应该有哪些功能，而不是成为使用别人选择的功能的程序语言的跟随者。


## 第三版附言

上述的前言是7年前编写。从那时起，信息应用和服务进入了人们的生活，在1990年看起来是不可思议的。这是不断增长的编程语言和程序框架的作用-这些都基于增长的解释器平台。

当你想要创建网站时。在1990年，这意味着格式化的静态文字和图片，创建一个浏览器上运行的程序，执行“print”语句。今天的动态网站大多利用脚本语言Javascript（或者说被解释执行的语言）。浏览器中运行的程序可以非常复杂，包含对网站服务器的异步请求。服务器通常也是一组包含多种服务功能的程序集合，这些不同的程序可能是用不同的编程语言编写而成。

或者你想要编写一个网络在线游戏中的bot，那么你可能在使用像Lua一样的脚本语言，可能会带一些面向对象的功能的扩展去表达类和行为。

或者你是编写集群中的程序，在全球范围创建索引，执行查询。那么你可能在使用函数式语言中的map-reduce概念去帮助你处理单个程序被调度的行为。

或者你在开发传感器网络中的新算法，探索如何使用惰性求值去更好的处理并发和数据聚合。或者为了控制网页，去研究像XSLT类似的转换系统。或者设计多媒体流合成转换框架。或者...

如此多的新应用！如此多的新语言！如此多的解释器！

一如既往，新手程序员，或者有经验的程序员，能够独自处理新的框架，使用特定集合的规则。但是创造一个新的框架，需要对技术的完全掌握：理解不同语言中相同的原理，了解语言中的哪个特性更适合哪类型的程序，并且知道如何修改语言的解释器。这些就是你会从这本书中学到的技巧。

Hal Abelson

2007年9月