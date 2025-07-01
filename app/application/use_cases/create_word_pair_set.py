from app.extensions import db
from app.application.dtos.word_pair_set import CreateWordPairSetDto, WordPairSetDto
from app.infrastructure.db.models.word_pairs import WordPairSetModel

class CreateWordPairSetUseCase:
    def __init__(self) -> None:
        self._db = db

    def execute(self, dto: CreateWordPairSetDto) -> WordPairSetDto:
        model = WordPairSetModel(
            name=dto.name,
            comment=dto.comment,
            owner_id=dto.owner_id,
            parent_folder_id=dto.parent_folder_id
        )
        self._db.session.add(model)
        self._db.session.commit()
        return WordPairSetDto(
            id=model.id,
            name=model.name,
            comment=model.comment,
            parent_folder_id=model.parent_folder_id,
            owner_id=model.owner_id,
            created_at=model.created_at
        )
