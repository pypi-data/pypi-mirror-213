"""
City repository with database CRUD operations
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Peter Yefi peteryefi@gmail.com
"""
import datetime
import logging

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from hub.city_model_structure.city import City as CityHub
from hub.persistence.repository import Repository
from hub.persistence.models import City as Model
from hub.persistence.models import CityObject
from hub.version import __version__


class City(Repository):
  """
  City repository
  """
  _instance = None

  def __init__(self, db_name: str, dotenv_path: str, app_env: str):
    super().__init__(db_name, dotenv_path, app_env)

  def __new__(cls, db_name, dotenv_path, app_env):
    """
    Implemented for a singleton pattern
    """
    if cls._instance is None:
      cls._instance = super(City, cls).__new__(cls)
    return cls._instance

  def insert(self, city: CityHub, pickle_path, application_id, user_id: int):
    """
    Inserts a city
    :param city: The complete city instance
    :param pickle_path: Path to the pickle
    :param application_id: Application id owning the instance
    :param user_id: User id owning the instance
    :return: Identity id
    """
    city.save_compressed(pickle_path)
    try:
      db_city = Model(
        pickle_path,
        city.name,
        city.level_of_detail.geometry,
        'None' if city.climate_file is None else str(city.climate_file),
        application_id,
        user_id,
        __version__)

      self.session.add(db_city)
      self.session.flush()
      self.session.commit()
      for building in city.buildings:
        db_city_object = CityObject(db_city.id,
                                    building)
        self.session.add(db_city_object)
        self.session.flush()
      self.session.commit()
      self.session.refresh(db_city)
      return db_city.id
    except SQLAlchemyError as err:
      logging.error('An error occurred while creating a city %s', err)
      raise SQLAlchemyError from err

  def update(self, city_id: int, city: CityHub):
    """
    Updates a city name (other updates makes no sense)
    :param city_id: the id of the city to be updated
    :param city: the city object
    :return: None
    """
    try:
      now = datetime.datetime.utcnow()
      self.session.query(Model).filter(Model.id == city_id).update({'name': city.name, 'updated': now})
      self.session.commit()
    except SQLAlchemyError as err:
      logging.error('Error while updating city %s', err)
      raise SQLAlchemyError from err

  def delete(self, city_id: int):
    """
    Deletes a City with the id
    :param city_id: the city id
    :return: None
    """
    try:
      self.session.query(CityObject).filter(CityObject.city_id == city_id).delete()
      self.session.query(Model).filter(Model.id == city_id).delete()
      self.session.commit()
    except SQLAlchemyError as err:
      logging.error('Error while fetching city %s', err)
      raise SQLAlchemyError from err

  def get_by_user_id_application_id_and_name(self, user_id, application_id, city_name) -> Model:
    """
    Fetch city based on the user who created it
    :param user_id: the user id
    :param application_id: the application id
    :param city_name: the city name
    :return: ModelCity
    """
    try:
      result_set = self.session.execute(select(Model).where(Model.user_id == user_id,
                                                            Model.application_id == application_id,
                                                            Model.name == city_name
                                                            )).first()
      if result_set is not None:
        result_set = result_set[0]
      return result_set
    except SQLAlchemyError as err:
      logging.error('Error while fetching city by name %s', err)
      raise SQLAlchemyError from err

  def get_by_user_id_and_application_id(self, user_id, application_id) -> [Model]:
    """
    Fetch city based on the user who created it
    :param user_id: the user id
    :param application_id: the application id
    :return: ModelCity
    """
    try:
      result_set = self.session.execute(
        select(Model).where(Model.user_id == user_id, Model.application_id == application_id)
      )
      return [r[0] for r in result_set]
    except SQLAlchemyError as err:
      logging.error('Error while fetching city by name %s', err)
      raise SQLAlchemyError from err
