from random import randint

from src.exceptions import DiceError


class Dice:
    __slots__ = ("_throw",
                 "_face",
                 "_retain_f",
                 "_retain_n",
                 "_result",
                 "_retain",
                 )

    def __init__(self, throw,
                 face,
                 retain_f=None,
                 retain_n=None):
        self._throw = throw
        self._face = face
        self._retain_f = retain_f
        self._retain_n = retain_n

        self._result = None
        self._retain = None

    def to_str(self, view_retains=False, startswith_retain='<strike>', endswith_retain='</strike>'):
        if (not isinstance(self._all_result, list) or not self.retains) and view_retains:
            view_retains = False
        if view_retains and isinstance(self._all_result, list) and len(self.result) != len(self._all_result):
            values = list(map(str, self._all_result)) if isinstance(self._all_result, list) else [str(self._all_result)]
            retains, cut = list(map(str, self.retains)), []
            for n, value in enumerate(values):
                if value in retains:
                    retains.remove(value)
                else:
                    cut.append(value)
                    values[n] = f"{startswith_retain}{value}{endswith_retain}"
        else:
            values = map(str, self.result) if isinstance(self.result, list) else [str(self.result)]

        return f"[{'+'.join(values)}]"

    def __repr__(self) -> str:
        return f"Dice(throw={self.throw}, face={self.face}, retain_f = {self._retain_f}, " \
               f"retain_n = {self._retain_n}, result = {self.result})"

    def _get_retains(self):
        if self._retain_n is None and self._retain_f is None:
            return None
        elif not all((self._retain_f, self._retain_n)):
            raise DiceError("Unspecified retain formula or count for save")
        elif self._retain_n > self._throw:
            return None
        all_results = self._all_result.copy()
        results = []

        for _ in range(self._retain_n):
            exclude = self._retain_f(all_results)
            all_results.remove(exclude)
            results.append(exclude)
        return results

    @property
    def _all_result(self):
        if not self._result:
            self._result = [randint(1, self._face) for _ in range(self._throw)]
        return self._result

    @property
    def throw(self):
        return self._throw

    @property
    def face(self):
        return self._face

    @property
    def retains(self):
        if self._retain is None:
            self._retain = self._get_retains()
        return self._retain

    @property
    def result(self):
        list_results = self._all_result.copy()
        if self.retains:
            list_results = self._retain
        return list_results

    @property
    def total(self):
        if isinstance(self.result, int):
            return self.result
        return sum(self.result)
