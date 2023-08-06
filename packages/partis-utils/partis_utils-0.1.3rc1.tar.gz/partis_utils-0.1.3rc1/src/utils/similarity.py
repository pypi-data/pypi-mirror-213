
from difflib import SequenceMatcher

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def dict_push(d, k, v):
  l = d.setdefault(k, list())
  l.append(v)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def dict_pop(d, k):
  v = None

  if k not in d:
    return v

  l = d[k]

  if len(l) > 0:
    v = l.pop(-1)

  if len(l) == 0:
    d.pop(k)

  return v


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def similarity(src, opt, isjunk = None, autojunk = True):

  if src == opt:
    return 1.0

  seq = SequenceMatcher(isjunk, src, opt, autojunk)

  ops = seq.get_opcodes()

  equal = list()
  deleted = dict()
  inserted = dict()

  transposed = list()

  num_changes = 0

  for op, i1, i2, j1, j2 in ops:
    a = src[i1:i2]
    b = opt[j1:j2]

    if op == 'equal':
      equal.append((a, i1))

    elif op == 'delete':
      num_changes += len(a)

      _i1 = dict_pop(inserted, a)

      if _i1 is None:
        dict_push(deleted, a, i1)
      else:
        transposed.append((a, i1, _i1))

    elif op in ['replace', 'insert']:

      _i1 = dict_pop(deleted, b)

      if _i1 is None:
        dict_push(inserted, b, i1)

      else:
        # num_changes -= len(b)
        transposed.append((b, _i1, i1))

      if op == 'replace':
        num_changes += len(a) + len(b)
        dict_push(deleted, a, i1)
      else:
        # insert
        num_changes += len(b)


  max_chars = max(len(src), len(opt))
  total_chars = len(src) + len(opt)
  num_equal = sum(len(v) for v, i0 in equal)
  num_transposed = sum(len(v) for v,i0,i1 in transposed)

  pro = num_equal / len(src)
  anti = (num_changes - 0.5*num_transposed) / total_chars

  similarity = min(1.0, max( 0.0, 0.5*( pro + 1.0 - anti ) ))

  return similarity

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def max_similarity(src, options, isjunk = None, autojunk = True):

  best_similarity = -1.0
  best_option = None

  for opt in options:
    _similarity = similarity(src, opt, isjunk = isjunk, autojunk = autojunk)

    if _similarity > best_similarity:
      best_similarity = _similarity
      best_option = opt

  return best_option, best_similarity
