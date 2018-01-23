# Kubernetes Object file version converter

Convert API Object file into specified version.

## Usage

### Query

`kube-ver-conv.py query [Object Kind]`

**Example**

```
$ ./kube-ver-conv.py query DaemonSet

1.5: extensions/v1beta1

1.6: extensions/v1beta1

1.7: extensions/v1beta1

1.8: apps/v1beta2

1.9: apps/v1
```

---

# 中文版

转换 Kuberntes API Object 到指定版本。

## 用法

### 查询

`kube-ver-conv.py query [对象类型]`

**例如**：

```
$ ./kube-ver-conv.py query DaemonSet

1.5: extensions/v1beta1

1.6: extensions/v1beta1

1.7: extensions/v1beta1

1.8: apps/v1beta2

1.9: apps/v1
```
