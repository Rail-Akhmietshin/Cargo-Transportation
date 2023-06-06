from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, delete, update

from sqlalchemy.ext.asyncio import AsyncSession

from geopy.distance import geodesic as get_distance
from starlette import status
from starlette.responses import JSONResponse

from .models import Location, Cargo, Car
from .schemas import CargoCreate, CarUpdate, CargoUpdate
from src.database import get_async_session
from .utils import (
    get_cargo_pick_up, get_car_locations, get_cargo_delivery, get_cargo_with_locations,
    cars_to_cargo_pick_up, get_current_location, cargos_and_locations_with_suitable_weight
)

router = APIRouter(
    prefix="/transportation",
    tags=["Transportation"]
)


@router.post("/cargo")
async def add_cargo(cargo: CargoCreate, session: AsyncSession = Depends(get_async_session)):
    select_query = select(Location.id).where(
        Location.zip_code.in_((cargo.pick_up, cargo.delivery))
    )
    response = await session.execute(select_query)
    pick_up, delivery = response.scalars().all()

    insert_query = insert(Cargo).values(
        pick_up=pick_up,
        delivery=delivery,
        weight=cargo.weight,
        description=cargo.description
    )
    await session.execute(insert_query)
    await session.commit()


@router.get("/cargos")
async def get_cargos(session: AsyncSession = Depends(get_async_session)):
    cargos = await get_cargo_pick_up(session)
    car_locations = await get_car_locations(session)

    suitable_car_to_cargos = await cars_to_cargo_pick_up(cargos, car_locations, 450, session)

    return suitable_car_to_cargos


@router.get("/cargo")
async def get_cargo(cargo_id: int, session: AsyncSession = Depends(get_async_session)):
    cargo_pick_up, car_locations = await get_cargo_with_locations(cargo_id, session)
    cargos_delivery = await get_cargo_delivery(cargo_id, session)

    title = " ".join([
        f"From: {cargo_pick_up.city}, {cargo_pick_up.state};",
        f"To: {cargos_delivery.city}, {cargos_delivery.state};",
        f"Weight: {cargo_pick_up.weight} kg;"
    ])
    if cargo_pick_up.description:
        title += f"Description: {cargo_pick_up.description}"

    data = {title: []}
    for car_location in car_locations:
        distance = get_distance(car_location[:2], cargo_pick_up[:2]).mi
        data[title].append({
            f"Идентификатор машины: {car_location[2]}": f"Расстояние: {round(distance)} mi"
        })
    return data


@router.put("/cargo")
async def update_cargo(cargo: CargoUpdate, session: AsyncSession = Depends(get_async_session)):
    update_query = update(Cargo).where(
        Cargo.id == cargo.id
    ).values(
        weight=cargo.weight,
        description=cargo.description
    )
    await session.execute(update_query)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "Статус выполнения запроса": "Данные о грузе успешно обновлены"
        }
    )


@router.delete("/cargo")
async def delete_cargo(cargo_id: int, session: AsyncSession = Depends(get_async_session)):
    query = delete(Cargo).where(Cargo.id == cargo_id)
    await session.execute(query)
    await session.commit()
    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT,
        content={
            "Статус выполнения запроса": "Груз успешно удален из базы данных"
        })


@router.get("/filters/cargos")
async def filter_cargos(
        weight: float = None,
        distance: int = None,
        session: AsyncSession = Depends(get_async_session)
):
    if (weight and distance) or distance:
        if weight and distance:
            cargos = await cargos_and_locations_with_suitable_weight(weight, session)
        else:
            cargos = await get_cargo_pick_up(session)

        car_locations = await get_car_locations(session)
        suitable_cars_to_cargo_pick_up = await cars_to_cargo_pick_up(cargos, car_locations, distance, session)
        return suitable_cars_to_cargo_pick_up
    else:
        all_cargos_select_query = select(Cargo.id, Cargo.weight, Cargo.description)
        output_data_keys = ['id', 'weight', 'description']

        if weight:
            result = await session.execute(
                all_cargos_select_query.where(Cargo.weight == weight)
            )
        else:
            result = await session.execute(all_cargos_select_query)

        suitable_cargos = result.fetchall()
        normalize_suitable_cargos = []
        for row in suitable_cargos:
            cargo = {output_data_keys[key]: value for key, value in enumerate(row)}
            normalize_suitable_cargos.append(cargo)
        return normalize_suitable_cargos


@router.put("/car")
async def update_car(car: CarUpdate, session: AsyncSession = Depends(get_async_session)):
    location_id = await get_current_location(car.zip_code, session)
    update_query = update(Car).where(
        Car.id == car.id
    ).values(
        current_location=location_id
    )
    await session.execute(update_query)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "Статус выполнения запроса": "Локация машины успешно изменена"
        }
    )
