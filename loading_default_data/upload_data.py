import asyncio
import csv

from random import randint as random_value
from sqlalchemy import insert, select, func

from src.database import async_session_maker
from src.transportation.models import Location, Car, Cargo
from src.transportation.utils import generate_unique_code


async def upload_cars(session):
    select_query = select(Location.id).order_by(func.random()).limit(20)
    result = await session.execute(select_query)
    data = result.scalars().all()
    for location_id in data:
        unique_id = await generate_unique_code(session)
        insert_query = insert(Car).values(
            unique_id=unique_id,
            current_location=int(location_id),
            load_capacity=int(random_value(1, 1000))
        )
        await session.execute(insert_query)
        await session.commit()


async def upload_cargos(session):
    select_query = select(Location.id).order_by(func.random()).limit(1000)
    result = await session.execute(select_query)
    data = result.scalars().all()
    for n in range(0, 500, 2):
        insert_query = insert(Cargo).values(
            pick_up=int(data[n]),
            delivery=int(data[n+1]),
            weight=int(random_value(1, 1000)),
            description=""
        )
        await session.execute(insert_query)
        await session.commit()


async def upload_locations():
    async with async_session_maker() as session:
        with open('loading_default_data/uszips.csv', "r", newline='') as f:
            data = csv.reader(f)
            for n, x in enumerate(data):
                if n > 0:
                    zip_code, lat, lng, city, state_id, state_name = x[:6]
                    query = insert(Location).values(
                        city=city,
                        state=state_name,
                        zip_code=int(zip_code),
                        lat=float(lat),
                        lon=float(lng)
                    )
                    await session.execute(query)
                    await session.commit()
        await upload_cars(session)
        await upload_cargos(session)


if __name__ == "__main__":
    asyncio.run(upload_locations())
