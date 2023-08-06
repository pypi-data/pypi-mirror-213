from collections import deque
from inspect import getmembers_static, isfunction

from graphviz import Digraph


def is_leaf(obj):
  return not isinstance(obj, dict) and \
    not isinstance(obj, list) and \
    (type(obj).__repr__ is not object.__repr__ or \
      type(obj).__str__ is not object.__str__)


def is_property(var, val):
  return not var.startswith('__') and not isfunction(val)


def format_label(s):
  for c in '{}|<>':
    s = s.replace(c, '\\' + c)
  return s


def graph(obj):
  g = Digraph(node_attr={'shape': 'record'})

  if is_leaf(obj):
    g.node('', str(obj))
    return g

  labels = []
  visited = set()
  q = deque([(None, obj)])

  def process_property(var, val, curr_id):
    if is_property(var, val):
      var = f'{var}: {type(val).__name__}'
      p_id = str(id(val))
      label = f'{{{var}|{format_label(str(val))}}}' if is_leaf(val) else f'<{p_id}> {var}'

      if not is_leaf(val):
        q.append((f'{curr_id}:{p_id}', val))

      labels.append(label)

  while q:
    prev_id, curr = q.popleft()
    curr_id = str(id(curr))

    if curr_id in visited:
      g.edge(prev_id, curr_id)
      continue

    visited.add(curr_id)

    if isinstance(curr, dict):
      for key, val in curr.items():
        process_property(str(key), val, curr_id)
    elif isinstance(curr, list):
      for i, val in enumerate(curr):
        process_property(str(i), val, curr_id)
    else:
      for var, val in getmembers_static(curr):
        process_property(var, val, curr_id)

    g.node(curr_id, '|'.join(labels))
    labels.clear()

    if prev_id:
      g.edge(prev_id, curr_id)

  return g


def save_img(obj, filename: str, format='png'):
  ext = '.' + format

  if len(filename) < len(ext) or filename[:len(ext)] != ext:
    filename += ext

  with open(filename, 'wb') as f:
    f.write(graph(obj).pipe(format))
