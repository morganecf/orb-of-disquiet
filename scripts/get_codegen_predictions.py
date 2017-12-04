import subprocess
import time

cmd = "java -jar codegen_score_row.jar -m 5a207fa7eeb38c357a32689f.jar -s 'I am so happy'"

p = subprocess.Popen(cmd.split(), stdin=subprocess.PIPE, bufsize=1)

p.stdin.write('TEST: I am so happy')

while True:
  r = raw_input()

  p.stdin.write(r)

  print(p.stdout.readline())
