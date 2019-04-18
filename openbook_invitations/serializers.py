from django.conf import settings
from rest_framework import serializers
from openbook.settings import PROFILE_NAME_MAX_LENGTH
from openbook_invitations.models import UserInvite
from openbook_auth.models import User
from openbook_invitations.validators import invite_id_exists, check_invite_not_used


class CreateUserInviteSerializer(serializers.Serializer):
    nickname = serializers.CharField(
        max_length=PROFILE_NAME_MAX_LENGTH,
        required=True,
        allow_blank=False)


class InvitedUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username'
        )


class GetUserInviteSerializer(serializers.ModelSerializer):
    created_user = InvitedUserSerializer(many=False)

    class Meta:
        model = UserInvite
        fields = (
            'id',
            'email',
            'is_invite_email_sent',
            'nickname',
            'token',
            'created_user',
            'created'
        )


class GetUserInvitesSerializer(serializers.Serializer):
    count = serializers.IntegerField(
        required=False,
        max_value=20
    )
    offset = serializers.IntegerField(
        required=False,
    )
    status = serializers.ChoiceField(required=False, choices=[
        'ALL',
        'PENDING',
        'ACCEPTED'
    ])


class SearchUserInvitesSerializer(serializers.Serializer):
    count = serializers.IntegerField(
        required=False,
        max_value=20
    )
    status = serializers.ChoiceField(required=False, choices=[
        'ALL',
        'PENDING',
        'ACCEPTED'
    ])
    query = serializers.CharField(
        max_length=settings.SEARCH_QUERIES_MAX_LENGTH,
        allow_blank=False,
        required=True
    )


class DeleteUserInviteSerializer(serializers.Serializer):
    invite_id = serializers.IntegerField(
        validators=[invite_id_exists],
        required=True,
    )


class EditUserInviteSerializer(serializers.Serializer):
    invite_id = serializers.IntegerField(
        validators=[invite_id_exists],
        required=True,
    )
    nickname = serializers.CharField(
        max_length=PROFILE_NAME_MAX_LENGTH,
        required=True,
        allow_blank=False)


class EmailUserInviteSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    invite_id = serializers.IntegerField(
        validators=[check_invite_not_used],
        required=True,
    )