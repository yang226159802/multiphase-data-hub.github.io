# 多相流 Kaggle 数据集上传简要规范

目标：下载者能够根据上传文件，用 Python 读取速度、压力、界面等流场变量，并构造自己的训练集或可视化结果。

## 1. 必须包含的文件

```text
dataset-metadata.json
info.json
data/
```

推荐包含：

```text
README.md
load_example.py
checksums.sha256
```

其中 `info.json` 是核心说明文件，`README.md` 只需简短介绍并指向 `info.json`。

## 2. 数据文件

真实数据放在 `data/` 中。数据格式不强制统一，可接受：

```text
.npy / .npz / .h5 / .hdf5 / .zarr / NetCDF
.dat / .vtk / .vti / .vtu / .xdmf / EnSight / OpenFOAM
Gvol.000001 / V.000001 / P.000001 等无扩展名二进制文件
```

前两类常见格式只需在 `info.json` 中写清变量、shape、单位、网格和读取方式。

第三类无扩展名或求解器特定二进制文件必须额外说明：

```text
header 字节数
dtype
大小端
payload shape
vector 分量排列方式
reshape 顺序
```

并必须提供：

```text
load_example.py
```

## 3. 两/多相流变量要求

完整 CFD 流场数据原则上必须包含：

```text
速度变量
压力变量
界面变量
```

常见命名：

```text
速度：U / V / velocity / u,v,w
压力：P / p / pressure
界面：alpha / Gvol / VOF / phi / level_set
```

界面变量必须说明相位约定，例如 `Gvol=1` 表示哪一相。

其他变量可选上传，例如曲率、界面法向量、涡量、温度、组分、密度场、黏度场等。

固定工况参数不要作为默认流场变量上传，应写入 `info.json`，例如：

```text
rho_l, rho_g, mu_l, mu_g, surface tension, gravity, Re, We, Oh
```

## 4. 网格要求

均匀网格不必上传单独的网格/几何文件，但 `info.json` 必须写清：

```text
网格尺寸
物理范围
dx / dy / dz
坐标顺序
cell-centered 或 node-centered
边界条件
```

非均匀网格、曲线网格或非结构网格必须上传相应的网格/几何/坐标文件。

## 5. `dataset-metadata.json`

该文件通常由 Kaggle CLI 自动生成：

```bash
kaggle datasets init -p <path/to/dataset>
```

生成后需要人工编辑：

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

其中 `kaggle-user` 必须与 Kaggle 用户名一致。

## 6. `info.json`

`info.json` 至少应包含：

```text
dataset_id
title
description
format
variables
grid
physics / 工况参数
contributors
license
doi / citation
local 文件路径列表
```

要求：

```text
info.json 中列出的文件必须真实存在。
上传了哪些变量，就只写哪些变量。
```

## 7. 上传前检查

上传前确认：

```text
dataset-metadata.json 可解析
info.json 可解析且文件路径正确
速度、压力、界面变量说明清楚
网格可由文件或元数据恢复
相位约定已说明
至少一个样本能用 Python 读取
无扩展名二进制文件提供 load_example.py
license 和 citation 清楚
```

