class Trigger:
    def __init__(self):
        """
            触发器
                通过 self.update() 来接收并监视 state_dict，
                当 state_dict 全部或部分发生变化时，将会把【发生变化的部分】
                传入绑定的函数中，并执行一次该函数。
        """

        self.last_state = dict()
        self.func_ls = []

    def bind(self, target):
        """
            绑定函数

            参数：
                target:     <func/list of func>
        """
        if not isinstance(target, (list, tuple,)):
            target = [target]
        for func in target:
            assert callable(func)
        self.func_ls.extend(target)

    def update(self, cur_state):
        """
            更新状态，决定是否触发
        """
        assert isinstance(cur_state, (dict,))

        new_state = dict()
        for key, value in cur_state.items():
            if key not in self.last_state or self.last_state[key] != value:
                new_state[key] = value

        if len(new_state) > 0:
            for func in self.func_ls:
                func(new_state)
            self.last_state.update(new_state)

        return new_state
