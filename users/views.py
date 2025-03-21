from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model,logout
from .serializers import UserLoginSerializer,UserRegistrationSerializer,UserSerializer
from .models import CustomUser

User = get_user_model()


class UserListView(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer


class UserRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            # Save the new user
            user = serializer.save()
            
            # Prepare the user data for the response
            user_data = {
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "image": user.image.url if user.image else None  # Handle image URL if provided
            }
            
            # Return a success message and user details
            return Response({
                "success": True,
                "message": "User registered successfully",

            }, status=status.HTTP_201_CREATED)
        
        # If the serializer is not valid, return the validation errors
        return Response({
            "message": "User registration failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            print(email)
            print(password)
            try:
                user = CustomUser.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                print(user)
                if user is not None:
                    token, _ = Token.objects.get_or_create(user=user)
                    
                    # Role-based login logic
                    if user.role == 'admin':
                        return Response({
                            "message": "Admin login successful!",
                            "token": token.key,
                            "user_id": user.id,
                            "role": user.role
                        })
                    elif user.role == 'medicine_manager':
                        return Response({
                            "message": "Medicine Manager login successful!",
                            "token": token.key,
                            "user_id": user.id,
                            "role": user.role
                        })
                    elif user.role == 'order_manager':
                        return Response({
                            "message": "Order Manager login successful!",
                            "token": token.key,
                            "user_id": user.id,
                            "role": user.role
                        })
                    else:
                        return Response({"message": "Invalid role."}, status=400)
                else:
                    return Response({"message": "Invalid email or password."}, status=400)
            except CustomUser.DoesNotExist:
                return Response({"message": "User not found."}, status=400)
        
        return Response(serializer.errors, status=400)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful!",
                         "success": True}, status=200)