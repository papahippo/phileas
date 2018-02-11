from Euphonia import *
print(euphonia["called", "Larry"])

class ThisMailing(Mailing):
    def get_html_text(self, recipients=[], mailGroup=None, file_list=[], taal='NL'):
        names = [recipient.called for recipient in recipients]
        name_str = ', '.join(names[:-1])
        if name_str:
            name_str += names[-1]
        else:
            name_str = names[-1]

        return h |(
            "Dear ",  name_str,
            h.br*2,
            "something seems to be actually ",
            h.b | "working!"
        )


if __name__ == "__main__":
    ThisMailing().main()
