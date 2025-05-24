# ruff: noqa: F401, I001

# Сервисы администраторов
from .administrator.administrator_cancel import AdministratorCancelService
from .administrator.administrator_with_user_create import (
    AdministratorWithUserCreateService,
)

# Сервисы спортсменов
from .athlete.athlete_cancel import AthleteCancelService

# Сервисы тренеров
from .coach.coach_cancel import CoachCancelService

# Сервисы пользователей
from .user.user_appoint_administrator import UserAppointAdministratorService
from .user.user_appoint_athlete import UserAppointAthleteService
from .user.user_appoint_coach import UserAppointCoachService
