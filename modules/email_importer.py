import imaplib
import email
from email.header import decode_header

# Função para acessar o e-mail e importar releases
def import_releases(email_user, email_pass, keywords, server='imap.gmail.com', port=993):
    try:
        # Conectar ao servidor de e-mail
        mail = imaplib.IMAP4_SSL(server, port)
        mail.login(email_user, email_pass)
        print("Conexão com o servidor de e-mail estabelecida com sucesso.")

        # Selecionar a caixa de entrada
        mail.select("inbox")

        # Procurar por e-mails não lidos
        status, messages = mail.search(None, 'UNSEEN')
        if status != "OK":
            print("Erro ao procurar e-mails: ", status)
            return []

        emails = messages[0].split()
        print(f"{len(emails)} e-mails não lidos encontrados.")

        releases = []

        for mail_id in emails:
            status, msg_data = mail.fetch(mail_id, "(RFC822)")
            if status != "OK":
                print(f"Erro ao buscar e-mail ID {mail_id}: ", status)
                continue

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])

                    # Decodificar o assunto do e-mail
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")

                    # Obter o remetente do e-mail
                    from_ = msg.get("From")

                    # Obter o corpo do e-mail
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))

                            try:
                                body = part.get_payload(decode=True).decode()
                            except:
                                body = ""
                                pass

                            if "attachment" not in content_disposition:
                                releases.append({
                                    "subject": subject,
                                    "from": from_,
                                    "body": body
                                })
                    else:
                        content_type = msg.get_content_type()
                        body = msg.get_payload(decode=True).decode()
                        releases.append({
                            "subject": subject,
                            "from": from_,
                            "body": body
                        })
                    print(f"Release adicionado: Assunto - {subject}, De - {from_}")

                    # Verificar se o e-mail deve ser arquivado
                    if any(keyword.lower() in subject.lower() or keyword.lower() in body.lower() for keyword in keywords):
                        print(f"Arquivando e-mail: Assunto - {subject}, De - {from_}")
                        mail.store(mail_id, '+FLAGS', '\\Seen')
                        mail.copy(mail_id, 'Archived')
                        mail.store(mail_id, '+FLAGS', '\\Deleted')
                        mail.expunge()

        mail.logout()
        print(f"Total de releases importados: {len(releases)}")
        return releases

    except imaplib.IMAP4.error as e:
        print(f"Erro de conexão: {str(e)}")
        return []
