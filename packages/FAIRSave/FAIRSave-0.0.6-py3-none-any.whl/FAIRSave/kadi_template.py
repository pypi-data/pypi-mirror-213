from kadi_apy import KadiManager
import uuid
from typing import Optional


def Template_Create(*args, **kwargs):
    import warnings
    warnings.simplefilter('always', DeprecationWarning)
    warnings.warn('Warning! "Template_Create" will be renamed to '
                  '"create_template_kadi" in a future release!',
                  DeprecationWarning)
    return create_template_kadi(*args, **kwargs)

def create_template_kadi(data,
                         title: str,
                         instance: Optional[str] = None,
                         host: Optional[str] = None,
                         pat: Optional[str] = None,
                         group_id: Optional[int] = None):

    template_name_words = title.split(' ')[:2]

    template_name = '-'.join((template_name_word[:3]
                              for template_name_word
                              in template_name_words))

    template_name = template_name + '-'

    template = (KadiManager(instance=instance, host=host, token=pat)
                .template(title=title,
                          identifier=(template_name+str(uuid.uuid4())),
                          type='record',
                          data=data,
                          create=True))

    template.add_group_role(group_id=group_id, role_name='editor')
