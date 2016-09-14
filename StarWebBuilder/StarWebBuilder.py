# Variáveis de ambiente necessárias:
#
#       STARWEB_USER: usuário do StarWeb
#   STARWEB_PASSWORD: senha do StarWeb
#   STARWEB_WORK_DIR: diretório local de trabalho do AIT.
#                       Exemplo: C:\dev\tke\ait\ (Windows)
#                                /home/taschetto/projects/tke/ait/ (Linux)
# STARWEB_SHARE_PATH: diretório remoto de trabalho do AIT.
#                       Exemplo: \\stwebdv\sisweb\desenv\ait\ (Windows)
#                                /mnt/stwebdv/ (Linux)
#
# Atenção: para este script funcionar você DEVE ter permissões de escrita em
#          STARWEB_SHARE_PATH. Do contrário, a cópia do arquivo falhará.

import argparse
import os
from Builder import Builder

def main():
  parser = argparse.ArgumentParser(description='Fator 7 StarWeb Builder.')
  parser.add_argument("absolute_path")
  parser.add_argument("--env", default="gisdesenv")
  parser.add_argument("--run", action="store_true")
  args = parser.parse_args()

  print("Local path.: {f}".format(f=args.absolute_path))
  print("Work dir...: {d}".format(d=os.environ['STARWEB_WORK_DIR']))
  print("Remote.path: {p}".format(p=os.environ['STARWEB_SHARE_PATH']))
  if args.run:
    print("Env........: {e}".format(e=args.env))
    print("Run........: {r}\n".format(r=args.run))
  else:
    print("Env........: {e}\n".format(e=args.env))

  builder = Builder(os.environ['STARWEB_SHARE_PATH'],
                    args.absolute_path,
                    os.environ['STARWEB_WORK_DIR'],
                    args.env,
                    args.run,
                    os.environ['STARWEB_USER'],
                    os.environ['STARWEB_PASSWORD'])
  if args.run:
    builder.run_script()
  else:
    builder.copy()
    builder.build()

if __name__ == "__main__":
  main()