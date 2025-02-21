from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import timedelta, datetime
import asyncio
import time

scheduler = AsyncIOScheduler()

async def async_func():
    print('run start')
    # Use asyncio.sleep instead of time.sleep for non-blocking sleep
    await asyncio.sleep(3)
    print('run complete')

# Start from current time
base_time = datetime.now()

# Schedule jobs with smaller intervals since we're now non-blocking
for i in range(100):
    run_date = base_time + timedelta(seconds=1 * i)  # Can use smaller intervals now
    scheduler.add_job(async_func, trigger='date', run_date=run_date, misfire_grace_time=60)

# Modify the main loop to use asyncio
async def main():
    scheduler.start()
    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

asyncio.run(main())
