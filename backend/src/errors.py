from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status
from sqlalchemy.exc import SQLAlchemyError

class DbDashException(Exception):
    """This is the base class for all bookly errors"""

    pass


class InvalidToken(DbDashException):
    """User has provided an invalid or expired token"""

    pass


class RevokedToken(DbDashException):
    """User has provided a token that has been revoked"""

    pass


class AccessTokenRequired(DbDashException):
    """User has provided a refresh token when an access token is needed"""

    pass


class RefreshTokenRequired(DbDashException):
    """User has provided an access token when a refresh token is needed"""

    pass


class UserAlreadyExists(DbDashException):
    """User has provided an email for a user who exists during sign up."""

    pass


class AwsAccountAlreadyExists(DbDashException):
    """User has provided an email for a user who exists during sign up."""

    pass


class InvalidCredentials(DbDashException):
    """User has provided wrong email or password during log in."""

    pass


class InsufficientPermission(DbDashException):
    """User does not have the neccessary permissions to perform an action."""

    pass


class AwsAccountNotFound(DbDashException):
    """Account Not found"""

    pass


class UserNotFound(DbDashException):
    """User Not found"""

    pass

class InvalidParameters(DbDashException):
    """User Not found"""
    pass


class AccountNotVerified(Exception):
    """Account not yet verified"""
    pass

class PasswordIncorrect(DbDashException):
    """Account not yet verified"""
    pass

class JiraMetaNameAlreadyExists(DbDashException):
    """Account not yet verified"""
    pass

class ServerAlreadyExists(DbDashException):
    """Account not yet verified"""
    pass

class JiraMetaDataNotFound(DbDashException):
    """Account not yet verified"""
    pass    

class ServerNotFound(DbDashException):
    """Account not yet verified"""
    pass  

# Infrastructure
class ExternalServiceError(DbDashException):
    pass

class JiraUnavailableError(DbDashException):
    pass

class JiraAuthError(DbDashException):
    pass

# Domain
class InvalidIssueError(DbDashException):
    pass

class ProvisioningError(DbDashException):
    pass

# Persistence
class RepositoryError(DbDashException):
    pass

class JiraAlreadyExists(DbDashException):
    pass

class JobAlreadyExits(DbDashException):
    pass

class JiraTicketStatusChange(DbDashException):
    pass

def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:

    async def exception_handler(request: Request, exc: DbDashException):

        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler


def register_all_errors(app: FastAPI):
    app.add_exception_handler(
        PasswordIncorrect,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Password is incorrect",
                "error_code": "wrong_password",
            },
        ),
    )

    app.add_exception_handler(
        JobAlreadyExits,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Job with same parameters already in progress..",
                "error_code": "job_exists",
            },
        ),
    )  

    app.add_exception_handler(
        JiraTicketStatusChange,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Jira Ticket status cannot be changed",
                "error_code": "jira_isues",
            },
        ),
    ) 


    app.add_exception_handler(
        JiraAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Jira with same ticket number exists with not closed status",
                "error_code": "jira_exits",
            },
        ),
    )   

    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "User with email already exists",
                "error_code": "user_exists",
            },
        ),
    )

    app.add_exception_handler(
        UserNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "User not found",
                "error_code": "user_not_found",
            },
        ),
    )
    
    app.add_exception_handler(
        AwsAccountNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Account Not found",
                "error_code": "account_not_found",
            },
        ),
    )  
    
    app.add_exception_handler(
        AwsAccountNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Account Not found",
                "error_code": "account_not_found",
            },
        ),
    )   
    
    app.add_exception_handler(
        AwsAccountAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Aws Account with Same Account number already exists",
                "error_code": "account_exists",
            },
        ),
    )
    
    app.add_exception_handler(
        InvalidParameters,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Query parameters not valid",
                "error_code": "parameters_not_valid",
            },
        ),
    )
    
    app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Invalid Email Or Password",
                "error_code": "invalid_email_or_password",
            },
        ),
    )
    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Token is invalid Or expired",
                "resolution": "Please get new token",
                "error_code": "invalid_token",
            },
        ),
    )
    app.add_exception_handler(
        RevokedToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Token is invalid or has been revoked",
                "resolution": "Please get new token",
                "error_code": "token_revoked",
            },
        ),
    )
    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Please provide a valid access token",
                "resolution": "Please get an access token",
                "error_code": "access_token_required",
            },
        ),
    )
    app.add_exception_handler(
        RefreshTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Please provide a valid refresh token",
                "resolution": "Please get an refresh token",
                "error_code": "refresh_token_required",
            },
        ),
    )
    app.add_exception_handler(
        InsufficientPermission,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "You do not have enough permissions to perform this action",
                "error_code": "insufficient_permissions",
            },
        ),
    )

    app.add_exception_handler(
        AccountNotVerified,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Account Not verified",
                "error_code": "account_not_verified",
                "resolution":"Please check your email for verification details"
            },
        ),
    )

    @app.exception_handler(500)
    async def internal_server_error(request, exc):

        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


    @app.exception_handler(SQLAlchemyError)
    async def database__error(request, exc):
        print(str(exc))
        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    app.add_exception_handler(
        JiraMetaNameAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Jira Meta data with same name already exists",
                "error_code": "Metadata_exists",
            },
        ),
    )

    app.add_exception_handler(
        JiraMetaDataNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Jira Metadata Not found",
                "error_code": "metadata_not_found",
            },
        ),
    ) 

    app.add_exception_handler(
        ServerAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Server Already Exists",
                "error_code": "server_already_exits",
            },
        ),
    ) 

    app.add_exception_handler(
        ServerNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Server data not found",
                "error_code": "server_data_notfound",
            },
        ),
    ) 



    