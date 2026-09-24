from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.core.config import get_settings

settings = get_settings()

# Supabase's connection pooler (PgBouncer on port 6543) runs in
# *transaction* mode, which does not support protocol-level prepared
# statements.  Setting prepared_statement_cache_size=0 tells asyncpg
# to use the simple query protocol instead.
_is_supabase = "supabase" in settings.DATABASE_URL

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    # asyncpg-specific: disable prepared-statement cache when going
    # through Supabase's PgBouncer (transaction-mode pooling)
    connect_args={"prepared_statement_cache_size": 0} if _is_supabase else {},
)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    """Dependency that provides a database session."""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Create all tables on startup."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
