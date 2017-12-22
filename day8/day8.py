#!/usr/bin/python
# coding=utf-8
import re
import os
def get_pattern(n=False):
	pattern = r"(^[a-z]+)" if n else r"([a-z]+)"
	p = re.compile(pattern,re.MULTILINE)
	return p

def clean_input(s):
	s = s.replace(" if ",",")
	s = s.replace("inc","+=")
	s = s.replace('dec','-=')
	return s

def refactor_input(s):
	p = get_pattern()
	s = p.sub(r"$reg{'\1'}",s)
	return s

def read_file_s(file):
	with open(file,'r') as f:
		s = f.read()
	return s
"""
def refactor_dict(A,s):
	K = (k for k in enumerate(A))
	for k,v in K:
		print(v)
"""
def get_registers(s):
	p = get_pattern(True)
	r = p.findall(s)
	return list(set(r))

def get_pre(s):
	registers = get_registers(s)
	#refactor_dict(registers,s)
	s = ','.join("'{}'=>0".format(x) for x in registers)
	a = "#!/usr/bin/perl\n# coding=utf-8\nuse List::Util qw(max);"
	b = "my %reg = ({});\nmy @maxes = ();".format(s)
	pre = "{}\n{}".format(a,b)
	return pre

def form(cond,stmt):
	s = "if ({}) {{ {};}}".format(cond,stmt)
	return s

def get_instructions(s):
	A = s.split("\n")
	instruct = [a.split(",") for a in A]
	instruct = '\npush @maxes, max values %reg;\n'.join(form(x[1],x[0]) for x in instruct)
	return instruct

def create_output(s):
	pre = get_pre(s)
	ens = 'my $reg_max = max values %reg;\nmy $max_max = max @maxes;\nprint("$reg_max\\n");\nprint("$max_max\\n");'
	s = refactor_input(s)
	instruct = get_instructions(s)
	out = "{}\n{}\npush @maxes, max %reg;\n{}".format(pre,instruct,ens)
	return out

def write_file(file,s):
	with open("_{}.pl".format(file),'w') as f:
		f.write(s)

def perlify(in_file,out_file):
	s = read_file_s(in_file)
	s = clean_input(s)
	t = create_output(s)
	write_file(out_file,t)

def main():
	in_file = "input.in"
	out_file = "temp"
	perlify(in_file,out_file)
	os.system("perl _{}.pl".format(out_file))
	os.remove("_{}.pl".format(out_file))

if __name__ == '__main__':
	main()