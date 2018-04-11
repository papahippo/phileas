def unravel(seq):
    """
Unravel/flatten a sequence of HTML Elements. This is necessary because
concatenations of Elements may be coded as tuples or lists.
The unravelling happens when the top Cr4level Element is stringified. In other words,
sequencing is a form of deferred concatenation. Earlier versons of phileas didn't
support the use of '+' to 'concatenate as you go' so many levels of unravelling could
be required. As one might guess, 'unravel' is a recursive function.
    """
    ans = []
    for it in seq:
        if it is None:
            continue
        if isinstance(it, (list, tuple)):
            ans += unravel(it)
        else:
            ans.append(it)
    return ans


class Element:

    """
Each possible HTML tag is defined  as a lcass inheriting this class.
The name of the class is the lower case tag string with a leading underscore added,
e.g. '_h3' or '_br'. When no attributes are associated with a tag, it can be expressed
simply by e.g. 'h.br' or 'h.h4' (without the quotes). Such references are 'corrected'
(by __getattr__ - see above) to return an instance of the corresponding class.
When, however, attributes are required, it must be expressed as e.g.
'h.a(href='somewhere')'. Note that this calls - not creates - an instance (see
member function '__call__' below). Differences of the 'rules of use' of various html tags
are handled by the attribute 'AttrDicts'. 'AttrDicts' is a (often empty) tuple of
dictionaries. keys of each dictionary represent valid attributes for this _Element.
The corresponding values are (in the current implementation) booleans indicating
whether a value is associated with this attribute. False means that the value must not be
supplied and will automatically be derived from the attribute name. This will probably be
changed in a later release, e.g. to use a function or class as a value; this will make
validation and manipulation of numeric values easier. N.B. class Element must be declared
within class _HTML40. This ensures that e.g. h._h4 where h is obtained by e.g.
'h = _HTML40()' is a valid attribute reference (see __getattr__ above).
    """
    AttrDicts = ()
    okAttrs = None
    # 'separateClose' is True for most Elements but False for tags like 'br' which are
    # self-contatined and so don't require a separate closing tag.
    #
    separateClose = True
    dented = True

    def __init__(self, tag=None, separateClose=None, children=[], **sArgs):
        self.tag = tag
        self.sArgs = sArgs
        self.children = children[:]
        if separateClose is not None:  # use None for 'no overrule'
            self.separateClose = separateClose

    def __call__(self, **args):
        """
This functions makes it possible to derive tags with attributes by calling the tag with
arguments, e.g. 'h.img(src='pickie.jpg')'.
Beware: this looks like a simple instance creation but isn't; h.img already returns an
instance so the bracketed construction gets routed to this function.
This construction can be used with empty brackets to force a copy operation as opposed
to just a name alias; i.e. 'mytable = h.table()' is kind of analogous to the following
'trick' for lists: 'my_list = precious_list[:]'.
        """
        if self.okAttrs is None:
            self.okAttrs = {}
            for d in self.AttrDicts:
                self.okAttrs.update(d)
        sArgs = {}
        for key, val in args.items():
            key = key.lower().replace('_', '-')
            if not key in self.okAttrs.keys():
                raise KeyError(key)
            if not self.okAttrs[key]:
                sArgs[key] = key
            else:
                # the following statement is currently essentially
                # just a cheap and cheerful way to allow numeric
                # values to be specified without quotes; room for improvement here!
                sArgs[key] = str(val)
        return self.__class__(tag=self.tag, separateClose=self.separateClose,
                              **sArgs)

    def _as_children(self, other):
        """
Function '_as_children' is used internally by several public customization member function.
Its purpose is to avoid unnecessary nesting of Elements when the child
Element is tagless; in this case, its children can be taken on board by its parent.
        """
        return ((other is self or isinstance(other, self.__class__)) and other.tag is None
                and other.children or [other,])

    def __or__(self, other):
        """
member function '__or__' ensures that code like e.g. 'h.h4 | <expression>',
when converted to a string, results in '<h4>expression</h4>'.
Similarly 'h.a(href="myLink") | "text"' becomes '<a href=myLink>text</a>'.
        """
        return self.__class__(tag=self.tag, separateClose=self.separateClose,
                              children=self._as_children(other), **self.sArgs)

    __ror__ = __or__
    """ 
The above definition ensures  that the '|' operator (see above) is symmetrical.
    """

    def __ior__(self, other):
        """
Member function '__ior__' facilitates adding more child Elements to an
already defined html Element, using the '|=' in-place operator
        """
        self.children.extend(self._as_children(self, other))
        return self

    def __and__(self, other):
        """
This member function facilitates the use of & (usually a bit-wise 'and') to conditionally
apply HTML operators, e.g.:
'(this_user==selected_user)&h.em | "this is highlighted when it relates to selected user"'.
        """
        return self if other else self.__class__() # if false, return 'lame' html tag.

    __rand__ = __and__  # '&' operator is symmetrical

    def __add__(self, other):
        """
This custom function was introduced very late in the development in order to
facilitate the use of '+' instead of ',' for concatenating Elements. This will
drastically reduce the amount of 'unravelling' when stringifying complex nested
HTML objects.
        """
        if not other:
            return self()  # just return clone of self!

        return self.__class__(tag=None, separateClose=False,
            children=self._as_children(self)+self._as_children(other))

    def __radd__(self, other):
        """ note that our addition is not commutative!
        """
        return self.__class__(tag=None, separateClose=False,
            children=self._as_children(other)+self._as_children(self))

    def __mul__(self, other):
        return sum([self for i in range(other)], None)

    __rmul__ = __mul__  # e.g. h.br*5 and 5*h.br are equivalent

    def __str__(self):
        """
__str__ is used to create a character representation of the Element. For example,
this is used by 'print'. The character representation in our case is valid HTML.
        """
        if self.children is None:
            return ''
        if self.tag is None:  # special case for 'orphan' Elements
            s = ''
        else:
            s = "<%s" % self.tag
            for key, val in self.sArgs.items():
                if val is not None:
                    s += ' %s="%s"' % (key.lower(), val)
            if not self.separateClose:
                s += '/'
            s += '>'
        for child in unravel(self.children):
            s += str(child)
        if self.separateClose:
            s += '</%s>' % self.tag
            if self.tag not in ('span', 'a'):
                s += '\n'
        return s

    def join(self, seq):
        """
Member function 'join' ensures that the construction
(e.g.) 'h.br.join(seq)' causes items of sequence to
be interspersed with blank lines when output. Items of the
sequence with the value 'None' are ignored completely
(but zero length strings are treated normally!)
        """
        return self.__class__( tag=None, separateClose=False , children=(seq[:1] + [(self+term) for term in seq[1:]]))
