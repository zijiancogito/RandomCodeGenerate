from random import choice
import utils
import random
import cfile as C
import argparse
import sys
import os

def compile_file(filename, opt_level):
  compiler_options = ['-fno-ipa-pure-const',
                      '-fno-inline-functions']
  cmd = f"gcc -O{opt_level} -w {' '.join(compiler_options)} {filename}.c -o {filename}.o"
  import os
  pipeline = os.popen(cmd)
  print(pipeline.read())
  print("Compile Finish.")


def main_file(filename):
  f = C.cfile(filename)
  f.code.append(C.sysinclude('stdio.h'))
  f.code.append(C.blank())
  f.code.append(utils._main())
  f.code.append(utils._printf())
  f.code.append(utils._scanf_no_pointer())
  f.code.append(utils._rand())
  for i in range(10000):
    f.code.append(utils._func(f"func{i}"))
  utils._file(filename, str(f))

def main():
  parser = argparse.ArgumentParser(description='Random Code Generator')
  subparsers = parser.add_subparsers(help='sub-command help')

  parser_1 = subparsers.add_parser('gen', help='generate random codes and get a c file.')
  parser_1.add_argument('-f', '--filename', help="Name of file.")

  parser_2 = subparsers.add_parser('compile', help='Compile code.')
  parser_2.add_argument('-o', '--option', help='compiler optimize level')
  parser_2.add_argument('-f', '--filename', help='path to save')
  args = parser.parse_args()
  # print(args)
  subp = sys.argv[1]
  if subp == "gen":
    main_file(args.filename)
  elif subp == "compile":
    compile_file(args.filename, args.option)
  else:
    print(args.help)

if __name__ == '__main__':
  main()