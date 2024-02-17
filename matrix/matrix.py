#!/usr/bin/env python3

import re
import json

from os import system
from getpass import getpass
from SecureData import encryptObject, decryptObject

# AES128-CBC-PKCS7
matrixData = b"dx3z8CQHse/Y3TF/IXfTAV9EVEiArLx4rzJgOQmpA+0R3DCluOx1YlbeLnZdZ7lJ5OXiNiQ/qW2FzIz6rKv49+oeqjVUrL/WEKfznmX6HJgtWJU3SLqyckrVLbS4M7yxk13+u1JPip7oAK6xN1ywgzlRsaEb7jKGbc8AL3q77rz8B9i6jR7iquZbIKsLM/3AYCnvyD0iesiqx+mGzXeq4fEgBzSG75h8qc/d5XVj9o1F0noStZz9PqlDUH2LimZspGe9bvExpf8SuR/oOF41Aec0JCIiRY7rfJp9rPa+tiODFBa+DltcKerI6ut9062e11fDc9h79UCiFQx/Ko1n5NZ6TpOUErafJmeoXsq6x0A+HrzowVMyCglkKi6r0zAj4+sWTwj599lcfsoqM16BkjTjDPZXNxoq8wQBAvEVcmEk3mp8DRecs5z4DijsvErrlB0FvXMzRpoSm8vblsUykweWsPxztbtBQQRuU3uR4B2t4UL7+PKJDe/A39uw+IRnat9H524xo4TEBggzVbOU2vGjv7NGrRqL6cbfP30onKQbo5SszHxm13QtzOwcNCLgr/vB5qZJBHN9A97J6d0ajrk3SGlmJMO5aJWf6EXt6I+/zoFONDaxVc/j2w2vwWGT"
matrix = None


def convCoords(c):
	pattern = re.compile('^[a-hA-H]{1}[1-8]{1}$')
	if not pattern.match(c):
		raise ValueError
	x = ord(c[0]) - 97 if c[0].islower() else ord(c[0])-65
	y = int(c[1])-1
	return (x, y)


def getValue(x, y):
	return matrix[x][y]


if __name__ == '__main__':
	password = getpass("Password: ")
	try:
		matrix = decryptObject(matrixData, password)
	except:
		print("Incorrect password")
		system('pause')
		exit()

	while True:
		i = input("Enter coords [A-H][1-8] or <Q> to quit: ")
		if i in ('q', 'Q', 'quit', 'QUIT', 'Quit', 'exit', 'EXIT', 'Exit'):
			exit()

		for c in i.split():
			try:
				print(f'{c.upper()}\t{getValue(*convCoords(c))}')
			except ValueError:
				print('Invalid coordinate')
