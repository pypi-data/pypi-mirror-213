from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Union

from funrun import action
from funrun.product import Product, ProductOrPath


@dataclass
class WcOutput(Product):
    def count(self):
        return int(self.match(r"^\s*(\d+)").group(1))


@dataclass
class DirContents(Product):
    def entities(self):
        return self.lines()


@dataclass
class Directory(Product):
    pass


@action
def cat(input: List[ProductOrPath]) -> Product:
    return Product(lambda: f'cat  {" ".join(input)}')


@action
def grep(keyword: str, input: ProductOrPath) -> Product:
    return Product(lambda: f"grep {keyword} {input}")


@action
def wc(input: ProductOrPath) -> WcOutput:
    return WcOutput(lambda: f"wc {input}")


@action
def ls(input: Optional[Union[Directory, str, Path]] = None) -> Product:
    return Product(lambda: f"ls {input}" if input else "ls")


@action
def find(input: Optional[Union[Directory, str, Path]], type="f", pattern="") -> DirContents:
    return DirContents(lambda: f'find {input} -type {type} -name "{pattern}"')
