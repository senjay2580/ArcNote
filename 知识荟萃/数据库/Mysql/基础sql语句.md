

## 🧱 一、DDL（数据定义语言）

~~~sql
-- 创建数据库
CREATE DATABASE school;

-- 创建表
CREATE TABLE student (
    student_id INT PRIMARY KEY,                            -- 主键约束
    name VARCHAR(50) NOT NULL,                             -- 非空约束
    age TINYINT CHECK (age BETWEEN 18 AND 30),             -- CHECK 约束（MySQL 8.0 支持）
    gender CHAR(1) DEFAULT 'M' CHECK (gender IN ('M','F')),-- 默认值 + CHECK 约束
    email VARCHAR(100) UNIQUE,                             -- 唯一约束
    class_id INT,                                          -- 外键（关联班级）
    
    -- 定义外键约束：引用 class 表的主键
    CONSTRAINT fk_class FOREIGN KEY (class_id) REFERENCES class(class_id)
        ON DELETE SET NULL ON UPDATE CASCADE
    CONSTRAINT chk_salary CHECK (salary >= 1000),
    CONSTRAINT uq_emp_name UNIQUE (emp_name)
);


-- 修改表
-- 添加新列
ALTER TABLE student ADD phone VARCHAR(20);

-- 修改列的数据类型
ALTER TABLE student MODIFY age TINYINT UNSIGNED;

-- 删除列
ALTER TABLE student DROP COLUMN phone;

-- 添加外键
ALTER TABLE student ADD CONSTRAINT fk_class2 FOREIGN KEY (class_id) REFERENCES class(class_id);

-- 删除外键
ALTER TABLE student DROP FOREIGN KEY fk_class2;;

-- 删除表
DROP TABLE student;

-- 删除数据库
DROP DATABASE school;
```

~~~



## ✏️ 二、DML（数据操作语言）

```sql
-- 插入数据
INSERT INTO student_backup (id, name, age)
SELECT id, name, age FROM student WHERE age < 20;

-- 查询数据
SELECT * FROM student;

-- 更新数据
UPDATE student
SET age = 22,
    email = 'zhangsan22@example.com'
WHERE id = 1;


TRUNCATE TABLE student;
# 把 student 表中的所有数据删除，但表还在，列结构、约束还在。
```

---

## 🔐 三、DCL（数据控制语言）

```sql
-- 创建一个只能从本机登录的用户
CREATE USER 'user1'@'localhost' IDENTIFIED BY 'password123';

-- 创建一个可以从任何主机访问的用户（不安全）
CREATE USER 'user2'@'%' IDENTIFIED BY 'pass456';

-- 创建指定 IP 段可以访问的用户（更安全）
CREATE USER 'user3'@'192.168.1.%' IDENTIFIED BY 'pass789';

-- 授权（给某个用户赋予权限）
-- 允许 user1 查询和插入 school 库中所有表
GRANT SELECT, INSERT ON school.* TO 'user1'@'localhost';
GRANT ALL PRIVILEGES ON school.* TO 'user1'@'localhost';
GRANT SELECT ON school.* TO 'user1'@'localhost' WITH GRANT OPTION;

-- 撤销权限
-- 回收 user1 的 INSERT 权限
REVOKE INSERT ON school.* FROM 'user1'@'localhost';

-- 回收所有权限（写两次）
REVOKE ALL PRIVILEGES, GRANT OPTION FROM 'user1'@'localhost';


-- 查看权限
SHOW GRANTS FOR 'user1'@'localhost';

-- 删除用户
DROP USER 'user1'@'localhost';

-- 修改密码
ALTER USER 'user1'@'localhost' IDENTIFIED BY 'newpassword456';
--  重命名用户

RENAME USER 'user1'@'localhost' TO 'user_renamed'@'localhost';

```



| 权限名称       | 作用描述                        |
| -------------- | ------------------------------- |
| `SELECT`       | 查询数据                        |
| `INSERT`       | 插入数据                        |
| `UPDATE`       | 修改数据                        |
| `DELETE`       | 删除数据                        |
| `ALL`          | 所有权限（慎用）                |
| `CREATE`       | 创建表/数据库                   |
| `DROP`         | 删除表/数据库                   |
| `ALTER`        | 修改表结构                      |
| `INDEX`        | 创建/删除索引                   |
| `GRANT OPTION` | 再授权权限                      |
| `EXECUTE`      | 执行存储过程/函数（MySQL 5.0+） |

---

## 🔁 四、==游标（Cursor）==

游标（Cursor）是一种数据库对象，用于**逐行遍历查询结果集**。

在 SQL 中，通常查询是集合操作，一次性返回多行；游标允许我们**一行一行地处理数据**，更像编程语言中的迭代器。



- **逐行处理复杂业务逻辑**：当需要对查询结果的每一行单独操作，比如更新、调用存储过程等，游标非常有用。
- **处理集合操作无法直接完成的任务**：某些逻辑无法用单条 SQL 完成，游标提供编程式处理能力。
- **实现批量操作的细粒度控制**：比如批量更新时需要逐条校验。

```sql
DELIMITER //

