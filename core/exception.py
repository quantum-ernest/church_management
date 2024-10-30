from fastapi import HTTPException, status
from sqlalchemy.orm import Session


class AppValidationException:
    def __init__(self, session: Session, mapper_pk_ids: dict):
        """

        :param mapper_pk_ids: dict of the mapper class and the primary pk_id id
        :raise: raises and exception raised when a validation fails
        """
        self.mapper_pk_ids = mapper_pk_ids
        self.session = session


class NotFound(AppValidationException):
    def __call__(self):
        for mapper, pk_ids in self.mapper_pk_ids.items():
            for pk_id in pk_ids:
                result = mapper.check_if_id_exists(self.session, pk_id)
                if not result:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail=f'Object {mapper.__name__}: with ID {pk_id} not found')


class AlreadyExists(AppValidationException):
    def __call__(self):
        for mapper, pk_ids in self.mapper_pk_ids.items():
            for pk_id in pk_ids:
                result = mapper.check_if_id_exists(self.session, pk_id)
                if result:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail=f'Object {mapper}: with ID {pk_id} already exists')
