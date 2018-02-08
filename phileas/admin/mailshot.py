#!/usr/bin/python3
"""
music_mailer.py has a symbiotic relationship with 'subscribers.py'; either may play the role of
main script.
"""
import sys, os, re, time, smtplib

from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
import mimetypes
import email.utils
from email.header import Header

from phileas import _html40 as h

MagicMailTreeName = 'MagicMailTree'
# ok_exts = ('.pdf', '.jpg', '.jpeg')

def putmsg(*pp, **kw):
    print(*pp, **kw, file=sys.stderr)

class _Mailshot:

# start of stub settings
    sender = 'hippos@chello.nl'
    title = "[dummy title]'  voor {roepnaam}"
    members = []
    mailGroups = []
# end of stub settings

_plain_text = {
        'EN': """
Please enable HTML in your mail client in order to see the full text of this email.     
            """,
        'NL': """
Gelieve HTML weergave in te stellen in uw email client om de vollige tekst
van deze mail te zien.
        """,
    }
    _html_text = {  # ultimately need to include something like....
# ...  h.p | ([(name, h.br) for name in files_to_attach]),
        'EN': h.em | ("just a stub for English HTML text!"),
        'NL': h.em | ("just a stub for Dutch HTML text!"),
    }

    def plain_text(self, taal):
        return self._plain_text[taal]


    def html_text(self, taal):
        return self._html_text[taal]


# 'gather' functionality not yet(?) ported from music_mailer.py.
# def gather(list_of_name_tuples, upper_dir): ..etc.

    def __init__(self):
        pass  # for now

    def main(self):
        script_filename = sys.argv.pop(0)
        script_shortname = os.path.split(script_filename)[1]
        ok_commands = ('show', 'take', 'check', 'send', 'quit')
        command = (sys.argv and sys.argv.pop(0))
        if sys.stdout.isatty():
            if not command:
                command = 'check'
        else:
            print ("Content-type: text/html;charset=UTF-8\n\n") # the blank line really matters!
            command = 'show'
        if command not in ok_commands:
            putmsg("error: %s is not one of %s." %(command, ok_commands))
            sys.exit(999)
        cwd = os.getcwd()
        path_elements = cwd.split(os.sep)
        mailing_id = path_elements.pop()
        if path_elements.pop() != MagicMailTreeName:
            putmsg("warning: %s is not within a '%s' directory." %(mailing_id, MagicMailTreeName))
            # sys.exit(997)

        # identify all possible attachments once only, before checking per-user.
        #
        # now look at each potential recipient in turn:
        #
        putmsg("Looking for subdirectories corresponding to mail groups...")
        for mailGroup in self.mailGroups:
            try:
                files_to_attach = os.listdir(mailGroup.name)
            except FileNotFoundError:
                putmsg ("warning: no subdirectory for mail group '%s' " % mailGroup.name)
                files_to_attach = None

            if not files_to_attach:
                # message below can get in the way, so maybe suppress it?:
                putmsg("I found nothing to attach so will not send mail at all to mailgroup '%s'"
                        % mailGroup.name)
                continue
            if not email_addr:
                putmsg ("We have no email address for %s."  % name)
                putmsg ("perhaps you need to putmsg the above would-be attachments?")
                continue
            # Create message container - the correct MIME type is multipart/alternative.
            msg = MIMEMultipart()
            subject = self.title.format(**locals())
            files_to_attach.sort()
            file_list = ",\n".join(['      %s' %filename for filename in files_to_attach])
            try:
                sender = self.sender
            except AttributeError:
                sender = "Gill and Larry Myerscough"
            putmsg('preparing mail for intrument (group) "%s"' % name)
            putmsg('    mail subject will be "%s"' % subject)
            putmsg('    mail will appear to come from "%s"' % sender)
            putmsg('    mail recipient(s) will be "%s"' % email_addr)
            putmsg('    mail attachment(s) will be ...\n%s' % file_list)
            message_id_string = None
            msg['From'] = email.utils.formataddr((str(Header(sender, 'utf-8')), 'hippos@chello.nl'))
            msg['Subject'] = subject
            msg['To'] = email_addr
            utc_from_epoch = time.time()
            msg['Date'] = email.utils.formatdate(utc_from_epoch, localtime=True)
            msg['Messsage-Id'] = email.utils.make_msgid(message_id_string)
            msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'

            textual_part = MIMEMultipart('alternative')
                          h.p | ([(name, h.br) for name in files_to_attach]),

            # Prepare both parts and insert them into the message container.
            # According to RFC 2046, the last part of a multipart message, in this case
            # the HTML message, is best and preferred.
            for template_text, subtype in (
                    (self.plain_text(), 'plain'),
                    (self.htnl_text(),  'html'),
            ):
                text = layout.format(**locals())
                sub_part =  MIMEText(text, subtype)
                textual_part.attach(sub_part)

            msg.attach(textual_part)

            for filename in files_to_attach:
                rel_name = os.path.join(name, filename)
                # Guess the content type based on the file's extension.  Encoding
                # will be ignored, although we should check for simple things like
                # gzip'd or compressed files.
                ctype, encoding = mimetypes.guess_type(rel_name)
                if ctype is None or encoding is not None:
                    # No guess could be made, or the file is encoded (compressed), so
                    # use a generic bag-of-bits type.
                    ctype = 'application/octet-stream'
                maintype, subtype = ctype.split('/', 1)
                with open(rel_name, 'rb') as attachment:
                    attachment_data = attachment.read()
                part = MIMEBase(maintype, subtype)
                part.set_payload(attachment_data)
                # Encode the payload using Base64
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(rel_name))
                msg.attach(part)
            putmsg ("length of message is %u bytes" % len(bytes(msg)))
            if command in ('show',):
                print(str(html_layout))
            elif command in ('q', 'quit'):
                sys.exit(0)
            elif command in ('s', 'send',): # 'send' in sys.argv:
                with smtplib.SMTP('smtp.upcmail.nl') as s:
                    s.send_message(msg)
                    putmsg ("mail has been sent to '%s'." % email_addr)


if __name__ == '__main__':
    _Mailshot().main()
