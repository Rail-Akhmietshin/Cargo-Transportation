from sqlalchemy import select, func, update
import asyncio

from src.database import async_session_maker
from src.celery import celery_app
from .models import Location, Car


async def update_location_cars():
    async with async_session_maker() as session:
        select_locations_id = select(Location.id).order_by(func.random()).limit(20)
        location_select_response = await session.execute(select_locations_id)
        locations = location_select_response.scalars().all()

        select_cars_id = select(Car.id)
        car_select_response = await session.execute(select_cars_id)
        cars = car_select_response.scalars().all()

        for location_id, car_id in zip(locations, cars):
            update_query = update(Car).values(
                current_location=int(location_id),
            ).where(
                Car.id == car_id
            )
            await session.execute(update_query)
            await session.commit()


@celery_app.task
def start_func():
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(update_location_cars())
