import strawberry


@strawberry.type
class Query:
    @strawberry.field
    async def getMusicList(self) -> str:
        return "123"
