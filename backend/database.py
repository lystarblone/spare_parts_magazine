from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
from .models import Base, Equipment, Part, Workshop, ReplacementType

logger = logging.getLogger(__name__)

DATABASE_URL = 'sqlite:///./spare_parts.db'

engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info('Database tables created successfully')

        db = SessionLocal()
        try:
            if db.query(Equipment).count() == 0:
                equipments = [
                    Equipment(name='Грузовик A', fleet_quantity=15),
                    Equipment(name='Экскаватор B', fleet_quantity=8),
                    Equipment(name='Погрузчик C', fleet_quantity=12),
                    Equipment(name='Кран D', fleet_quantity=5),
                    Equipment(name='Бульдозер E', fleet_quantity=10),
                ]
                db.add_all(equipments)
                db.commit()
                logger.info('Initialized 5 equipment records')

            if db.query(Part).count() == 0:
                equipments = db.query(Equipment).all()
                parts = []
                for eq in equipments:
                    for i in range(1, 6):
                        parts.append(Part(
                            name=f'Запчасть {i} для {eq.name}',
                            useful_life=365 * i,
                            equipment_id=eq.id,
                            quantity_per_equipment=2 + i % 3,
                            stock_quantity=10 + i,
                            procurement_time=7 + i * 3
                        ))
                db.add_all(parts)
                db.commit()
                logger.info(f'Initialized {len(parts)} part records')

            if db.query(Workshop).count() == 0:
                workshops = [
                    Workshop(name='Центральный Гараж', address='Москва, ул. Ленина, 1'),
                    Workshop(name='Северный Ремонт', address='Санкт-Петербург, Невский пр., 2'),
                    Workshop(name='Южная Мастерская', address='Краснодар, ул. Мира, 3'),
                    Workshop(name='Восточный Сервис', address='Владивосток, ул. Океанская, 4'),
                    Workshop(name='Западный Депо', address='Калининград, ул. Канта, 5'),
                ]
                db.add_all(workshops)
                db.commit()
                logger.info('Initialized 5 workshop records')

            if db.query(ReplacementType).count() == 0:
                types = [
                    ReplacementType(name='ремонт'),
                    ReplacementType(name='плановая замена'),
                    ReplacementType(name='внеплановая замена'),
                    ReplacementType(name='профилактика'),
                    ReplacementType(name='модернизация'),
                ]
                db.add_all(types)
                db.commit()
                logger.info('Initialized 5 replacement type records')

        except Exception:
            db.rollback()
            logger.exception('Failed to initialize database with default data')
            raise
        finally:
            db.close()
    except Exception:
        logger.exception('Failed to create database tables')
        raise