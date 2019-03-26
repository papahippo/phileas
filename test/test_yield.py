from phileas import html5 as h
import sys, os

def test_page():

    yield from (
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
             (False & h.em | 'plain '), (True & h.em | "italic")
             ),
            h.br.join(sys.path[:3]), h.br * 2,
            # let's check the creation of 'deliberately orphaned html Elements:
            h | ("\n[orphaned Elements' text should look just like any other text.]")

        )
    )

def little_test_page():

    print("yield#1")
    yield  from (h.h4 | ('dsdfs',))

    print("yield#2")
    yield from  (h.p | (h.em | (h.strong | ('aha!', "asdf"))))
    yield "easy",

def main():
    "Content-type: text/html\n\n",
    #print([[e for e in el] for el in test_page()])
    print([el for el in test_page()])


if __name__ == '__main__':
    main()
