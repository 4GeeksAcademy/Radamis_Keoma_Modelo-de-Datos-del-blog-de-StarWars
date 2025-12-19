from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Date, Time, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre_usuario: Mapped[str] = mapped_column( String(50), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(nullable=False)
    apellido: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)

    favoritos_personaje: Mapped[list["FavoritoPersonaje"]] = relationship(back_populates="user",cascade="all, delete-orphan")
    favoritos_pelicula: Mapped[list["FavoritoPelicula"]] = relationship(back_populates="user",cascade="all, delete-orphan")


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "nombre_usuario": self.nombre_usuario,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }


class Personaje(db.Model):
    __tablename__ = "personaje"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(nullable=False)
    apellido: Mapped[str] = mapped_column(nullable=False)
    planeta: Mapped[str] = mapped_column(String(500), nullable=True)
    bueno: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)

    pelicula: Mapped[str] = mapped_column(ForeignKey("Pelicula.id"), nullable=False)
    favorito_by: Mapped[list["FavoritoPersonaje"]] = relationship( back_populates="personaje", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "planeta": self.planeta,
            "bueno": self.bueno,
        }


class Pelicula(db.Model):
    __tablename__ = "pelicula"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(nullable=False)
    fecha_producion: Mapped[Date] = mapped_column(Date, nullable=False)
    compañia_de_produccion: Mapped[str] = mapped_column(nullable=False)
    duracion: Mapped[Time] = mapped_column(Time, nullable=False)

    director: Mapped[str] = mapped_column(ForeignKey("Director.nombre"), nullable=False)
    favorito_by: Mapped[list["FavoritoPelicula"]] = relationship(back_populates="Pelicula", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "fecha_producion": self.fecha_producion,
            "compañia_de_produccion": self.compañia_de_produccion,
            "duracion": self.duracion,
            "director": self.director
        }


class Director(db.Model):
    __tablename__ = "director"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(nullable=False)
    apellido: Mapped[str] = mapped_column(nullable=False)
    fecha_nacimiento: Mapped[Date] = mapped_column(Date, nullable=False)
    lugar_de_nacimiento: Mapped[str] = mapped_column(nullable=True)
    historia_de_vida: Mapped[str] = mapped_column(String(500), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fecha_nacimiento": self.fecha_nacimiento,
            "lugar_de_nacimiento": self.lugar_de_nacimiento,
            "historia_de_vida": self.historia_de_vida
        }


class FavoritoPersonaje(db.Model):
    __tablename__ = "favorito_personaje"
    __table_args__ = (UniqueConstraint("User_id", "Personaje_id", name="uq_User_Personaje"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    personaje_id: Mapped[int] = mapped_column(ForeignKey("personaje.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="favoritos")
    personaje: Mapped["Personaje"] = relationship(back_populates="favorito_by")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "personaje_id": self.personaje_id
        }


class FavoritoPelicula(db.Model):
    __tablename__ = "favorito_pelicula"
    __table_args__ = (UniqueConstraint("User_id", "Pelicula_id", name="uq_User_Pelicula"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    pelicula_id: Mapped[int] = mapped_column(ForeignKey("pelicula.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="favoritos")
    pelicula: Mapped["Pelicula"] = relationship(back_populates="favorito_by")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "pelicula_id": self.pelicula_id
        }
