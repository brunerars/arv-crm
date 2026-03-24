import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    from workers.sla_scheduler import check_sla_violations

    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_sla_violations, "interval", hours=1, id="sla_check")
    scheduler.start()
    logger.info("Workers started - SLA scheduler running every hour")

    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
