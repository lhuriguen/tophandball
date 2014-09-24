import hashlib
from django.db import models
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount


class UserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = ((FEMALE, 'Female'), (MALE, 'Male'))

    user = models.OneToOneField(User, related_name='profile')
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, blank=True, null=True)

    def __unicode__(self):
        return "{}'s profile".format(self.user.username)

    class Meta:
        db_table = 'user_profile'

    @property
    def profile_image_url(self):
        sa = SocialAccount.objects.filter(user_id=self.user.id)
        if len(sa):
            return sa[0].get_avatar_url()

        # Use Gravatar as fallback
        return 'http://www.gravatar.com/avatar/{}?s=80&d=identicon'.format(
            hashlib.md5(self.user.email).hexdigest())
        # return ''

    def admin_thumbnail(self):
        url = self.profile_image_url
        if url:
            return u'<img src="%s" />' % (url)
        else:
            return u'No Image'
    admin_thumbnail.short_description = 'Avatar preview'
    admin_thumbnail.allow_tags = True


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
