import json

from asyncio import TimeoutError
from datetime import datetime, timedelta
from aiohttp import ClientSession, ClientTimeout, ClientResponse
from loguru import logger

from intellect_core.dto.dto import IntellectConfigDto, \
    CoreCommand, \
    ObjectType, \
    IntellectVisitDto, \
    AutarizationInfo, \
    IntellectDepartmentDto
from intellect_core.handler import IntellectError, ErrorClass, ErrorSubClass


class IntellectWebServer:
    log_debug: bool = False
    config: IntellectConfigDto
    autarization_info: AutarizationInfo
    expire_token_date: str

    # =====================================================================================================================

    async def _wrap_response(self, response: ClientResponse):
        await response.read()
        if (await response.json()).get("Status") == "ERROR":
            logger.error(await response.json())
        if self.log_debug:
            logger.debug(
                f"\nresponse_body: {bytes(await response.read()).decode()}\nresponse: {response}")

    def _get_url(self, object_type: ObjectType, command: CoreCommand,
                 dto: IntellectVisitDto.Create | IntellectVisitDto.Update | None, objid: int | None) -> str:
        url = f"http://{self.config.intellect_host}:{self.config.intellect_port}/intellect_core/Event?command={command.value}objtype{object_type.value},"
        if dto:
            for key, value in dto.dict().items():
                if value:
                    url = url + f"{key}<{value}>,"
                logger.debug(f"{key}, {value}")

            return url[0:-1]
        else:
            url = url + f"objid<{objid}>"
            return url

    # =====================================================================================================================
    async def autorization(self):
        timeout = ClientTimeout(total=5)
        async with ClientSession(timeout=timeout) as session:
            url = f"http://{self.config.host_user}:{self.config.host_password}@{self.config.intellect_host}:{self.config.intellect_port}/token?expires_in={self.config.token_expires}"
            logger.debug(url)
            try:
                async with session.request(method="GET", url=url) as response:
                    string = "{" + (await response.text()).replace("\n", ",")[2:-2] + "}"
                    self.autarization_info = AutarizationInfo(**json.loads(string))
                    self.expire_token_date = datetime.now() + timedelta(seconds=self.autarization_info.expires_in)
                    if self.log_debug:
                        logger.debug(f"\nresponse_body: {bytes(await response.read()).decode()}\nresponse: {response}")
            except TimeoutError as e:
                logger.error(f"Intellect connection error timeout: {e}")

    # =====================================================================================================================
    async def init(self, intellect_config: IntellectConfigDto):
        self.config = intellect_config

    async def logic(self, object_type: ObjectType,
                    command: CoreCommand,
                    dto: IntellectVisitDto.Create |
                         IntellectVisitDto.Update |
                         IntellectDepartmentDto.Create |
                         IntellectDepartmentDto.Update = None,
                    objid: int = None) -> None:
        session = ClientSession()
        match command:
            case CoreCommand.CREATE | CoreCommand.UPDATE:
                if dto:
                    dto.level_id = self.config.access_level
                    url = self._get_url(object_type, command, dto, None)
                    try:
                        async with session.request(method="GET", url=url) as response:
                            await self._wrap_response(response)
                            await session.close()
                    except OSError as e:
                        await session.close()
                        logger.error(f"Intellect connection error: {e}")
                else:
                    await session.close()
                    raise IntellectError(message="You need set dto for update or create object",
                                         context={"class": ErrorClass.CREATE_OR_UPDATE,
                                                  "subclass": ErrorSubClass.DTO_NOT_FOUND})
            case CoreCommand.DELETE:
                if objid:
                    url = self._get_url(object_type, command, None, objid)
                    try:
                        async with session.request(method="GET",
                                                   url=url) as response:
                            await self._wrap_response(response)
                            await session.close()
                    except OSError as e:
                        await session.close()
                        logger.error(f"Intellect connection error: {e}")
                else:
                    await session.close()
                    raise IntellectError(message="You need set object id for delete object",
                                         context={"class": ErrorClass.DELETE,
                                                  "subclass": ErrorSubClass.OBJECT_ID_NOT_FOUND})
