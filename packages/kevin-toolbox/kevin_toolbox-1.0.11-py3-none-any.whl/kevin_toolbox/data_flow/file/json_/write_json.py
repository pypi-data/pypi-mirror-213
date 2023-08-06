import os
import json
import copy
from kevin_toolbox.data_flow.file.json_.converter import integrate
from kevin_toolbox.computer_science.algorithm.for_nested_dict_list import traverse


def write_json(content, file_path, sort_keys=False, converters=None):
    file_path = os.path.abspath(file_path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    if converters is not None:
        converter = integrate(converters)
        content = traverse(var=[copy.deepcopy(content)],
                           match_cond=lambda _, __, v: not isinstance(v, (list, dict)), action_mode="replace",
                           converter=lambda _, x: converter(x))[0]

    with open(file_path, 'w') as f:
        json.dump(content, f, indent=4, ensure_ascii=False, sort_keys=sort_keys)
