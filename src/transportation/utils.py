import string
from typing import Sequence, Any

from sqlalchemy import select, Row
from sqlalchemy.ext.asyncio import AsyncSession

from src.transportation.models import Car, Location, Cargo
from random import randint as random_value
from random import choice as random_choice
from geopy.distance import geodesic as get_distance


async def generate_unique_code(session: AsyncSession):
    while True:
        unique_id = str(random_value(1000, 9999)) + random_choice(string.ascii_uppercase)

        select_query = select(Car.unique_id).where(Car.unique_id == unique_id)
        result = await session.execute(select_query)
        data = result.scalars().first()
        if not data:
            return unique_id


async def get_current_location(zip_code: int, session: AsyncSession):
    location_select_query = select(Location.id).where(Location.zip_code == zip_code)
    response = await session.execute(location_select_query)
    location_id = response.scalars().one()
    return location_id


async def cars_to_cargo_pick_up(
        cargos: Sequence[Row[tuple[Any, ...]]],
        car_locations: list,
        max_distance: int,
        session: AsyncSession
):
    car_and_cargos = []

    for cargo_location in cargos:
        current_cars = 0
        for car_location in car_locations:
            distance = round(get_distance(cargo_location[:2], car_location).mi)
            if distance <= max_distance:
                current_cars += 1
        if current_cars:
            cargos_delivery = await get_cargo_delivery(cargo_location[4], session)
            car_and_cargos.append({
                "Pick up": ", ".join(cargo_location[2:4]),
                "Delivery": ", ".join(cargos_delivery),
                "Count cars": current_cars
            })
    return car_and_cargos


async def get_cargo_pick_up(session: AsyncSession):
    cargo_pick_up_query = select(
        Location.lat, Location.lon, Location.city, Location.state, Cargo.id
    ).join(
        Cargo, Cargo.pick_up == Location.id
    )
    response_cargo_pick_up = await session.execute(cargo_pick_up_query)
    return response_cargo_pick_up.fetchall()


async def get_cargo_delivery(where_parameter: int, session: AsyncSession):
    cargo_delivery_query = select(
        Location.city, Location.state
    ).join(
        Cargo, Cargo.delivery == Location.id
    ).where(
        Cargo.id == where_parameter
    )
    response_cargo_delivery = await session.execute(cargo_delivery_query)
    return response_cargo_delivery.fetchone()


async def get_car_locations(session: AsyncSession):
    car_locations_query = select(
        Location.lat, Location.lon
    ).join(
        Car, Car.current_location == Location.id
    )
    response_car_locations = await session.execute(car_locations_query)
    return response_car_locations.fetchall()


async def get_cargo_with_locations(cargo_id: int, session: AsyncSession):
    cargo_pick_up_query = select(
        Location.lat, Location.lon, Location.city, Location.state, Cargo.weight, Cargo.description
    ).join(
        Cargo, Cargo.pick_up == Location.id
    ).where(
        Cargo.id == cargo_id
    )
    car_locations_query = select(
        Location.lat, Location.lon, Car.unique_id
    ).join(
        Car, Car.current_location == Location.id
    )
    response_cargo_pick_up = await session.execute(cargo_pick_up_query)
    response_car_locations = await session.execute(car_locations_query)
    cargo_pick_up = response_cargo_pick_up.fetchone()
    car_locations = response_car_locations.fetchall()
    return cargo_pick_up, car_locations


async def cargos_and_locations_with_suitable_weight(weight: float, session: AsyncSession):
    request_with_suitable_weights = select(
        Location.lat, Location.lon, Location.city, Location.state, Cargo.id, Cargo.weight, Cargo.description
    ).join(
        Cargo, Cargo.pick_up == Location.id
    ).where(
        Cargo.weight == weight
    )
    response = await session.execute(request_with_suitable_weights)
    return response.fetchall()
