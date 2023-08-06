from kevin_toolbox.computer_science.algorithm.for_nested_dict_list import traverse


def get_leaf_nodes(var):
    """
        获取嵌套字典列表 var 中所有叶节点
            以列表 [(name,value), ...] 形式返回，其中名字 name 的解释方式参考 get_value_by_name() 介绍

        参数：
            var:                待处理数据
                                    当 var 不是 dict 或者 list 时，返回空列表
    """
    res = []

    def func(_, idx, v):
        nonlocal res
        if not isinstance(v, (list, dict,)):
            res.append((idx, v))
        return False

    traverse(var=var, match_cond=func, action_mode="skip", b_use_name_as_idx=True)
    return res
