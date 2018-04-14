from .html4 import HTML4
import sys

# create a singleton instance of this class. The approved method to use phileas is to include this
# by  "from phileas import html40 as h" (The alias with leading '_' is deprecated but retained to avoid
# having to refactor lots of stuff!). Then html element creation can use the compact form
# (e.g.) "h.h4 ..." etc. (html40.h4 ... would soon get cumbersome!)

_html40 = html40_ = HTML4()
# I recommend that this is imported under a much shorter name, e.g.:
# 'from phileas import html40 as h'. This usage will be assumed and
# 'h' referred to as 'the HTML generator' in this code.

def main():

    h = html40_  # the local equivalent of 'from phileas import html40 as h'.
    print(
        "Content-type: text/html\n\n",
        h.html | (
            (h.p |
             """ This primitive web-page was produced using 'phileas' (and python of course!).
             """ + (h.em | 'aha!')
             ) +
            (h.p |
             h.br * 2 +
             h.br + "abc " * 3 + 4 * 'xyz ' + '\n' +
             3 * h.br +
             """ If you're viewing this output in a browser, you can get to some (possibly not
              100% up to date!) background info on 'phileas' by clicking """ +
             h.br + (h.a(href="http://larry.myerscough.nl/phileas_project/") | 'this text') +
             '.' +
             (False & h.em | 'plain ') + (True & h.em | "italic")
             ) +

            h.br.join(sys.path[:3]), h.br * 2,
            # let's check the creation of 'deliberately orphaned html Elements:
            h | ("\n[orphaned Elements' text should look just like any other text.]"
                 + "... even when using the '+' operator!")

        )
    )


if __name__ == '__main__':
    main()
