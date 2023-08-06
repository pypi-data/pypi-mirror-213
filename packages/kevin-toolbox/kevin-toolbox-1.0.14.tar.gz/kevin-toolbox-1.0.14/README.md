# kevin_toolbox

一个通用的工具代码包集合



环境要求

```shell
numpy>=1.19
pytorch>=1.2
```

安装方法：

```shell
pip install kevin-toolbox  --no-dependencies
```



[项目地址 Repo](https://github.com/cantbeblank96/kevin_toolbox)

[使用指南 User_Guide](./notes/User_Guide.md)

[免责声明 Disclaimer](./notes/Disclaimer.md)

[版本更新记录](./notes/Release_Record.md)：

- v 1.0.14（2023-06-14） 【bug fix】
  - computer_science.algorithm.registration
    - 将 Registry.collect_from() 修改为 Registry.collect_from_paths() 并增加了 b_execute_now 参数，用于控制延时导入。通过延时导入、以及调用文件函数的文件位置检查，避免了 TypeError: super(type, obj): obj must be an instance or subtype of type 的错误。

