__version__ = "0.0.0"

from funrun.decorators import action
from funrun.product import Product
from funrun.runner import MAKE_OUTPUT, Runner


def make(product: MAKE_OUTPUT, **kwargs) -> MAKE_OUTPUT:
    """
    generates the product using a runner.

    :param product: Product to make
    :param kwargs:
    :return:
    """
    runner = Runner()
    return runner.make(product, **kwargs)
