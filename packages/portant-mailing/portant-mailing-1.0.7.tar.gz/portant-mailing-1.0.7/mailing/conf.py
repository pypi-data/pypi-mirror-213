from appconf import AppConf

from django.conf import settings  # noqa


def resolve(setting, **kwargs):
    """Resolve setting to a result of a callable or itself."""
    if hasattr(setting, '__call__'):
        return setting(**kwargs)
    return setting


class MailingAppConf(AppConf):

    EMAIL_FROM = ''
    SEND_TASK = 'mailing.tasks.send_mail_task'
    WHITELIST = []

    class Meta:
        prefix = 'mailing'
        required = []

    def configure_send_task(self, value):
        if hasattr(value, '__call__'):
            return value

        # Try resolving a setting to a fully qualified name
        # of a function, return the function object if found
        try:
            modname, part_symbol, attr = value.rpartition('.')
            assert part_symbol == '.', value
            assert modname != '', value
        except Exception:
            return value

        try:
            m = __import__(modname, fromlist=[attr])
            f = getattr(m, attr)
            return f
        except Exception:
            raise
