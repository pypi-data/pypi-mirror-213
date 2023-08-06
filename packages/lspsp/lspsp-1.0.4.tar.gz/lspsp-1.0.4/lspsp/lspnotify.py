import logging
import smtplib
from jinja2 import Environment, FileSystemLoader
import os

from lspsp.mailbuilder import MailBuilder


class LspNotify:
    def __init__(self, mode) -> None:
        self._logger = logging.getLogger(__name__)
        self._mode = mode

    def get_subject(self, content):
        if self._mode == 0:
            return '收件收发配置测试'
        elif self._mode == 1:
            return '发现LSPSP.ME新库存%d个' % (len(content))
        else:
            return '未知类型的邮件'

    def mail(self, config, content):
        root = os.path.dirname(__file__)
        path = os.path.join(root, 'resource')
        env = Environment(loader=FileSystemLoader(path))
        template_name = ''
        if self._mode == 0:
            template_name = 'test'
        else:
            template_name = 'mail'
        template = env.get_template(template_name + '.html')
        html_content = str(template.render(content=content))

        smtp = None
        if config['ssl']:
            smtp = smtplib.SMTP_SSL(config['host'], config['port'])
        else:
            smtp = smtplib.SMTP(config['host'], config['port'])
        smtp.login(config['usn'], config['pwd'])

        for item in config['recv']:
            builder = MailBuilder().content(html_content).frm(config['name'], config['usn']).to(
                item).subject(self.get_subject(content))
            message = builder.build()

            smtp.sendmail(config['usn'], item, message.as_string())
            self._logger.info("Email sended to: %s", item)
