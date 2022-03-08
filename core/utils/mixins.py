from core.tools.common import slugify


class ChatGroupMixin:
    def __set_slug__(self):
        if self.cache_group_name != self.group_name:
            from core.models import ChatGroup

            new_slug = slugify(self.group_name)
            difference = 1
            while ChatGroup.objects.filter(slug=new_slug).exists():
                new_slug = slugify(self.group_name) + str(difference)
                difference += 1

            self.slug = new_slug
