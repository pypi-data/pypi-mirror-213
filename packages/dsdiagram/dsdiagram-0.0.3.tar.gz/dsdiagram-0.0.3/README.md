# data structure diagram generator

## installation

download [graphviz](https://www.graphviz.org/download/)

```
pip install dsdiagram
```

## quick start

### save image

```py
from dsdiagram import save_img


class Node:

  def __init__(self, id, next=None):
    self.id = id
    self.next = next


n = 5
nodes = [Node(id) for id in range(n)]
head = nodes[0]

for id in range(n):
  nodes[id].next = nodes[(id + 1) % n]

save_img(head, 'linked-list')
```

`linked-list.png`

![](https://raw.githubusercontent.com/David0922/gen-data-structure-diagram/main/examples/linked-list.png)

### render diagram in jupyter

![](https://github.com/David0922/gen-data-structure-diagram/blob/main/examples/jupyter.png?raw=true)
