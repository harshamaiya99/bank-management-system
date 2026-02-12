from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from jose import JWTError, jwt

from auth.schemas import Token
from auth import utils, crud

router = APIRouter(tags=["authentication"])


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Validates username/password and issues access and refresh tokens.
    """
    user = crud.get_user_by_username(form_data.username)
    if not user or not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Calculate expiration times
    access_token_expires = timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=utils.REFRESH_TOKEN_EXPIRE_DAYS)

    # Generate tokens
    access_token = utils.create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )
    refresh_token = utils.create_refresh_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=refresh_token_expires
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "role": user.role,
        "access_token_expires_in": int(access_token_expires.total_seconds()),
        "refresh_token_expires_in": int(refresh_token_expires.total_seconds())
    }


@router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str = Body(..., embed=True)):
    """
    Uses a refresh token to generate a new access/refresh token pair.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(refresh_token, utils.SECRET_KEY, algorithms=[utils.ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Verify user still exists
    user = crud.get_user_by_username(username)
    if user is None:
        raise credentials_exception

    # Calculate new expiration times
    access_token_expires = timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=utils.REFRESH_TOKEN_EXPIRE_DAYS)

    # Generate new tokens (Rotating refresh tokens is recommended security practice)
    new_access_token = utils.create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )
    new_refresh_token = utils.create_refresh_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=refresh_token_expires
    )

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
        "role": user.role,
        "access_token_expires_in": int(access_token_expires.total_seconds()),
        "refresh_token_expires_in": int(refresh_token_expires.total_seconds())
    }