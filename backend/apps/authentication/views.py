"""
인증 관련 뷰
"""
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from common.utils import success_response, error_response
from .models import User
from .serializers import (
    UserSerializer,
    SignupSerializer,
    LoginSerializer,
    PasswordChangeSerializer
)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """회원가입"""
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user_data = UserSerializer(user).data
        return success_response(
            data=user_data,
            message="회원가입이 완료되었습니다.",
            status_code=status.HTTP_201_CREATED
        )
    return error_response(
        message="회원가입에 실패했습니다.",
        details=serializer.errors,
        status_code=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """로그인"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            # JWT 토큰 생성
            refresh = RefreshToken.for_user(user)

            return success_response(
                data={
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                    }
                },
                message="로그인에 성공했습니다."
            )
        else:
            return error_response(
                message="아이디 또는 비밀번호가 올바르지 않습니다.",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

    return error_response(
        message="로그인 정보를 확인해주세요.",
        details=serializer.errors,
        status_code=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """로그아웃"""
    try:
        refresh_token = request.data.get("refresh")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return success_response(message="로그아웃되었습니다.")
    except Exception as e:
        return error_response(
            message="로그아웃에 실패했습니다.",
            details=str(e),
            status_code=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    """현재 사용자 정보 조회"""
    serializer = UserSerializer(request.user)
    return success_response(data=serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_info(request):
    """사용자 정보 수정"""
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return success_response(
            data=serializer.data,
            message="정보가 수정되었습니다."
        )
    return error_response(
        message="정보 수정에 실패했습니다.",
        details=serializer.errors
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """비밀번호 변경"""
    serializer = PasswordChangeSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user

        # 기존 비밀번호 확인
        if not user.check_password(serializer.validated_data['old_password']):
            return error_response(
                message="기존 비밀번호가 올바르지 않습니다.",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # 새 비밀번호 설정
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return success_response(message="비밀번호가 변경되었습니다.")

    return error_response(
        message="비밀번호 변경에 실패했습니다.",
        details=serializer.errors
    )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    """회원 탈퇴"""
    user = request.user
    user.is_active = False
    user.save()
    return success_response(message="회원 탈퇴가 완료되었습니다.")
