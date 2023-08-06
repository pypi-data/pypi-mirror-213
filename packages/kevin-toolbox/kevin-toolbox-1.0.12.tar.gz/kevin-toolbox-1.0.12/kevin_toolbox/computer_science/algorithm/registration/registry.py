import re
import inspect
import pkgutil
import weakref
from kevin_toolbox.computer_science.algorithm.for_nested_dict_list import get_value_by_name, set_value_by_name, \
    traverse, count_leaf_node_nums


class Registry:
    """
        注册器
            具有以下功能
            - 管理成员，包括添加 add()、获取 get() pop() 成员等
            - 支持通过装饰器 register() 来添加成员
            - 支持通过 collect_from() 搜索指定的路径，当该路径下的模块被 register() 装饰器包裹时，将自动导入（用于解决python中的模块是惰性的问题）

        使用方法：
            以目录结构：
                xx/——— modules_dir
                 |       |——— a.py
                 |       |___ ...
                 |——— test.py
            为例。
            我们的目标是在 test.py 中，构建一个能够自动加载 modules_dir 中待注册成员的 Registry 实例。
            具体步骤如下：
                1. 在文件 test.py 中：
                    # 创建注册器实例
                    DB = Registry(uid="DB")
                    # 设置搜索路径
                    DB.collect_from(path_ls=["xx/modules_dir"])

                2. 在 modules_dir 下需要加载的成员中，以 a.py 为例：
                    # 导入注册器实例
                    from xx.test import DB
                    # 使用 DB.register() 装饰器注册
                    @DB.register(name=":my_module")
                    class A:
                        ...
                    # 使用 add() 函数注册
                    DB.add(obj=233, name=":var:c")

                3. 在文件 test.py 中：
                    # 获取已注册成员
                    module = DB.get(name=":my_module")

                4. 如果需要在其他文件中获取已有注册器实例，除了用 import 之外，还可以直接用 uid
                    # 获取指定 uid 下的实例
                    temp = Registry(uid="DB")
    """
    name = "registry made by kevin"
    __instances = weakref.WeakValueDictionary()  # {uid: instance_i, ...} 用于保存创建的实例
    __counter = 0

    def __new__(cls, *args, **kwargs):
        """
            __new__函数返回的实例，将作为self参数被传入到__init__函数。
                如果__new__函数返回一个已经存在的实例（不论是哪个类的），__init__还是会被调用的，所以要特别注意__init__中对变量的赋值。
        """
        uid = kwargs.get("uid", cls.__counter)

        # 获取实例
        if uid in cls.__instances:
            # 返回已存在的实例
            self = cls.__instances[uid]
        else:
            # 传入 __init__ 中新建一个实例
            self = super().__new__(cls)
        return self

    def __init__(self, *args, **kwargs):
        """
            参数：
                uid:                <hashable> 实例的唯一标识符
                                        默认置空，此时将新建一个实例，并将此时已有实例的数量作为 uid
                                        当为非空，则根据 uid 到已有实例中寻找相同的实例，并返回（使用该特性可以构造单例模式）
        """
        try:
            getattr(self, "uid")
        except:
            pass
        else:
            return  # 如果是从 __new__ 中获取的已有的实例则不重复进行参数赋值
        self.database = dict()
        #
        self.uid = kwargs.get("uid", Registry.__counter)
        self.inactivate_b_force_of_add = False
        # 记录到 __instances 中
        Registry.__instances[self.uid] = self
        Registry.__counter += 1

    def add(self, obj, name=None, b_force=False):
        """
            注册

            参数：
                obj：            待注册成员
                                    可以是函数、类或者callable的实例
                                    也可以是各种 int、float、str变量
                                    总之一切对象皆可
                name：           <str> 成员名称
                                    默认为 None，此时将从被注册对象 obj 的属性中尝试推断出其名称。
                                        若 obj 中有 name 或者 __name__ 属性（优先选择name），则推断出的名称是 f':{obj.name}'；
                                            进一步若有 version 属性，则为 f':{obj.name}:{obj.version}'
                                        否则报错。
                                        比如下面的类：
                                            class A:
                                                version="1.0"
                                        的默认注册名称将是 ":A:1.0"
                                    对于 int、str 和其他没有 name 或者 __name__ 属性的变量则必须要手动指定 name 参数。
                        需要注意的是，成员的名称确定了其在注册器内部 database 中的位置，名称的解释方式参考 get_value_by_name() 中的介绍。
                        因此不同的名称可能指向了同一个位置。
                b_force：          <boolean> 是否强制注册
                                    默认为 False，此时当 name 指向的位置上已经有成员时，将不进行覆盖而直接报错
                                    当设置为 True，将会强制覆盖
        """
        # 检验参数
        if name is None:
            name = getattr(obj, "name", getattr(obj, "__name__", None))
            if name is not None:
                name = f':{name}'
                version = getattr(obj, "version", None)
                if version is not None:
                    name += f':{version}'
        assert isinstance(name, (str,))

        # 尝试注册
        temp = self.database.copy()
        set_value_by_name(var=temp, name=name, value=obj, b_force=True)
        # check
        if not self.inactivate_b_force_of_add and not b_force:
            inc_node_nums = count_leaf_node_nums(var=obj) if isinstance(obj, (list, dict)) else 1  # 增加的节点数量
            assert count_leaf_node_nums(var=temp) == count_leaf_node_nums(var=self.database) + inc_node_nums, \
                f'registration failed, it may be a conflict with an existing member'
        self.database = temp

    def get(self, name, **kwargs):
        """
            获取

            参数：
                name：           <str> 成员名称
                default:          默认值
                                    找不到时，若无默认值则报错，否则将返回默认值
        """
        try:
            return get_value_by_name(var=self.database, name=name)
        except:
            if "default" in kwargs:
                return kwargs["default"]
            else:
                raise AssertionError(f'element {name} not exists')

    def pop(self, name, **kwargs):
        """
            弹出

            参数：
                name：           <str> 成员名称
                                    名称一定要准确，不能含有模糊的 | 字符
                default:          默认值
                                    找不到时，若无默认值则报错，否则将返回默认值
        """
        assert "|" not in name, \
            f'to pop up a specific member needs to give the exact name, ' \
            f'does not support the "|" character with automatic deduction, invalid name: {name}, ' \
            f'what you probably want to pop is {name.replace("|", ":")}'
        res, b_found = None, False

        def func(_, idx, value):
            nonlocal res, b_found
            if res is None and idx == name:
                res, b_found = value, True
                return True
            else:
                return False

        traverse(var=self.database, match_cond=func, action_mode="remove", b_use_name_as_idx=True)
        if b_found:
            return res
        else:
            if "default" in kwargs:
                return kwargs["default"]
            else:
                raise AssertionError(f'element {name} not exists')

    def clear(self):
        self.database.clear()

    # -------------------- 装饰器 --------------------- #

    def register(self, name=None, b_force=False):
        """
            用于注册成员的装饰器
                成员可以是函数、类或者callable的实例

            参数：
                name：           <str> 成员名称
                                    默认为 None
                b_force：        <boolean> 是否强制注册
                                    默认为 False
                                （以上参数具体参考 add() 函数介绍）
        """

        def wrapper(obj):
            nonlocal self, name, b_force
            self.add(obj, name=name, b_force=b_force)
            return obj

        return wrapper

    # -------------------- 其他 --------------------- #

    def collect_from(self, path_ls):
        """
            遍历 path_ls 下的所有模块，并自动导入其中被 register() 装饰器包裹的部分
                注意，自动导入时使用的 add() 方法中的 b_force 将强制设置为 True
                这意味着不再检查可能冲突的添加项
        """
        temp = None
        for loader, module_name, is_pkg in pkgutil.walk_packages(path_ls):
            module = loader.find_module(module_name).load_module(module_name)
            if temp is None:
                for name, obj in inspect.getmembers(module):
                    if getattr(obj, "name", None) == Registry.name and getattr(obj, "uid") == self.uid:
                        temp = obj
                        temp.inactivate_b_force_of_add = True
                        break
        if temp is not None:
            self.database = temp.database


UNIFIED_REGISTRY = Registry(uid="UNIFIED_REGISTRY")
