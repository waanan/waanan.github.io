---
title: "第一个C++程序"
date: 2022-12-28T16:40:41+08:00
---

准备好开发环境后，编写第一个程序。

***

## 使用Visual Studio开发

1. 打开VS（Visual Studio），选择「创建新项目」。

在IDE中，「项目」代表打包生成程序所需的所有资源。
包括源代码，音频，数据文件，编译链接设置等。

当需要创建新程序时，重新创建新的项目。
不同的IDE的项目有不同的保存格式，一般无法打开其它IDE创建的项目。

{{< img src="./create_project.png" title="创建项目">}}

2. 选择控制台应用

学习C++的基础知识时，开始时选择「控制台应用」。

控制台应用，代表生成的程序，从命令行读取数据，或打印数据到命令行。
不涉及复杂的图形界面操作，同时不用修改可在不同操作系统运行，非常适合入门学习。

{{< img src="./console_project.png" title="选择项目类型">}}

3. 填写项目名称

填写项目名称「HelloWorld」。推荐选择「将解决方案和项目放在同一目录」。

单个解决方案里，可包含多个项目，这里暂时不展开。

{{< img src="./project_name.png" title="填写项目名称">}}

4. 运行项目

项目打开，右侧「资源管理器」包含解决方案和项目。
「源文件」中有「HelloWorld.cpp」。
在中间的编辑器中，看到「HelloWorld.cpp」的源代码。
点击「调试」-「开始执行不调试」，即可运行程序。

{{< img src="./project.png" title="编辑界面">}}

这时，窗口下方「输出」框里有如下文字，代表已编译成功。
编译的可执行文件是「D:\code\HelloWorld\x64\Debug\HelloWorld.exe」。

```bash
已启动生成...
1>------ 已启动生成: 项目: HelloWorld, 配置: Debug x64 ------
1>HelloWorld.cpp
1>HelloWorld.vcxproj -> D:\code\HelloWorld\x64\Debug\HelloWorld.exe
========== 版本: 1 成功，0 失败，0 更新，0 跳过 ==========
========== 占用时间 00:13.214 ==========
```

5. 查看运行效果

下图中，打印出「Hello World！」。

{{< img src="./result.png" title="运行结果">}}

***

## 使用命令行进行开发

首先在编辑器中输入如下代码。保存为「HelloWorld.cpp」。

```C++
#include <iostream>

int main()
{
    std::cout << "Hello World!" << std::endl;
    return 0;
}
```

使用「g++」对cpp文件进行编译。

```bash
g++ -o HelloWorld HelloWorld.cpp
```

编译完成后，当前目录下看见可执行文件「HelloWorld」。

如下命令执行，即可得到运行效果。

```bash
./HelloWorld
```

***

{{< prevnext prev="/basic/chapter0/install-dev-env/" next="/basic/chapter1/program-structure/" >}}
0.4 安装开发环境
<--->
1.0 程序结构介绍
{{< /prevnext >}}
