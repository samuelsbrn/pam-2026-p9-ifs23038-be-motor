from app.extensions import SessionLocal
from app.models.motor import Motor
from app.services.llm_service import generate_from_llm
from app.utils.parser import parse_motor_response


def create_motors(total: int, genre: str | None = None):
    session = SessionLocal()

    try:
        requested_genre = (genre or "").strip()
        genre_instruction = (
            f'Semua motor harus konsisten dengan genre "{requested_genre}". '
            f'Field "genre" untuk setiap item harus diisi "{requested_genre}" atau variasi penulisan yang masih setara.'
            if requested_genre
            else "Setiap motor harus memiliki genre yang bervariasi."
        )

        prompt = f"""
        Dalam format JSON, buat {total} rekomendasi motor yang saat ini sering dibicarakan.
        {genre_instruction}
        Semua motor harus relevan dengan motor modern dan tidak boleh duplikat.
        Format:
        {{
            "motors": [
                {{
                    "title": "...",
                    "genre": "...",
                    "description": "...",
                    "popularity_reason": "..."
                }}
            ]
        }}
        """

        result = generate_from_llm(prompt)
        motors = parse_motor_response(result)

        saved = []

        for item in motors:
            generated_genre = item.get("genre", "").strip()
            final_genre = requested_genre or generated_genre

            motor = Motor(
                title=item.get("title", "").strip(),
                genre=final_genre,
                description=item.get("description", "").strip(),
                popularity_reason=item.get("popularity_reason", "").strip(),
            )
            session.add(motor)
            session.flush()
            saved.append(
                {
                    "title": motor.title,
                    "genre": motor.genre,
                    "description": motor.description,
                    "popularity_reason": motor.popularity_reason,
                    "created_at": motor.created_at.isoformat(),
                }
            )

        session.commit()

        return saved

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()


def get_all_motors(page: int = 1, per_page: int = 100):
    session = SessionLocal()

    try:
        query = session.query(Motor)
        total = query.count()
        data = (
            query
            .order_by(Motor.id.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

        return {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": (total + per_page - 1) // per_page,
            "data": [
                {
                    "id": motor.id,
                    "title": motor.title,
                    "genre": motor.genre,
                    "description": motor.description,
                    "popularity_reason": motor.popularity_reason,
                    "created_at": motor.created_at.isoformat(),
                }
                for motor in data
            ],
        }

    finally:
        session.close()
