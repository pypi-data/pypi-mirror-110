from ..BaseCWS import BaseCWS
from ...._C import THUlac
from ....data import load


class THUlacCWS:
    """使用THUlac实现的CWS算法
    """
    def __init__(self, device=None):
        model_path = load("cws.lac", 'fp32')
        self.model = THUlac(model_path)
        #super().__init__(device)

    def __call__(self, sents):
        result = [self.model.cut(sent) for sent in sents]
        results = []
        for sep in result:
            if sep[-1] == '\n':
                sep = sep[:-1]
            results.append(sep)
        return results
