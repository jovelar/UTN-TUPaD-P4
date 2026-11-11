from sqlmodel import Session, select
from app.core.database import engine
from app.modules.unidades_medida.model import UnidadMedida, TipoUnidadMedida


def seed_unidades_medida():
    with Session(engine) as session:
        # Solo inserta si la tabla está vacía
        if session.exec(select(UnidadMedida)).first():
            return
        unidades = [
            UnidadMedida(nombre="kilogramo", simbolo="kg", tipo=TipoUnidadMedida.peso),
            UnidadMedida(nombre="gramo", simbolo="g", tipo=TipoUnidadMedida.peso),
            UnidadMedida(nombre="litro", simbolo="L", tipo=TipoUnidadMedida.volumen),
            UnidadMedida(nombre="mililitro", simbolo="mL", tipo=TipoUnidadMedida.volumen),
            UnidadMedida(nombre="pieza", simbolo="u", tipo=TipoUnidadMedida.contable),
            UnidadMedida(nombre="docena", simbolo="doc", tipo=TipoUnidadMedida.contable),
        ]
        session.add_all(unidades)
        session.commit()