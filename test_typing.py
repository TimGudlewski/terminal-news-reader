import inspect


class TypeTester:
    whatever: list[str] = []

    def __init__(self, a=0):
        if a:
            self.whatever = self._make_whatever()

    def _make_whatever(self) -> list[str]:
        return ["1", "2", "3"]

    def test_whatever(self):
        if self.whatever:
            print("hi")


if __name__ == "__main__":
    a = TypeTester(1)
    print(isinstance(a, object))



