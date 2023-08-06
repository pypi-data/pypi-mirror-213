## 简化版蛋白质二级结构分类器
### 使用方法
- 首先通过pip进行安装：
```bash
$ python3 -m pip install restraint-fold --upgrade -i https://pypi.org/simple
```
- 然后直接在命令行进行使用：
```bash
$ python3 -m fold -h
usage: __main__.py [-h] [-i I] [-o O] [--simplified SIMPLIFIED]

optional arguments:
  -h, --help            show this help message and exit
  -i I                  Set the input pdb file path.
  -o O                  Set the output txt file path.
  --simplified SIMPLIFIED
                        Return the simplified information, default to be 0.
```

### 示例
- 执行一个生成完整的alpha和beta序列的命令：
```bash
$ python3 -m fold -i fold/pdb/case2-optimized.pdb -o case2-secondary.txt
```
得到的结果如下所示：
```txt
# case2-secondary.txt
alpha:
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 31 32 33 34 35 36 37 39 40 41 42 43 44 45 46 78 79 80 81 82 83 84 85 86 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109
beta:
23 24 25 26 27 28 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 86 87 88 89 90 91 92 93 94 95 96 97 98 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157
```

```bash
$ python3 -m fold -i fold/pdb/case2-optimized.pdb -o case2-secondary.txt --simplified 1
```
得到的结果如下所示：
```txt
# case2-secondary.txt
alpha:
1~24
31~36
39~45
78~85
94~97
99~108

beta:
23~28
46~76
86~98
117~157
```
### 提示
如果输入的pdb文件中氢原子有缺失，需要先通过Xponge或者Hadder等工具进行补氢，然后再对结构进行解析：
```bash
$ python3 -m pip install hadder --upgrade -i https://pypi.org/simple
$ python3 -m hadder -h
usage: __main__.py [-h] [-i I] [-o O]

optional arguments:
  -h, --help  show this help message and exit
  -i I        Set the input pdb file path.
  -o O        Set the output pdb file path.
  
$ python3 -m hadder -i input.pdb -o ouput.pdb # e.g. $ python3 -m hadder -i examples/case2.pdb -o examples/case2-complete.pdb
1 H-Adding task with 3032 atoms complete in 0.116 seconds.
```
