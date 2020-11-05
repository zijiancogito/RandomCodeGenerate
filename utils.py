import cfile as C
import random

def _rand():
  print("Generate rand function...")
  body = C.block(innerIndent=3)
  body.append(C.statement(f"{C.variable('var0', 'int')} = {C.fcall('rand')}"))
  body.append(C.statement('return var0'))
  head = C.function('f_rand', 'int')
  func = C.sequence()
  func.append(head)
  func.append(body)
  print(str(func))
  return func

def _scanf_no_pointer():
  print("Generate scanf function...")
  body = C.block(innerIndent=3)
  body.append(C.statement(C.variable('var0', 'int')))
  body.append(C.statement(C.fcall('scanf').add_arg('\"%d\"').add_arg('&var0')))
  body.append(C.statement("return var0"))
  head = C.function('f_scanf_nop', 'int',)
  func = C.sequence()
  func.append(head)
  func.append(body)
  print(str(func))
  return func

def _printf():
  print("Generate printf function...")
  body = C.block(innerIndent=3)
  body.append(C.statement(C.fcall('printf').add_arg('\"%d\"').add_arg('p0')))
  head = C.function('f_printf', 'void',).add_param(C.variable('p0', 'int'))
  func = C.sequence()
  func.append(head)
  func.append(body)
  print(str(func))
  return func

def _expression(all_vars: list, op_seq: list, target):
  end = False
  expr = random.choice(all_vars)
  for it in range(5):
    opc = random.choice(op_seq)
    var = random.choice(all_vars)
    expr = f"({expr}) {opc} {var}"
    end = random.choice([True, False])
    if end:
      break
  return expr

def _func(funcname):
  print(f"Generate {funcname}...")
  para_count = random.randint(0, 3)
  local_count = 3
  local_const = 2
  body = C.block(innerIndent=3)
  for i in range(local_count):
    body.append(C.statement(f"{C.variable(f'var{i}', 'int')} = {C.fcall(random.choice(['f_rand', 'f_scanf_nop']))}"))
  for i in range(local_const):
    body.append(C.statement(f"{C.variable(f'var{i+local_count}', 'int')} = {random.randint(-1000, 1000)}"))

  all_vars = [f'var{i}' for i in range(local_const + local_count)] + [f'p{i}' for i in range(para_count)]
  op_seq = ['+', '-', '*', '/', '<<', '>>']
  # print(all_vars)
  max_iter = 5
  targets = []
  for i in range(4):
    trg = random.choice(all_vars)
    expr = _expression(all_vars, op_seq, trg)
    body.append(C.statement(f"{trg} = {expr}"))
    targets.append(trg)
  ret_var = random.choice(all_vars)
  ret_expr = _expression(targets, op_seq, ret_var)
  body.append(C.statement(f"{ret_var} = {ret_expr}"))
  body.append(C.statement(f'return {ret_var}'))
  head = C.function(funcname, 'int')
  for i in range(para_count):
    head.add_param(C.variable(f'p{i}', 'int'))
  func = C.sequence()
  func.append(head)
  func.append(body)
  print(str(func))
  return func

def _main():
  print("Generate main function...")
  func = C.sequence()
  head = C.function('main', 'int',)
  body = C.block(innerIndent=3)
  body.append(C.statement('return 0'))
  func.append(head)
  func.append(body)
  print(str(func))
  return func

def _file(filename, stream):
  with open(filename, 'w') as f:
    f.write(stream)

def test():
  _printf()
  _rand()
  _scanf_no_pointer()
  _func("func")
  _main()

def main():
  test()

if __name__ == '__main__':
  main()