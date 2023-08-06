# IBATS_Utils
IBATS 通用工具，该工具涉及数据库、量化、以及一些通用工具。

#### 版本历史
* 2021-06-21 \[1.20210623.0]
  > feat: add math module.\
  > feat: add get_file_name_iter.\
  > refactor: split mess funcs to separated modules.

* 2021-06-18 \[1.20210618.0]
  > fix: cls=SimpleJsonEncoder.

* 2021-06-07 \[1.20210607.1]
  > feat: enhance dict_2_jsonable, obj_2_json.\
  > fix: JsonEncoder, SimpleJsonEncoder on Enum value.\
  > feat: use CalVer

#### 编译命令
```bash
python setup.py build bdist_wheel
twine upload dist/*
```
