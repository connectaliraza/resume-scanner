import logging
from typing import Optional

from app.api.base_components import BaseAPI
from app.api.resume_scanner.controllers import ResumeScannerController
from app.api.resume_scanner.repositories import ResumeRepository
from app.api.resume_scanner.services import ResumeScannerService
from app.api.user_management.controllers import UserManagementController
from app.api.user_management.services import UserManagementService
from app.db.database import Database
from app.exceptions.exception_handlers import resume_processing_exception_handler
from app.exceptions.exceptions import ResumeProcessingError

logger = logging.getLogger(__name__)
# config = AppConfig.from_yaml()


class AppContext:
    """Application context for dependency injection and initialization."""

    # Configuration

    # Service instances (initialized later)
    user_management_service: Optional[UserManagementService] = None
    resume_scanner_service: Optional[ResumeScannerService] = None

    api: Optional[BaseAPI] = None
    controllers: list = []

    _initialized: bool = False

    @classmethod
    async def initialize(cls) -> None:
        """
        Initialize all application services asynchronously.

        This must be called during application startup.

        Raises:
            RuntimeError: If already initialized
            Exception: If initialization fails
        """
        if cls._initialized:
            logger.warning("AppContext already initialized")
            return

        try:
            logger.info("Initializing AppContext...")

            # Database initialization

            # Services
            logger.info("Initializing services...")
            cls.user_management_service = UserManagementService()

            # Initialize database and repository for resume scanner
            db = Database()
            resume_repository = ResumeRepository(db)
            cls.resume_scanner_service = ResumeScannerService(resume_repository)

            logger.info("Services initialized successfully")

            # Controllers
            logger.info("Initializing controllers...")
            api_version = "v1"
            cls.controllers = [
                UserManagementController(cls.user_management_service, api_version),
                ResumeScannerController(cls.resume_scanner_service, api_version),
            ]
            logger.info("Controllers initialized successfully")

            # API
            logger.info("Initializing API...")
            cls.api = BaseAPI(
                ip="0.0.0.0",
                port=8000,
                debug=True,
                title="Resume Scanner API",
                description="API for parsing and managing resumes.",
                version="1.0.0",
                summary="Resume Scanner API",
            )

            # Register controllers
            cls.api.register_controllers(controllers=cls.controllers)
            cls.api.register_exception_handlers(
                [(ResumeProcessingError, resume_processing_exception_handler)]
            )
            logger.info("Controllers registered successfully")

            # Register exception handlers

            logger.info("API initialized successfully")

            cls._initialized = True
            logger.info("AppContext initialization complete")

        except Exception as e:
            logger.error(f"Failed to initialize AppContext: {str(e)}")
            raise

    @classmethod
    async def shutdown(cls) -> None:
        """Shutdown application context and cleanup resources."""
        try:
            logger.info("Shutting down application context")

            cls._initialized = False
            logger.info("Application context shutdown complete")

        except Exception as e:
            logger.error(f"Error during application shutdown: {str(e)}")
            raise

    @classmethod
    def is_initialized(cls) -> bool:
        """Check if AppContext is initialized."""
        return cls._initialized

    @classmethod
    def ensure_initialized(cls) -> None:
        """
        Ensure AppContext is initialized.

        Raises:
            RuntimeError: If not initialized
        """
        if not cls._initialized:
            raise RuntimeError(
                "AppContext not initialized. "
                "Call 'await AppContext.initialize()' first."
            )
