def traverse(var, match_cond, action_mode="remove", converter=None, b_use_name_as_idx=False):
    """
        遍历 var 找到符合 match_cond 的元素，将其按照 action_mode 指定的操作进行处理

        参数：
            var:                待处理数据
                                    当 var 不是 dict 或者 list 时，将直接返回 var 而不做处理
            match_cond:         <func> 元素的匹配条件
                                    函数类型为 def(parent_type, idx, value): xxxx
                                    其中：
                                        parent_type     该元素源自哪种结构体，有两个可能传入的值： list，dict
                                        idx             该元素在结构体中的位置
                                                            当 b_use_name_as_idx=False 时，
                                                                对于列表是 index，对于字典是 key
                                                            当为 True 时，传入的是元素在整体结构中的 name 位置，name的格式和含义参考
                                                                get_value_by_name() 中的介绍
                                        value           元素的值
            action_mode:        <str> 如何对匹配上的元素进行处理
                                    目前支持：
                                        "remove"        将该元素移除
                                        "replace"       将该元素替换为 converter() 处理后的结果
                                        "skip":          不进行任何操作
            converter:          <func> 参见 action_mode 中的 "replace" 模式
                                    函数类型为 def(idx, value): xxxx
                                    其中 idx 和 value 的含义参见参数 match_cond 介绍
            b_use_name_as_idx     <boolean> 对于 match_cond/converter 中的 idx 参数，是传入整体的 name 还是父节点的 index 或 key。
                                    默认为 False
    """
    assert callable(match_cond)
    assert action_mode in {"replace", "remove", "skip"}
    if action_mode == "replace":
        assert callable(converter)

    return recursive_(var, match_cond, action_mode, converter, b_use_name_as_idx, "")


def recursive_(var, match_cond, action_mode, converter, b_use_name_as_idx, pre_name):
    if isinstance(var, (list, dict)):
        items = reversed(list(enumerate(var))) if isinstance(var, list) else list(var.items())
        for k, v in items:
            if b_use_name_as_idx:
                idx = f'{pre_name}@{k}' if isinstance(var, list) else f'{pre_name}:{k}'
            else:
                idx = k
            if match_cond(type(var), idx, v):
                if action_mode == "remove":
                    var.pop(k)
                elif action_mode == "replace":
                    var[k] = converter(idx, v)
                else:
                    pass
            else:
                var[k] = recursive_(v, match_cond, action_mode, converter, b_use_name_as_idx, idx)
    else:
        pass
    return var
