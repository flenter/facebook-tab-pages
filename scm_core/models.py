from hashlib import sha1
from datetime import datetime

from django.db import models

from django.utils.encoding import smart_str
from django.utils.translation import ugettext_lazy as _


from core.fields import CodeField

import reversion

PUBLISH_STATE_DRAFT = 'draft'
PUBLISH_STATE_PUBLISHED = 'published'
PUBLISH_STATE_FOR_REVIEW = 'for_review'
PUBLISH_STATE_STALE = 'stale_content'

PUBLISH_STATES = (
    (PUBLISH_STATE_DRAFT, _('draft')),
    (PUBLISH_STATE_PUBLISHED, _('published')),
    (PUBLISH_STATE_FOR_REVIEW, _('for review')),
    (PUBLISH_STATE_STALE, _('Stale content')),
)


class LiveManager(models.Manager):
    """Live manager, checks for publish_date and state.

    .. note::
       it is not a failsafe way of retrieving data that is published. Keep using
       common sense while developing!
    """

#    def get_or_create(self, *args, **kwargs):
#        commit = kwargs.get("commit", 'default_is_true')
#        if commit == 'default_is_true':
#            commit = True
#        else:
#            del kwargs['commit']
#
#        if commit == False:
#            try:
#                return (self.get(**kwargs), False)
#            except self.model.DoesNotExist:
#                return (self.model(**dict((k, v) \
#                    for (k, v) in kwargs.items() if '__' not in k)), True)
#        return super(LiveManager, self).get_or_create(*args, **kwargs)
#
    def all(self, *args, **kwargs):
        return self.filter().all()

    def filter(self, *args, **kwargs):
        kwargs['publish_state'] = PUBLISH_STATE_PUBLISHED
        kwargs['publish_date__lte'] = datetime.now

        return super(LiveManager, self).filter(*args, **kwargs)

    def all(self, *args, **kwargs):
        kwargs['publish_state'] = PUBLISH_STATE_PUBLISHED
        kwargs['publish_date__lte'] = datetime.now
        return self.filter(*args, **kwargs)

    def count(self, *args, **kwargs):
        kwargs['publish_state'] = PUBLISH_STATE_PUBLISHED
        kwargs['publish_date__lte'] = datetime.now
        return self.filter(*args, **kwargs).count()

    def get(self, *args, **kwargs):
        kwargs['publish_state'] = PUBLISH_STATE_PUBLISHED
        kwargs['publish_date__lte'] = datetime.now

        return super(LiveManager, self).get(*args, **kwargs)

    def exclude(self, *args, **kwargs):
        return self.filter().exclude(*args, **kwargs)


class PublishItem(models.Model):
    """Basic model for publish/unpublish and date related stuff
    """
    publish_state = models.CharField(
        choices=PUBLISH_STATES,
        max_length=50,
        default=PUBLISH_STATE_PUBLISHED,
        verbose_name=_('publish state')
    )

    publish_date = models.DateTimeField(
        default=datetime.now,
        verbose_name=_('publish date')
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('date created')
    )

    date_modified = models.DateTimeField(
        auto_now=True,
        verbose_name=_('date modified')
    )

    def is_published(self):
        """returns true if the status == published and the datetime.now
        is >= publish_date
        """
        if(
            self.publish_date < datetime.now() and
            self.publish_state == PUBLISH_STATE_PUBLISHED):

            return True
        return False

    is_published.boolean = True

    class Meta():
        abstract = True

    objects = models.Manager()
    pubjects = LiveManager()


class ChangeTrackingMixin(object):

    # list of keys that will be monitored
    hashable_keys = []

    # hash_table that will store the hashes of a key

    def __init__(self, *args, **kwargs):

        self.hash_table = {}
        from inspect import getmodule

        from django.db.models.signals import post_init

        __class__ = self.__class__
        post_init.connect(
                ChangeTrackingMixin.handle_post_init,
                dispatch_uid="track::%s::post_init" % getmodule(__class__).__name__ + "." + __class__.__name__,
                sender=__class__)

        if not reversion.is_registered(self.__class__):
            reversion.register(self.__class__)

    def store_key_hash(self, store_obj, key):
        """Store a hash for a certain key in store_obj[key].

        Note: the stored value may be None if the value of the key is None or if a models.exceptions.ObjectDoesNotExist.
        Also keep in mind that relations are not being traversed. So only simple changes will be detected.
        """
        try:
            store_obj[key] = self.generate_hash(smart_str(getattr(self, key)))
        except models.exceptions.ObjectDoesNotExist:
            store_obj[key] = None

    @staticmethod
    def generate_hash(value):
        """Generate a sha1 hexdigest of a specific value (or return None if the value parameter is also None)
        """
        if value:
            return sha1(value).hexdigest()
        return None

    @staticmethod
    def handle_post_init(sender, instance=None, **kwargs):
        instance.store_initial_hashes()

    def get_changes(self):
        """Returns an array of keys that have been modified
        """

        changes = []

        # check for possible problems
        if len(self.hash_table.keys()) == 0 or \
                len(self.__class__.hashable_keys) == 0:
            raise ValueError("The hash table for changes does not contain any values and/or no hashable keys are defined")

        for key, value in self.hash_table.items():
            try:
                current_value = smart_str(getattr(self, key))
            except models.exceptions.ObjectDoesNotExist:
                current_value = None

            if not value == self.generate_hash(current_value):
                changes.append(key)

        return changes

    def store_initial_hashes(self):
        """Store the initial hashes into the instance's hash_table.clear.
        """
        for key in self.hashable_keys:
            self.store_key_hash(self.hash_table, key)

    def get_verbose_names(self, keys):

        verbose = []
        for key in keys:
            verbose.append(self._meta.get_field(key).verbose_name)

        return verbose

    @reversion.revision.create_on_success
    def save_revision(self, changes):
        reversion.revision.comment = "Storing from stream: " + ','.join(self.get_verbose_names(changes))
        self.save()

    @reversion.revision.create_on_success
    def save_as_stale(self, changes):
        self.publish_state = PUBLISH_STATE_STALE
        self.external_id = ''
        reversion.revision.comment = "Setting stale and maybe saving other changes: " + ','.join(self.get_verbose_names(changes))
        self.save()


class TestPubjectItem(PublishItem):
    """ Class made for unit testing...
    """
    title = models.CharField(max_length=255)
    code = CodeField(max_length=10)
