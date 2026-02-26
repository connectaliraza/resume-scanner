import asyncio
import logging

from app_context import AppContext

# from app.logger.logging_setup import setup_logging

# setup_logging()

logger = logging.getLogger(__name__)


async def main():
    """
    Main application entry point using async/await properly.
    """
    logger.info("**** Starting Resume Scanner API ****")

    try:
        # Initialize application
        logger.info("Initializing application (async)...")
        await AppContext.initialize()
        logger.info("Application initialized successfully")

        # Start API - uvicorn will manage the event loop
        logger.info("Starting API server...")
        await AppContext.api.start()

    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise
    finally:
        # Cleanup
        logger.info("**** Shutting down Resume Scanner API ****")
        try:
            await AppContext.shutdown()
        except Exception as e:
            logger.error(f"Error during shutdown: {str(e)}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
