#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/1/28 4:12 下午
# @Author  : zhengyu.0985
# @FileName: RichTest.py
# @Software: PyCharm

from rich import print
from rich.console import Console
print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:", locals())

console = Console()
console.print("Hello", "World!")
console.print("Hello", "World!", style="bold red")
console.print("Where there is a [bold cyan]Will[/bold cyan] there [u]is[/u] a [i]way[/i].")
