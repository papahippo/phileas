#!/usr/bin/env python3
import inspect


class Awhere:
    prev_lineno = -1

    def __init__(self, *pp):
        # print ( inspect.getsourcelines(self))
        last_lineno = inspect.getouterframes(inspect.currentframe())[-1].lineno
        self.lineno_range = (Awhere.prev_lineno+1, last_lineno + 1)
        Awhere.prev_lineno = last_lineno

if __name__ == "__main__":
    # class 'Awhere' is probably best used as a mix-in, but for this example,
    # let's keep it simple.

    aw0 = Awhere() # first call returns wrong start line so this call is typically used as a dummy
    aw1 = Awhere(42,
                54,
                99)

    aw2 = Awhere(
        142, 156,
        167
    )
    print ([aw.lineno_range for aw in (aw0, aw1, aw2)])
