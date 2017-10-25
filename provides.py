"""
A Juju charm interface for linking the cinder-storpool charm to the cinder one.
"""
from charms import reactive

from spcharms import utils as sputils


def rdebug(s):
    """
    Pass the diagnostic message string `s` to the central diagnostic logger.
    """
    sputils.rdebug(s, prefix='storpool-storage-backend-requires')


class CinderBackendProvides(reactive.RelationBase):
    """
    Just notify the charm when the relationship has been established.
    """
    scope = reactive.scopes.UNIT

    @reactive.hook('{provides:cinder-backend}-relation-{joined,changed}')
    def changed(self):
        """
        Handle a notification and set the "*.configure" state.
        """
        rdebug('relation-joined/changed invoked')
        reactive.set_state('storage-backend.configure')