CREATE PROCEDURE increase_age_for_minors()
BEGIN
    -- 1. 定义变量标记是否遍历结束
    DECLARE done INT DEFAULT FALSE;
    -- 2. 定义游标取出需要处理的学生ID和年龄
    DECLARE sid INT;
    DECLARE sage INT;

    -- 3. 定义游标，查找所有年龄小于18岁的学生
    DECLARE cur CURSOR FOR
        SELECT id, age FROM student WHERE age < 18;

    -- 4. 定义异常处理器，游标读取结束时设置 done = TRUE
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- 5. 打开游标
    OPEN cur;

    -- 6. 循环读取游标数据
    read_loop: LOOP
        FETCH cur INTO sid, sage;          -- 取出一条记录的id和age
        IF done THEN                      -- 判断是否取完
            LEAVE read_loop;              -- 结束循环
        END IF;

        -- 7. 对当前学生年龄加1
        UPDATE student SET age = sage + 1 WHERE id = sid;
    END LOOP;

    -- 8. 关闭游标，释放资源
    CLOSE cur;
END //

DELIMITER ;

```

---

## 🛠️ 五、==存储过程==

存储过程是 **预编译的 SQL 语句块**，存储在数据库中，可以被反复调用，**封装逻辑、提高效率、增强安全性**。

delimiter   分隔符

游标用于遍历多条数据；

`INOUT` 参数既能传入，也能修改返回

`DECLARE CONTINUE HANDLER` 用于捕获游标取数据结束的异常；

过程最后用 `SELECT` 返回结果集（非输出参数）；

使用 `DELIMITER` 更改分隔符避免语句冲突。

```sql
DELIMITER //

CREATE PROCEDURE SampleProcedure(
    IN inputId INT,               -- 输入参数
    OUT outputName VARCHAR(50),   -- 输出参数
    INOUT inoutAge INT            -- 输入输出参数
)
BEGIN
    -- 变量声明
    DECLARE done INT DEFAULT 0;
    DECLARE tempName VARCHAR(50);
    DECLARE tempAge INT;

    -- 游标声明：查询符合条件的多条记录
    DECLARE cur CURSOR FOR
        SELECT name, age FROM student WHERE id >= inputId;

    -- 异常处理：游标取完时设置 done=1
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    -- 初始化输出参数
    SET outputName = '';

    -- 打开游标
    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO tempName, tempAge;
        IF done = 1 THEN
            LEAVE read_loop;  -- 退出循环
        END IF;

        -- 处理逻辑示例：把第一个名字赋值给输出参数
        IF outputName = '' THEN
            SET outputName = tempName;
        END IF;

        -- 简单条件判断示例
        IF tempAge > 25 THEN
            SET inoutAge = tempAge;  -- 更新输入输出参数
        END IF;

        -- 这里可以执行更多逻辑，比如更新某些记录
        -- UPDATE student SET age = age + 1 WHERE name = tempName;

    END LOOP;

    CLOSE cur;

    -- 返回结果集示例
    SELECT id, name, age FROM student WHERE id = inputId;

END //

DELIMITER ;

```

---

## 🔗 六、WITH 子句（公用表表达式）

​	`WITH` 子句用于定义一个**临时的结果集**（相当于临时视图），这个结果集可以在后续的主查询中多次引用，使得 SQL 语句更清晰、更易读、结构更清楚。

**with recursive**

~~~~sql
WITH GRANT OPTION
with check option
~~~~



---





~~~sql
~~~



```sql
-- 查询成绩排名前 3 的学生
WITH top_scores AS (
    SELECT student_id, score
    FROM scores
    ORDER BY score DESC
    LIMIT 3
)
SELECT s.student_id, st.name, s.score
FROM top_scores s
JOIN student st ON s.student_id = st.id;
```

---

## 🧷 七、约束（包括 CHECK）

```sql
CREATE TABLE employee (
    id INT PRIMARY KEY,  -- 主键，唯一且非空

    name VARCHAR(50) NOT NULL,  -- 非空约束

    age INT,
    CONSTRAINT chk_age CHECK (age >= 18 AND age <= 65),  -- 年龄范围检查（CHECK）

    gender ENUM('M', 'F') DEFAULT 'M',  -- 限定性别的取值，默认男

    salary DECIMAL(10, 2) DEFAULT 5000 CHECK (salary >= 0), -- 默认值+非负薪资限制

    email VARCHAR(100) UNIQUE,  -- 邮箱唯一约束

    department_id INT,  -- 外键字段，指向部门表

    CONSTRAINT fk_dept FOREIGN KEY (department_id) REFERENCES department(id)  -- 外键约束

    -- 你也可以加：CONSTRAINT uq_name UNIQUE (name) -- 姓名不能重复（如果业务需要）
);

