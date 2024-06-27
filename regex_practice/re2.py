import sys; args = sys.argv[1:]

idx = int(args[0])-40

myRegexLst = [
  r"/^[x.o]{64}$/i",
  r"/^[xo]*\.[xo]*$/i",
  r"/^(\..+|x+o*\..*|.*\.o*x+|.+\.)$/i",
  r"/^.(..)*$/s",
  r"/^(0|1[01])([01]{2})*$/",
  r"/\w*(a[eiou]|e[aiou]|i[aeou]|o[aeiu]|u[aeio])\w*/i",
  r"/^(1?0)*1*$/",
  r"/^\b[bc]*a?[bc]*$/",
  r"/^\b[bc]*((a[bc]*){2})*$/",
  r"/^(2[02]+|((1[02]*){2}|2)(([02]*1[02]*){2})*)$/"
]

if idx < len(myRegexLst):
  print(myRegexLst[idx])

# Sathvik Redrouthu 1 2024