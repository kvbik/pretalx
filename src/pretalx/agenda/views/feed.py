from django.contrib.syndication.views import Feed
from django.http import Http404
from django.utils import feedgenerator


class ScheduleFeed(Feed):
    feed_type = feedgenerator.Atom1Feed
    description_template = "agenda/feed/description.html"

    def get_object(self, request, *args, **kwargs):
        if not request.user.has_perm("agenda.view_schedule", request.event):
            raise Http404()
        return request.event

    def title(self, obj):
        return f"{obj.name} schedule updates"

    def link(self, obj):
        return obj.urls.schedule.full()

    def feed_url(self, obj):
        return obj.urls.feed.full()

    def feed_guid(self, obj):
        return obj.urls.feed.full()

    def description(self, obj):
        return f"Updates to the {obj.name} schedule."

    def items(self, obj):
        return obj.schedules.filter(version__isnull=False).order_by("-published")

    def item_title(self, item):
        return f"New {item.event.name} schedule released ({item.version})"

    def item_link(self, item):
        url = item.event.urls.changelog.full()
        return f"{url}#{item.version}"

    def item_pubdate(self, item):
        return item.published
