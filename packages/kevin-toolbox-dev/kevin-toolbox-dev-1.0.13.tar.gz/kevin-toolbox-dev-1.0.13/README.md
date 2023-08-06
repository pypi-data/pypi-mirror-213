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

- v 1.0.13（2023-06-14）
  - computer_science.algorithm.for_nested_dict_list
    - 添加 copy_() 方法用于复制嵌套字典列表，支持深拷贝（复制结构和叶节点）和浅拷贝（仅复制结构，不新建叶节点）
    - 将 get_leaf_nodes() 修改成 get_nodes()，新增了 level 参数用于支持获取某一层的参数，原来的 get_leaf_nodes(var) 等效于 get_nodes(var,level=-1)
    - 修改 traverse()，增加了 b_traverse_matched_element 参数用于控制，对于匹配上的元素，经过处理后，是否继续遍历该元素的内容。
    
  - patches.for_test

    - modify check_consistency()

  - computer_science.algorithm.registration

    - 修改了 Registry.add() 中对于参数 b_force 的行为，对于 b_force：

      - 默认为 False，此时当 name 指向的位置上已经有成员或者需要强制修改database结构时，将不进行覆盖而直接跳过，注册失败
      - 当设置为 True，将会强制覆盖

      该改动的目的是避免对已有的成员进行重复的注册更新。



