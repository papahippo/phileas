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
from phileas.admin import Vereniging
MagicMailTreeName = 'MagicMailTree'
# ok_exts = ('.pdf', '.jpg', '.jpeg')


class Mailing_:
# start of stub settings
    sender = 'hippos@chello.nl'
    title = "{grouping.name}: Mailing '{mailing_name}'  voor {mailGroup.name}"
    grouping = Vereniging()
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

    def get_plain_text(self, recipients=[], mailGroup=None, file_list=[], taal='NL'):
        return self._plain_text[taal]


    def get_html_text(self, recipients=[], mailGroup=None, file_list=[], taal='NL'):
        # the html tagging probably doesn't belong here (musicraft..pyraft.html needs looking at!)
        return self._html_text[taal]

    def putmsg(self, this_verbosity, *pp, **kw):
        if self.verbosity >= this_verbosity:
            return print(*pp, file=sys.stderr, **kw)

# 'gather' functionality not yet(?) ported from music_mailer.py.
# def gather(list_of_name_tuples, upper_dir): ..etc.

    def __init__(self):
        pass  # for now

    def main(self):

        script_filename = sys.argv.pop(0)
        script_shortname = os.path.split(script_filename)[1]
        # maling_name, _ext = os.path.splitext(script_shortname)
        self.verbosity = 42 + sum([a in ('-v', '--verbose') for a in sys.argv])
        non_kw_args = [arg for arg in sys.argv if arg[0]!='-']
        ok_commands = ('check', 'send', 'quit')
        command = (non_kw_args and non_kw_args.pop(0))
        if not command:
            command = 'check'
        if command not in ok_commands:
            self.putmsg(-1, "error: %s is not one of %s." %(command, ok_commands))
            sys.exit(999)
        stdouttype = (non_kw_args and non_kw_args.pop(0))
        if not stdouttype:
            if sys.stdout.isatty():
                stdouttype = 'plain'
            else:
                stdouttype = 'html'
                print ("Content-type: text/html;charset=UTF-8\n\n") # the blank line really matters!
        cwd = os.getcwd()
        path_elements = cwd.split(os.sep)
        mailing_name = path_elements.pop()
        if path_elements.pop() != MagicMailTreeName:
            self.putmsg(0, "warning: %s is not within a '%s' directory." %(mailing_name, MagicMailTreeName))
            # sys.exit(997)

        # identify all possible attachments once only, before checking per-user.
        #
        # now look at each potential recipient in turn:
        #
        grouping = self.grouping  # for benifit of text templates!

        self.putmsg(1, "Looking for subdirectories corresponding to mail groups...", self.mailGroups)
        for mailGroup in self.mailGroups.contents:
            self.putmsg(1, "Dealing with mailgroup '%s'" % mailGroup.name)
            try:
                files_to_attach = os.listdir(mailGroup.name)
            except FileNotFoundError:
                self.putmsg (0, "warning: no subdirectory for mail group '%s' " % mailGroup.name)
                files_to_attach = None

            if not files_to_attach:
                # message below can get in the way, so maybe suppress it?:
                self.putmsg(1, "I found nothing to attach so will not send mail at all to mailgroup '%s'"
                        % mailGroup.name)
                continue
            recipients = []
            for member in mailGroup.contents:
                #if mailGroup not in member.mailingList:
                #    continue
                if not member.emailAddress:
                    self.putmsg (0, "We have no email address for %s."  % member.name)
                    self.putmsg (0, "perhaps you need to print the above would-be attachments?")
                    continue
                recipients.append(member)
            if not recipients:
                self.putmsg(1, "No-one needs to receive mail for mailgroup '%s'..." % mailGroup.name)
                self.putmsg(1, "... so we won't send any!")
                continue
            field_To_as_string = ', '.join([recipient.emailAddress
                                            for recipient in recipients])
            self.putmsg(1, '"%s" need to receive this particular mail' %field_To_as_string)
            # Create message container - the correct MIME type is multipart/alternative.
            msg = MIMEMultipart()
            subject = self.title.format(**locals())
            files_to_attach.sort()
            file_list = ",\n".join(['      %s' %filename for filename in files_to_attach])
            try:
                sender = self.sender
            except AttributeError:
                sender = "Gill and Larry Myerscough"
            self.putmsg(1, 'preparing mail for mailgroup "%s"' % mailGroup.name)
            self.putmsg(1, '    mail subject will be "%s"' % subject)
            self.putmsg(1, '    mail will appear to come from "%s"' % sender)
            self.putmsg(1, '    mail recipient(s) will be "%s"' % field_To_as_string)
            self.putmsg(1, '    mail attachment(s) will be ...\n%s' % file_list)
            message_id_string = None
            msg['From'] = email.utils.formataddr((str(Header(sender, 'utf-8')), 'hippos@chello.nl'))
            msg['Subject'] = subject
            msg['To'] = field_To_as_string
            utc_from_epoch = time.time()
            msg['Date'] = email.utils.formatdate(utc_from_epoch, localtime=True)
            msg['Messsage-Id'] = email.utils.make_msgid(message_id_string)
            msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'

            textual_part = MIMEMultipart('alternative')

            # Prepare both parts and insert them into the message container.
            # According to RFC 2046, the last part of a multipart message, in this case
            # the HTML message, is best and preferred.
            for text_getter, subtype in (
                    (self.get_plain_text, 'plain'),
                    (self.get_html_text,  'html'),
            ):
                text = text_getter(recipients = recipients, mailGroup=mailGroup,
                                   file_list=file_list, ) # .format(**locals())
                if subtype == stdouttype:
                    # Temporary? complication
                    if subtype == 'text':
                        print(str(text).format(**locals()))
                    else:
                        print(h.html | str(text).format(**locals()))
                        #print(h.html | ("humph", h.b | "bold"))
                sub_part =  MIMEText(str(text), subtype)
                textual_part.attach(sub_part)

            msg.attach(textual_part)

            for filename in files_to_attach:
                rel_name = os.path.join(mailGroup.name, filename)
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
            self.putmsg (1, "length of message is %u bytes" % len(bytes(msg)))
            if command in ('q', 'quit', 'htlm' 'plain'):
                sys.exit(0)
            elif command in ('s', 'send',): # 'send' in sys.argv:
                with smtplib.SMTP('smtp.upcmail.nl') as s:
                    s.send_message(msg)
                    self.putmsg (0, "mail has been sent to '%s'." % field_To_as_string)


if __name__ == '__main__':
    Mailing_().main()
