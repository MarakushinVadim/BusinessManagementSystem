from fastapi import APIRouter, Depends, status, Request

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.config import templates
from app.database import get_async_session
from app.models import UserModel, TeamModel
from app.services import check_admin
from app.auth.auth import current_active_user

router = APIRouter(prefix="/team", tags=["team"])

@router.get("/", response_model=schemas.TeamRead, status_code=status.HTTP_200_OK)
async def get_team(
        request: Request,
        user: UserModel = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session)
):
    if user.role == "admin":
        query = select(TeamModel).where(TeamModel.admin_id == user.id).options(selectinload(TeamModel.users))
    else:
        query = select(TeamModel).where(TeamModel.id == user.team_id).options(selectinload(TeamModel.users))

    response = (await session.scalars(query)).first()

    accept_header = request.headers.get("accept", "")

    return response


@router.post("/", response_model=schemas.TeamRead, status_code=status.HTTP_201_CREATED)
async def create_team(
    users: schemas.TeamCreate,
    request: Request,
    user: UserModel = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    await check_admin(user)

    team_data = users.model_dump()

    users_list = (
        await session.scalars(
            select(UserModel).where(UserModel.id.in_(team_data["users"]))
        )
    ).all()
    team_data["users"] = users_list

    team_db = TeamModel(**team_data, admin_id=user.id)
    session.add(team_db)
    await session.commit()

    accept_header = request.headers.get("accept", "")
    if "text/html" in accept_header:
        return templates.TemplateResponse(
            request=request,
            name="teams.html",
            context={"team_data": team_db, "user": user},
        )

    return team_db

# @router.get("/")
# async def get_my_team(
#         user: UserModel = Depends()
# )
