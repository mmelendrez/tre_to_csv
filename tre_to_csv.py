#!/user/bin/env python

import argparse
import re
from Bio import Phylo
from StringIO import StringIO

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "treefile",
    help = ".nwk or .tre file path"
  )
  return parser.parse_args()

def main(args):
  t = Phylo.read(args.treefile, 'nexus')

  nonterms = t.get_nonterminals()
  terms = t.get_terminals()

  attrs = ['name', 'branch_length', 'width', 'confidence']

  n = nodes(nonterms, attrs) + nodes(terms, attrs)
  headers = get_unique_headers(n)
  print ','.join(headers)
  csv = get_csv_values(n, headers)
  print '\n'.join(csv)

def get_csv_values(nodes_list, headers):
  r = []
  for x in nodes_list:
    t = []
    d = dict(x)
    for h in headers:
      v = d.get(h, '')
      t.append(v)
    r.append(','.join(t))
  return r

"""
n = [
  [
    ('one', '1')
  ],
  [
    ('one', '1'),
    ('two', '2')
  ]
]
h = ['one', 'two']
x = get_csv_values(n, h)
assert x == ['1,', '1,2']
"""

def get_unique_headers(nodes_list):
  unique_headers = set()
  for x in nodes_list:
    for y in x:
      unique_headers.add(y[0])
  return sorted(list(unique_headers))

"""
n = [[('one', '1')], [('one', '1'), ('two', '2')]]
x = get_unique_headers(n)
assert x == ['one', 'two'], x
"""

def split_comment(comment):
    kv = re.split(',(?=[a-zA-Z])', comment[2:-1])
    r = []
    for i in kv:
        split = split_kv(i)
        r += split
    return r

"""
x = split_comment('[&foo={1,2},bar=1]')
assert x == [('foo_start', '1'), ('foo_end', '2'), ('bar', '1')], x
x = split_comment('[&length_range={3.8281494893510626E_4,14.352918026321717},rate_95%_HPD={1.7845086804287104E_4,0.0010251769224814925},length_95%_HPD={3.8281494893510626E_4,1.5070077745538768},length=0.5388916323464435,posterior=0.0608,height_median=29.70276874027033,rate_range={5.150302290203778E_5,0.0016340716346819675},height_range={28.45245233084532,68.69071069965014},height_95%_HPD={28.801217078411373,31.132619815405704},rate=6.061868789563863E_4,rate_median=5.712602882591811E_4,length_median=0.40645877662341867,height=29.89831669852368]')
assert x == [('length_range_start', '3.8281494893510626E_4'), ('length_range_end', '14.352918026321717'), ('rate_95%_HPD_start', '1.7845086804287104E_4'), ('rate_95%_HPD_end', '0.0010251769224814925'), ('length_95%_HPD_start', '3.8281494893510626E_4'), ('length_95%_HPD_end', '1.5070077745538768'), ('length', '0.5388916323464435'), ('posterior', '0.0608'), ('height_median', '29.70276874027033'), ('rate_range_start', '5.150302290203778E_5'), ('rate_range_end', '0.0016340716346819675'), ('height_range_start', '28.45245233084532'), ('height_range_end', '68.69071069965014'), ('height_95%_HPD_start', '28.801217078411373'), ('height_95%_HPD_end', '31.132619815405704'), ('rate', '6.061868789563863E_4'), ('rate_median', '5.712602882591811E_4'), ('length_median', '0.40645877662341867'), ('height', '29.89831669852368')], x
"""

def split_kv(kv_str):
    '''
    'key={1,2}' => [('key_start', '1'), ('key_end', '2')]
    'key=1' => [('key', '1')]
    '''
    if '{' in kv_str:
        return split_bracket(kv_str)
    return split_single(kv_str)

"""
x = split_kv('key={1,2}')
assert x == [('key_start', '1'), ('key_end', '2')], x
x = split_kv('key=1')
assert x == [('key', '1')], x
"""

def split_single(kv_str):
    return [tuple(kv_str.split('='))]

"""
x = split_single('key=1.0')
assert x == [('key', '1.0')], x
"""
    
def split_bracket(kv_str):
    key, value = split_single(kv_str)[0]
    cutval = value[1:-1].split(',')
    return [(key+'_start', cutval[0]), (key+'_end', cutval[1])]

"""
x = split_bracket('key={1.0,2.0}')
assert x == [('key_start', '1.0'), ('key_end', '2.0')], x
"""

def nodes(clades, attrs):
    '''
    Returns list of lists of tuples
    '''
    r = []
    mcctre = []
    for nonterm in clades:
        for attr in attrs:
            kv = (attr, str(getattr(nonterm, attr)))
            mcctre.append(kv)
        mcctre += split_comment(nonterm.comment)
        r.append(mcctre)
        mcctre = []
    return r

if __name__ == "__main__":
  args = parse_args()
  main(args)
