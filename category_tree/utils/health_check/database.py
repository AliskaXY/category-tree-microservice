from sqlalchemy import select, text


async def health_check_db(session) -> bool:
    try: 
        health_check_query = select(text("1"))
        result = await session.scalars(health_check_query)
    except OSError:
        return False
    return result is not None
