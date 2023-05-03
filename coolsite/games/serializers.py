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
class GameSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()
    time_create = serializers.DateTimeField(read_only=True)
    time_update = serializers.DateTimeField(read_only=True)
    is_published = serializers.BooleanField(default=True)
    cat_id = serializers.IntegerField()
#
# def encode():
#     model = GamesModel('Chernobylite', 'Content: Chernobylite')
#     model_sr = GameSerializer(model)

