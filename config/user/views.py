from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from .serializers import RegisterSerializer
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import logout
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(["POST"])
def registration_view(request):
    # Initialize the serializer with the data from the request
    serializer = RegisterSerializer(data=request.data)

    # Check if the serializer is valid
    if serializer.is_valid():
        # Save the user account
        account = serializer.save()

        # Generate the refresh and access tokens for the user
        refresh = RefreshToken.for_user(account)

        # Prepare the response data
        data = {
            "token": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            "user": {"username": account.username, "email": account.email},
        }

        # Return the response with the token data and HTTP status 201 Created
        return Response(data, status=status.HTTP_201_CREATED)

    # If the serializer is not valid, return the validation errors
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST',])
# @authentication_classes([TokenAuthentication])
# def logout_view(request):
#   if request.method == 'POST':
#     request.user.auth.token.delete()
#     return Response(status=status.HTTP_200_OK)


# def logout_view(request):
#     logout(request)  # This logs out the user by removing their session data.
#     return JsonResponse({'message': 'Successfully logged out'})


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
def logout_view(request):
    # Get the user who is logged in
    user = request.user

    # Try to get the token associated with the user and delete it
    try:
        token = Token.objects.get(user=user)
        token.delete()
    except Token.DoesNotExist:
        pass  # If no token exists, do nothing

    # Optionally log out the user from the session (if using session-based authentication)
    # logout(request)

    # Return a response indicating success
    return Response(
        {"message": "Successfully logged out and token deleted."},
        status=status.HTTP_200_OK,
    )
