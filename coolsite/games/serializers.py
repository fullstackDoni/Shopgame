from rest_framework import serializers

from games.models import Games


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Games
        fields = ('title', 'cat_id')
