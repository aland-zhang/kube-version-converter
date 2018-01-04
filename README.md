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

### Convert

```
usage: kube-ver-conv.py convert [-h] [-s [file name]] [-d [file name]] -t
                                [output version] [-o [output format]]

optional arguments:
-h, --help            show this help message and exit
-s [file name], --source-file [file name]
                      YML or JSON file to process, '-' for STDIN.
-d [file name], --dest-file [file name]
                      File name for output, '-' for STDOUT.
-t [output version], --to-version [output version]
                      Kubernetes version of the out object file.
-o [output format], --output-format [output format]
                      Format of the output file, default is yaml
```

**Example**

`./kube-obj-ver-conv.py convert -s deploy.yaml  -d deploy.1.9.yaml -o yaml -t 1.9`


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

### 转换

```
用法: kube-ver-conv.py convert [-h] [-s [file name]] [-d [file name]] -t
                                [output version] [-o [output format]]

可选参数：
-h, --help            show this help message and exit
-s [file name], --source-file [file name]
                      待处理的 JSON 或 YAML 文件，缺省为 “-”，代表从 STDIN 输入。
-d [file name], --dest-file [file name]
                      输出文件名称，缺省为 “-”，代表输出到 STDOUT。
-t [output version], --to-version [output version]
                      指定输出为 Kuberntes 版本的文件。
-o [output format], --output-format [output format]
                      输出格式，可以指定 json 或者 yaml，缺省为 yaml
```

**例如**

`./kube-obj-ver-conv.py convert -s deploy.yaml  -d deploy.1.9.yaml -o yaml -t 1.9`
