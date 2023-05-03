from rest_framework import serializers

from games.models import Games


# class GamesModel:
#     def __init__(self, title, content):
#         self.title = title
#         self.content = content
#
#
#
#

class GameSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Games
        fields = "__all__"

# Serializer by DONI
