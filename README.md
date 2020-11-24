# check_willhem_new_apartments
A small util to scan willhem housing site periodically then mail back to receiver

In order to use the script, some environment variables are needed:
1. SENDER_MAIL: gmail address of the sender. Sorry, only gmail option is supported currently
2. SENDER_MAIL_PWD: send mail's password
3. RECEIVER_MAIL: receiver's mail. Of course, can be any domain.
4. After setting the environment variables, in the same terminal, issue: python check_for_new_apartment.py
