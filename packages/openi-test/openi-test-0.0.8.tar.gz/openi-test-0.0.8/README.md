# This is a test package for OpenI PyPi

test package for OpenI 启智AI协作平台.

# 使用说明安装

```bash
pip install openi-test
```

## openi.dataset.upload_file()

> 上传数据集函数

安装完成可仿照下列示，运行即可上传数据集

```python
from openi.dataset import upload_file
upload_file(
    file = "", # 必填，文件路径(包含文件名)
    username = "", # 必填，数据集所属项目用户名
    repository = "", # 必填，数据集所属项目名
    token = "", #必填，用户启智上获取的令牌token，并对该项目数据集有权限
  
    cluster = "", # 选填，可填入GPU或NPU，不填写后台默认为NPU
    app_url = "" #选填, 默认为平台地址，用户不用填写，开发测试用
    )

from openi.utils import (
    get_code_path,
    get_data_path,
    get_pretrain_model_path,
    get_output_path,
    push_output_to_openi,
    obs_copy_folder
)
code_path = get_code_path()
```
