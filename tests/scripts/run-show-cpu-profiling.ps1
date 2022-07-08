$file = ("./.profiling/cpu-"+(Get-Date -Format "yyyyMMdd-HHmmss").ToString())
python -m cProfile -o $file  $args && snakeviz $file