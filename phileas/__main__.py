from .html4 import HTML4
from .html5 import HTML5
import sys

# create a singleton instance of each html class.

_html40 = html4 = HTML4()  # _html40 is a deprecated alias!
html5 = HTML5()
# I recommend that one of the above is imported under a much shorter name, e.g.:
# 'from phileas import html4 as h'. This usage will be assumed and
# 'h' referred to as 'the HTML generator' in this code.

def main():

    h = html5 # the local equivalent of 'from phileas import html40 as h'.
    print (
        h.html | (
            h.p |
             ( """ This primitive web-page was produced using 'phileas' (and python of course!).
             """, h.em | ('aha!',),
             ),
             h.p | (
             h.br * 2,
             h.br, "abc " * 3, 4 * 'xyz ', '\n',
             3 * h.br,
             """ If you're viewing this output in a browser, you can get to some (possibly not
              100% up to date!) background info on 'phileas' by clicking """,
             h.br,  (h.a(href="http://larry.myerscough.nl/phileas_project/") | 'this text'),
             '.' ,
             (False & h.em | 'plain '), (True & h.em) | "italic"
             ),
            h.br.join(sys.path[:3]), h.br * 2,
            # let's check the creation of 'deliberately orphaned html Elements:
            h | ("\n[orphaned Elements' text should look just like any other text.]")

        )
    )

if __name__ == '__main__':
    main()
