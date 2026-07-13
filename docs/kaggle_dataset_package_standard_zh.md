# 多相流 Kaggle 数据集上传文件规范

目标：下载者应能根据上传文件，用 Python 读取两/多相流场数据，并按自己的任务构造训练集、测试集或可视化结果。

本规范不强制统一数据格式，但要求元数据清楚、变量含义明确、字段数据可读取。

## 一、推荐文件结构

每个 Kaggle 数据集建议包含：

```text
dataset-metadata.json
info.json
README.md
load_example.py
checksums.sha256
data/
```

其中：

```text
必须：dataset-metadata.json, info.json, data/
强烈推荐：load_example.py, README.md, checksums.sha256
```

## 二、`dataset-metadata.json`

这是 Kaggle 上传所需文件。

根据 BlastNet 的教程，通常通过以下命令自动生成：

```bash
kaggle datasets init -p <path/to/dataset>
```

生成后需要手动填写：

```json
{
  "title": "Dataset title",
  "id": "kaggle-user/dataset-slug",
  "licenses": [
    {
      "name": "CC-BY-4.0"
    }
  ]
}
```

注意：

- `id` 中的 `kaggle-user` 必须和 Kaggle 用户名一致；
- `dataset-slug` 建议只用小写字母、数字和连字符；
- license 不能随便填写，未确定前建议先保持 private。

## 三、`info.json`

`info.json` 是最重要的元数据文件，应作为数据集说明的权威来源。

它至少应包含：

```text
global：整个数据集的信息
local：每个 snapshot / case / sample 的文件路径和时间信息
```

### `global` 必须包含

```text
dataset_id
title
description
format
snapshots 或 sample 数量
variables
grid
physics
contributors
license
doi 或引用说明
known_limitations
```

### `local` 必须包含

```text
snapshot / sample id
time，如果有
每个变量对应的文件路径
```

重要要求：

```text
info.json 中列出的文件必须真实存在。
如果只上传了 Gvol，就不要在 info.json 中写 V 或 P 的文件路径。
```

## 四、`data/`

`data/` 存放实际流场数据。

可接受的数据类型包括：

```text
1. 已处理好的数组格式：
   .npy, .npz, .h5, .hdf5, .zarr, NetCDF

2. 常见 CFD / 可视化格式：
   .dat, .vtk, .vti, .vtu, .vtr, .xdmf + .h5, EnSight, OpenFOAM 等

3. 无扩展名或求解器特定二进制文件：
   Gvol.000001, V.000001, P.000001, VOF.000001 等
```

前两类格式较常见，只要在 `info.json` 中写清变量、shape、单位、网格和读取方式即可。

第三类二进制文件必须额外说明：

```text
header 字节数
dtype
大端 / 小端
payload shape
vector 分量排列方式
reshape 顺序
文件路径规则
单位
网格尺寸和坐标约定
```

第三类数据必须提供：

```text
load_example.py
```

否则外部用户很难可靠读取。

## 五、两/多相流变量要求

对于完整两/多相流 CFD 数据集，推荐至少包含以下三类变量：

```text
速度变量
压力变量
界面变量
```

具体可以是：

```text
速度：u, v, w 或 V
压力：p 或 P
界面：alpha, Gvol, VOF, phi, level-set, interface mask 等
```

其中界面变量必须说明相位约定，例如：

```text
Gvol = 1 表示液相还是气相
Gvol = 0 表示哪一相
0 < Gvol < 1 是否表示界面单元
```

其他变量可选上传，例如：

```text
曲率：kappa, Gcurv
法向量：normal, Gnorm
密度场：rho
黏度场：mu
温度：T
组分：Y_i
涡量、应变率、耗散率等诊断量
```

注意：如果 `rho`、`mu`、`sigma`、`g` 是固定算例参数，通常不应作为场变量上传，而应写在 `info.json` 的物理参数中。

## 六、`load_example.py`

强烈推荐所有数据集提供。

对于无扩展名或求解器特定二进制文件，必须提供。

脚本应做到：

- 能从数据集根目录直接运行；
- 至少读取一个 snapshot 或 sample；
- 打印变量名、shape、dtype、min、max；
- 不依赖作者私有代码；
- 尽量使用常见 Python 库。

对于大数据集，读取一个文件或一个切片即可。

## 七、`README.md`

推荐提供，但应保持简洁。

不需要重复 `info.json` 的全部内容。

建议只写：

```text
数据集名称
一句话介绍
包含哪些变量
完整元数据见 info.json
读取示例见 load_example.py
引用方式或 DOI
```

## 八、`checksums.sha256`

推荐提供，用于校验文件完整性。

生成方式：

```bash
find . -type f ! -name checksums.sha256 -print0 | sort -z | xargs -0 sha256sum > checksums.sha256
```

## 九、其他可选文件

按需提供：

```text
figures/
scripts/
grid/
metadata/
case files
mesh files
```

例如：

- 预览图；
- 数据转换脚本；
- 训练/验证/测试集划分文件；
- 求解器输入文件；
- 网格或坐标文件；
- ParaView / EnSight / OpenFOAM 所需 case 文件。

如果网格是均匀直角网格，可以不上传坐标文件，但必须在 `info.json` 中写清：

```text
网格尺寸
物理范围
dx / dy / dz
坐标顺序
变量位置
```

如果网格不能由元数据恢复，则必须上传网格、坐标或 mesh 文件。

## 十、最小 `info.json` 示例

```json
{
  "schema_version": "0.1.0",
  "dataset_type": "multiphase_flow_simulation",
  "global": {
    "dataset_id": "kaggle-user/dataset-slug",
    "title": "Dataset title",
    "description": "Short dataset description.",
    "format": "custom binary",
    "snapshots": 1,
    "variables": ["Gvol", "V", "P"],
    "grid": {
      "type": "uniform_cartesian",
      "cell_dims": [256, 256, 256],
      "domain_bounds_xyz": [[-3.14159, 3.14159], [-3.14159, 3.14159], [-3.14159, 3.14159]],
      "field_location": "cell_centered",
      "coordinate_order": "x,y,z"
    },
    "physics": {
      "flow_type": "two_phase_flow",
      "configuration": "droplet breakup in homogeneous isotropic turbulence",
      "physical_parameters": {
        "density_liquid": "TBD",
        "density_gas": "TBD",
        "viscosity_liquid": "TBD",
        "viscosity_gas": "TBD",
        "surface_tension": "TBD"
      },
      "boundary_conditions": "TBD",
      "initial_conditions": "TBD"
    },
    "contributors": ["TBD"],
    "license": "TBD",
    "doi": "TBD",
    "known_limitations": []
  },
  "local": [
    {
      "id": 0,
      "snapshot_id": "000001",
      "time": {
        "value": null,
        "units": "TBD"
      },
      "files": {
        "Gvol": "./data/Gvol/Gvol.000001",
        "V": "./data/V/V.000001",
        "P": "./data/P/P.000001"
      }
    }
  ]
}
```

## 十一、上传前检查清单

上传或提交前，应确认：

- `dataset-metadata.json` 存在，且 Kaggle owner id 正确；
- `info.json` 存在；
- `info.json` 中列出的文件都真实存在；
- 速度、压力、界面变量是否包含，以及缺失原因是否说明；
- 变量单位、shape、dtype 已说明；
- 网格可以根据文件或元数据恢复；
- 相位约定已说明；
- 至少一个样本能用 Python 读取；
- 无扩展名或求解器特定二进制文件提供了 `load_example.py`；
- license 和 citation 信息清楚。

