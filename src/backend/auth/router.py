from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from jose import JWTError, jwt

from auth.schemas import Token
from auth import utils, crud

router = APIRouter(tags=["authentication"])


@router.post("/token", response_model=Token)
def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Validates credentials, sets Refresh Token in HttpOnly Cookie, returns Access Token.
    """
    user = crud.get_user_by_username(form_data.username)
    if not user or not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=utils.REFRESH_TOKEN_EXPIRE_DAYS)

    access_token = utils.create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )
    refresh_token = utils.create_refresh_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=refresh_token_expires
    )

    # SECURE COOKIE SETTING
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,  # JavaScript cannot read this (prevents XSS theft)
        max_age=int(refresh_token_expires.total_seconds()),
        expires=int(refresh_token_expires.total_seconds()),
        samesite="lax",  # CSRF protection
        secure=False  # Set to True in production (HTTPS only)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role,
        "access_token_expires_in": int(access_token_expires.total_seconds())
    }


@router.post("/refresh", response_model=Token)
def refresh_token(request: Request, response: Response):
    """
    Reads Refresh Token from Cookie, validates it, and rotates keys.
    """
    # 1. Get token from cookie instead of body
    refresh_token = request.cookies.get("refresh_token")

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not refresh_token:
        raise credentials_exception

    try:
        payload = jwt.decode(refresh_token, utils.SECRET_KEY, algorithms=[utils.ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = crud.get_user_by_username(username)
    if user is None:
        raise credentials_exception

    # 2. Rotate Tokens
    access_token_expires = timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=utils.REFRESH_TOKEN_EXPIRE_DAYS)

    new_access_token = utils.create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )
    new_refresh_token = utils.create_refresh_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=refresh_token_expires
    )

    # 3. Set New Cookie
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        max_age=int(refresh_token_expires.total_seconds()),
        expires=int(refresh_token_expires.total_seconds()),
        samesite="lax",
        secure=False
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "role": user.role,
        "access_token_expires_in": int(access_token_expires.total_seconds())
    }


@router.post("/logout")
def logout(response: Response):
    """
    Clears the HttpOnly cookie.
    """
    response.delete_cookie(key="refresh_token")
    return {"message": "Logged out successfully"}