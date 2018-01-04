# Kubernetes Object file version converter

Convert API Object file into specified version.

## Usage

### Query

`kube-ver-conv.py query [Object Kind]`

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
                                [output version] [-o [output version]]

optional arguments:
  -h, --help            show this help message and exit
  -s [file name], --source-file [file name]
                        YML or JSON file to process, '-' for STDIN.
  -d [file name], --dest-file [file name]
                        File name for output, '-' for STDOUT.
  -t [output version], --to-version [output version]
                        Kubernetes version of the out object file.
  -o [output version], --output-format [output version]
                        Format of the output file, default is yaml
```

**Example**

`./kube-obj-ver-conv.py convert -s deploy.yaml  -d deploy.1.9.yaml -o yaml -t 1.9`