ALTER TABLE employee
ADD CONSTRAINT fk_dept FOREIGN KEY (department_id) REFERENCES department(id)
ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE employee
ADD CONSTRAINT uq_email UNIQUE (email);

ALTER TABLE employee
ADD CONSTRAINT chk_age CHECK (age BETWEEN 18 AND 65);

```

---

## 👓 八、视图（View）

```sql
-- 创建视图
CREATE VIEW young_students AS
SELECT id, name, age FROM student WHERE age < 25
WITH CHECK OPTION;
# 确保对视图的更新不会让数据跳出 age < 25 条件。
# 如果试图把 age 改成 26，会报错，保证视图数据的完整性

-- 使用视图
SELECT * FROM young_students;

-- 更新视图（只在某些简单视图上可行）
UPDATE young_students SET age = 24 WHERE id = 1;

-- 删除视图
DROP VIEW young_students;
```

**性能依赖基表**，**不是物理存储**

更新受限，复杂视图不可更新

不能包含参数，不能像**存储过程**那样灵活

---

## 🧾 九、==审计（Audit）==**（MySQL 原生不支持，需要插件）**

MySQL 通常借助插件（如 `audit_log`）或使用触发器模拟审计：

```sql
-- 创建审计表
CREATE TABLE audit_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    operation_type VARCHAR(20),
    table_name VARCHAR(50),
    operation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 示例触发器
DELIMITER //

CREATE TRIGGER log_student_insert
AFTER INSERT ON student
FOR EACH ROW
BEGIN
    INSERT INTO audit_log(operation_type, table_name)
    VALUES ('INSERT', 'student');
END //

DELIMITER ;
```

---

## 🧠 十、高级 SQL 查询

### 1. 子查询

```sql
-- 查询成绩最高的学生
SELECT * FROM student
WHERE id = (SELECT student_id FROM scores ORDER BY score DESC LIMIT 1);
```

### 2. 聚合函数 + 分组

```sql
SELECT gender, COUNT(*) AS count, AVG(age) AS avg_age
FROM student
GROUP BY gender;
```



### 3. 窗口函数（仅支持 MySQL 8+）

```sql
SELECT name, score,
       RANK() OVER (ORDER BY score DESC) AS score_rank
FROM scores;
```

### 4. EXISTS 子句

```sql
-- 查询至少有一门成绩大于90的学生
SELECT * FROM student s
WHERE EXISTS (
    SELECT 1 FROM scores sc
    WHERE sc.student_id = s.id AND sc.score > 90
);
```



# ==sql语句的执行顺序==

~~~sql
SELECT DISTINCT
    s.name, sc.course_id, sc.score
FROM
    student s
JOIN
    score sc ON s.id = sc.student_id
WHERE
    sc.score >= 60
GROUP BY
    s.name, sc.course_id
HAVING
    AVG(sc.score) > 70
ORDER BY
    s.name ASC
LIMIT 5;

~~~

| 执行顺序 | 关键字     | 说明（干什么用）                             |
| -------- | ---------- | -------------------------------------------- |
| 1        | `FROM`     | 确定要操作的表或视图，执行连接（JOIN）       |
| 2        | `ON`       | 多表连接时的连接条件                         |
| 3        | `JOIN`     | 把表连接成一个大表（结果集）                 |
| 4        | `WHERE`    | 过滤不符合条件的原始数据行                   |
| 5        | `GROUP BY` | 对过滤后的数据进行分组                       |
| 6        | `HAVING`   | 对分组结果进行条件过滤                       |
| 7        | `SELECT`   | 决定最终要显示哪些字段                       |
| 8        | `DISTINCT` | 去重（如果有）                               |
| 9        | `ORDER BY` | 对最终结果排序 基本上是最后了 如果不考虑分页 |
| 10       | `LIMIT`    | 取出前 N 条记录（分页/限制）                 |