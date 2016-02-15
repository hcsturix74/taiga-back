# Copyright (C) 2014-2015 Andrey Antukh <niwi@niwi.be>
# Copyright (C) 2014-2015 Jesús Espino <jespinog@gmail.com>
# Copyright (C) 2014-2015 David Barragán <bameda@dbarragan.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from taiga.base.api import serializers

from . import services
from . import models


class AttachmentSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField("get_url")
    thumbnail_card_url = serializers.SerializerMethodField("get_thumbnail_card_url")
    attached_file = serializers.FileField(required=True)
    is_video = serializers.SerializerMethodField("get_is_video")
    markers = serializers.SerializerMethodField("get_markers")


    class Meta:
        model = models.Attachment
        fields = (
            "id", "project", "owner", "name", "attached_file", "size",
            "url", "thumbnail_card_url", "description", "is_deprecated",
            "created_date", "modified_date", "object_id", "order", "sha1",
            "is_video", "markers"
        )
        read_only_fields = (
            "owner", "created_date", "modified_date", "sha1",
        )

    def get_url(self, obj):
        return obj.attached_file.url

    def get_thumbnail_card_url(self, obj):
        return services.get_card_image_thumbnailer_url(obj)

    def get_is_video(self, obj):
        if '.mp4' in obj.attached_file.url:
            return True
        else:
            return False

    def get_sources(self, obj):
        if self.get_is_video(obj):
            sources = dict(
                src=obj.attached_file.url,
                type='video/mp4'
            )
            return dict(sources=[sources, ])
        return False

    def get_markers(self, obj):
        if self.get_is_video(obj):
            return [
                {'time': 9.5, 'text': "this"},
                {'time': 16, 'text': "is"},
                {'time': 23.6, 'text': "so"},
                {'time': 28, 'text': "cool"}
            ]
        return []