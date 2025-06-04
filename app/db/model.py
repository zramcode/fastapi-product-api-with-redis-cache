from sqlalchemy.orm import mapped_column, Mapped
from app.db.database import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name:Mapped[str] = mapped_column(nullable= False, index=True)
    description:Mapped[str] = mapped_column(nullable=True)
    serialnumber :Mapped[str] = mapped_column(nullable= False, index= True, unique= True)
    price: Mapped[float] = mapped_column(nullable= False, default= 0)
    