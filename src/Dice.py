from random import randint

from exceptions import DiceError


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

    def __str__(self):
        return f"[{'+'.join(map(str, self.result)) if isinstance(self.result, list) else str(self.result)}]"

    def __repr__(self) -> str:
        return f"Dice(throw={self.throw}, face={self.face}, retain_f = {self._retain_f}, " \
               f"retain_n = {self._retain_n}, result = {self.result})"

    def _get_retains(self):
        if self._retain_n is None and self._retain_f is None:
            return None
        elif (self._retain_f is None and not self._retain_n is None) or \
                (self._retain_n is None and not self._retain_f is None):
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
        if len(list_results) == 1:
            return list_results[0]
        return list_results
