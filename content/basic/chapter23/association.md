---
title: "关联"
date: 2024-10-08T17:40:35+08:00
---

在前两节课中，我们讨论了两种类型的对象关系，即组合和聚合。其中复杂对象（整体）是由一个或多个简单对象（部分）构建的。

在本课中，将研究两个原本不相关的对象之间的较弱类型的关系，称为关联。与对象组合关系不同，在关联中，没有隐含的整体/部分关系。

***
## 关联

要符合关联的条件，对象和另一个对象必须具有以下关系：

1. 被关联的对象（成员）与当前对象（类）无整体/部分的关系
2. 被关联的对象（成员）可以同时属于多个对象（类）
3. 被关联的对象（成员）的生命周期不被当前对象（类）管理
4. 被关联的对象（成员）可能也可能不知道当前对象（类）的存在

对组合或聚合而言，代表的是整体和部分的关系。对于关联而言，关联的对象之间无这种关系。与聚合类似，被关联的对象，可以同时属于一个或多个对象，但是它不归这些对象所管理。对于聚合而言，关系是单向的，即一个对象是整体，一个对象是部分。关联的关系可能是双向的，两个对象可以互相感知到对方的存在。

医生和患者之间的关系是一个关联的关系。医生显然与他的病人有关系，但从概念上讲，这不是一种部分/整体（对象构成）关系。医生一天可以看许多患者，患者可以看许多医生（也许他们需要第二种意见，或者他们正在拜访不同类型的医生）。对象的生命周期都不与另一个对象绑定。

我们可以说，关联模型是“使用”关系。医生“使用”病人（赚取收入）。患者“使用”医生（治疗疾病）。

***
## 实现关联

关联是一种广泛存在关系，可以用许多不同的方法来实现它们。然而，大多数情况下，关联是使用指针实现的，其中当前对象指向关联的对象。

在本例中，我们将实现医生/患者双向关系，因为医生知道他们的患者是谁是有意义的，反之亦然。

```C++
#include <functional> // reference_wrapper
#include <iostream>
#include <string>
#include <string_view>
#include <vector>

// 因为 Doctor 和 Patient 循环依赖, 所以需要前向声明 Patient
class Patient;

class Doctor
{
private:
	std::string m_name{};
	std::vector<std::reference_wrapper<const Patient>> m_patient{};

public:
	Doctor(std::string_view name) :
		m_name{ name }
	{
	}

	void addPatient(Patient& patient);

	// 这个函数需要在 Patient 下面实现，因为这个函数的实现中，需要知道 Patient 的接口
	friend std::ostream& operator<<(std::ostream& out, const Doctor& doctor);

	const std::string& getName() const { return m_name; }
};

class Patient
{
private:
	std::string m_name{};
	std::vector<std::reference_wrapper<const Doctor>> m_doctor{}; // 这里记录看过的医生

	// 这个函数设置为private，因为不想它被任意调用
	// 需要使用 Doctor::addPatient(), 然后在其中调用本函数
	void addDoctor(const Doctor& doctor)
	{
		m_doctor.push_back(doctor);
	}

public:
	Patient(std::string_view name)
		: m_name{ name }
	{
	}

	friend std::ostream& operator<<(std::ostream& out, const Patient& patient);

	const std::string& getName() const { return m_name; }

	// 声明 Doctor::addPatient() 为友元函数，以便Doctor可以访问private函数 Patient::addDoctor()
	friend void Doctor::addPatient(Patient& patient);
};

void Doctor::addPatient(Patient& patient)
{
	// 这里doctor遇到patient
	m_patient.push_back(patient);

	// patient 也同样遇到 doctor
	patient.addDoctor(*this);
}

std::ostream& operator<<(std::ostream& out, const Doctor& doctor)
{
	if (doctor.m_patient.empty())
	{
		out << doctor.m_name << " has no patients right now";
		return out;
	}

	out << doctor.m_name << " is seeing patients: ";
	for (const auto& patient : doctor.m_patient)
		out << patient.get().getName() << ' ';

	return out;
}

std::ostream& operator<<(std::ostream& out, const Patient& patient)
{
	if (patient.m_doctor.empty())
	{
		out << patient.getName() << " has no doctors right now";
		return out;
	}

	out << patient.m_name << " is seeing doctors: ";
	for (const auto& doctor : patient.m_doctor)
		out << doctor.get().getName() << ' ';

	return out;
}

int main()
{
	// Patient 对象的创建在 Doctor 外部
	Patient dave{ "Dave" };
	Patient frank{ "Frank" };
	Patient betsy{ "Betsy" };

	Doctor james{ "James" };
	Doctor scott{ "Scott" };

	james.addPatient(dave);

	scott.addPatient(dave);
	scott.addPatient(betsy);

	std::cout << james << '\n';
	std::cout << scott << '\n';
	std::cout << dave << '\n';
	std::cout << frank << '\n';
	std::cout << betsy << '\n';

	return 0;
}
```

