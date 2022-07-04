$file = ("./.profiling/mem-"+(Get-Date -Format "yyyyMMdd-HHmmss").ToString()+'.txt')
python profileMain.py --mem --output $file $args && notepad $file