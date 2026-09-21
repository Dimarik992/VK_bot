from VKinder.db_model import Base, User, UserSearch, Candidate, UserSearchResult, UserInterest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from datetime import datetime
from typing import List, Dict, Optional, Any


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
Base.metadata.create_all(engine)


def get_user(vk_id: int) -> Optional[User]:
    """
    Функция возвращает информацию о пользователе по его vk_id.
    Если пользователь не найден — возвращает None.
    """
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.vk_id == vk_id).first()
        return user
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def save_user(vk_id: int, age: Optional[int] = None,
              gender: Optional[int] = None, city: Optional[str] = None) -> User:
    """
    Функция создает информацию о пользователе
    Если пользователь уже существует - то обновляет информацию о нем
    Допустимо обновлять отдельные атрибуты: age, gender, city
    """
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.vk_id == vk_id).first()
        if user:
            if age is not None:
                user.age = age
            if gender is not None:
                user.gender = gender
            if city is not None:
                user.city = city
        else:
            user = User(vk_id=vk_id, age=age, gender=gender, city=city)
            session.add(user)
        session.commit()
        return user
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def save_user_search(user_vk_id: int, age_from: int, age_to: int,
                     gender: int, city: str) -> UserSearch:
    """
    Функция сохраняет информацию о поиске пользователя в таблицу user_search
    """
    session = SessionLocal()
    try:
        search = UserSearch(
            user_vk_id=user_vk_id,
            age_from=age_from,
            age_to=age_to,
            gender=gender,
            city=city,
            search_date=datetime.now()
        )
        session.add(search)
        session.commit()
        session.refresh(search)
        return search
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def save_candidate(candidate_data: Dict[str, Any]) -> Candidate:
    """
    Функция обновляет информацию об одном кандидате по vk_id в таблице candidate
    Если такого vk_id еще нет, то создается новая запись
    Словарь по кандидату должен содержать поля: vk_id, profile_link, name, last_name и список photos
    """
    session = SessionLocal()
    try:
        candidate = session.query(Candidate).filter(Candidate.vk_id == candidate_data['vk_id']).first()
        if candidate:
            candidate.profile_link = candidate_data['profile_link']
            candidate.name = candidate_data['name']
            candidate.last_name = candidate_data['last_name']
            candidate.photos = candidate_data['photos']
        else:
            candidate = Candidate(
                vk_id=candidate_data['vk_id'],
                profile_link=candidate_data['profile_link'],
                name=candidate_data['name'],
                last_name=candidate_data['last_name'],
                photos=candidate_data['photos']
            )
            session.add(candidate)
        session.commit()
        return candidate
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def save_search_results(user_search_id: int,
                        candidates_data: List[Dict[str, Any]]) -> List[Candidate]:
    """
    Функция сохраняет результат поискового запроса
    На вход принимает id запроса и список словарей кандидатов
    Словарь должен содержать поля: vk_id, profile_link, name, last_name и список photos
    """
    session = SessionLocal()
    saved_candidates = []

    try:
        for item in candidates_data:
            vk_id = item.get("vk_id")
            if not vk_id:
                continue

            # Ищем кандидата по VK ID
            candidate = session.get(Candidate, vk_id)

            # Если кандидата нет — создаём
            if candidate is None:
                candidate = Candidate(vk_id=vk_id)
                session.add(candidate)
                session.flush()

            # Если кандидат уже был, информация перезаписывается.
            if "profile_link" in item:
                candidate.profile_link = item["profile_link"]
            if "name" in item:
                candidate.name = item["name"]
            if "last_name" in item:
                candidate.last_name = item["last_name"]
            if "photos" in item:
                candidate.photos = item["photos"]

            # Проверяем, не привязан ли уже этот кандидат к данному поиску
            link = (
                session.query(UserSearchResult)
                .filter_by(
                    user_search_id=user_search_id,
                    candidate_vk_id=vk_id
                )
                .first()
            )

            # Если связи нет — создаём
            if link is None:
                link = UserSearchResult(
                    user_search_id=user_search_id,
                    candidate_vk_id=vk_id
                )
                session.add(link)

            saved_candidates.append(candidate)

        session.commit()
        return saved_candidates

    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def mark_candidate_viewed(user_vk_id: int, candidate_vk_id: int,
                          is_liked: bool = False) -> UserInterest:
    """
    Функция добавляет информацию в таблицу user_interest
    Если запись по сочетанию user_vk_id и candidate_vk_id уже есть, то она обновляется
    Флаг is_viewed при вызове всегда ставится в True
    Флаг is_liked - функция принимает на вход
    """
    session = SessionLocal()
    try:
        interest = session.query(UserInterest).filter(
            UserInterest.user_vk_id == user_vk_id,
            UserInterest.candidate_vk_id == candidate_vk_id
        ).first()
        if interest:
            interest.is_viewed = True
            if is_liked:
                interest.is_liked = True
        else:
            interest = UserInterest(
                user_vk_id=user_vk_id,
                candidate_vk_id=candidate_vk_id,
                is_viewed=True,
                is_liked=is_liked
            )
            session.add(interest)
        session.commit()
        session.refresh(interest)
        return interest
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_new_candidates(user_vk_id: int, user_search_id: int):
    """
    Функция возвращает информацию о непросмотренных кандидатах для пользователя
    На вход принимает конкретный user_search_id и user_vk_id
    """
    session = SessionLocal()
    try:
        viewed_ids = session.query(UserInterest.candidate_vk_id).filter(
            UserInterest.user_vk_id == user_vk_id,
            (UserInterest.is_viewed == True) | (UserInterest.is_liked == True)
        ).scalar_subquery()

        return session.query(Candidate).join(
            UserSearchResult,
            Candidate.vk_id == UserSearchResult.candidate_vk_id
        ).filter(
            UserSearchResult.user_search_id == user_search_id,
            ~Candidate.vk_id.in_(viewed_ids)
        ).all()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_liked_candidates(user_vk_id: int) -> List[Candidate]:
    """
    Функция возвращает избранных кандидатов
    Для данного user_vk_id возвращаются все записи, где is_liked = True
    """
    session = SessionLocal()
    try:
        candidates = session.query(Candidate).join(
            UserInterest, Candidate.vk_id == UserInterest.candidate_vk_id
        ).filter(
            UserInterest.user_vk_id == user_vk_id,
            UserInterest.is_liked == True
        ).all()
        return candidates
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_user_search_history(user_vk_id: int) -> List[UserSearch]:
    """
    Функция возвращает список поисковых запросов пользователя
    """
    session = SessionLocal()
    try:
        searches = session.query(UserSearch).filter(
            UserSearch.user_vk_id == user_vk_id
        ).order_by(UserSearch.search_date.desc()).all()
        return searches
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_candidates_by_search(user_search_id: int) -> List[Candidate]:
    """
    Функция возвращает всех кандидатов, которые находятся в данном поисковом запросе
    """
    session = SessionLocal()
    try:
        candidates = session.query(Candidate).join(
            UserSearchResult, Candidate.vk_id == UserSearchResult.candidate_vk_id
        ).filter(UserSearchResult.user_search_id == user_search_id).all()
        return candidates
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