打印

```C++
James is seeing patients: Dave
Scott is seeing patients: Dave Betsy
Dave is seeing doctors: James Scott
Frank has no doctors right now
Betsy is seeing doctors: Scott
```

一般来讲，如果单向关联能实现逻辑，应该避免双向关联。因为双向关联增加了复杂性，往往很难在不出错的情况下编写完成。


***
## 自反关联

有时对象可能与相同类型的其它对象有关系。这被称为自反关联。自反关联的一个很好的例子是大学课程与先修课程之间的关系。

考虑一个简化的情况，一门课程只能有一个先修课程。可以这样做：

```C++
#include <string>
#include <string_view>

class Course
{
private:
    std::string m_name{};
    const Course* m_prerequisite{};

public:
    Course(std::string_view name, const Course* prerequisite = nullptr):
        m_name{ name }, m_prerequisite{ prerequisite }
    {
    }

};
```

这可能导致一系列关联（A课程有一个先修课程B，B课程有一个先修课程C，等等……）

***
## 间接关联

关联可以是间接的。在前面的所有情况下，我们都使用了指针或引用来直接将对象链接在一起。然而，在关联中，这并不是严格要求的。允许您将两个对象链接在一起的任何类型的数据都是足够的。在下面的示例中，展示了Driver类如何与Car具有单向关联，而不实际包括Car指针或引用：

```C++
#include <iostream>
#include <string>
#include <string_view>

class Car
{
private:
	std::string m_name{};
	int m_id{};

public:
	Car(std::string_view name, int id)
		: m_name{ name }, m_id{ id }
	{
	}

	const std::string& getName() const { return m_name; }
	int getId() const { return m_id; }
};

// carLot 是一个静态数组，装载了Car和查找的id
// 因为它是静态的，所以不需要分配一个CarLot对象
namespace CarLot
{
    Car carLot[4] { { "Prius", 4 }, { "Corolla", 17 }, { "Accord", 84 }, { "Matrix", 62 } };

	Car* getCar(int id)
	{
		for (auto& car : carLot)
        {
			if (car.getId() == id)
			{
				return &car;
			}
		}

		return nullptr;
	}
};

class Driver
{
private:
	std::string m_name{};
	int m_carId{}; // 通过 ID 而不是指针来进行关联

public:
	Driver(std::string_view name, int carId)
		: m_name{ name }, m_carId{ carId }
	{
	}

	const std::string& getName() const { return m_name; }
	int getCarId() const { return m_carId; }
};

int main()
{
	Driver d{ "Franz", 17 }; // Franz 车的 ID 是 17

	Car* car{ CarLot::getCar(d.getCarId()) }; // 从 car lot 中提车

	if (car)
		std::cout << d.getName() << " is driving a " << car->getName() << '\n';
	else
		std::cout << d.getName() << " couldn't find his car\n";

	return 0;
}
```

在上面的例子中，有一个carLot存放所有的汽车。需要汽车的驾驶员没有指向他的汽车的指针——相反，他有汽车的ID，当需要时，可以使用它从carLot中获取汽车。

在这个特定的例子中，这样做有点傻，因为将汽车从carLot中取出需要低效的查找（连接两者的指针要快得多）。然而，通过唯一的ID而不是指针引用事物是有好处的。例如，您可以引用当前不在内存中的内容（可能它们在文件或数据库中，并且可以按需加载）。此外，指针会占用4或8个字节——如果内存空间很少，并且唯一对象的数量相当低，则通过8位或16位整数引用它们可以节省大量内存。

***
## 组合vs聚合vs关联摘要

这里有一个摘要表，帮助您记住组合、聚合和关联之间的区别：

|  属性 |  组合  |  聚合 |  关联 |
|  ----  | ----  |  ----  |  ----  |
| 关系类型 | 部分-整体 | 部分-整体 | 相互关联 |
| 成员可以属于多个类 | 否 | 是 | 是 |
| 成员生命周期由类管理 | 是 | 否 | 否 |
| 关系指向 | 单向 | 单向 | 单向或双向 |
| 关系术语 | 一部分 | 有一个 | 使用一个 |

***

{{< prevnext prev="/basic/chapter23/aggregation/" next="/basic/chapter23/dependencies/" >}}
23.2 聚合
<--->
23.4 依赖关系
{{< /prevnext >}}
