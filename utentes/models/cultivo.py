# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, Numeric, Text
from sqlalchemy import ForeignKey, text

from geoalchemy2 import Geometry
from geoalchemy2.elements import WKTElement
from geoalchemy2.functions import GenericFunction

from utentes.lib.schema_validator.validator import Validator
from utentes.models.base import (
    Base,
    PGSQL_SCHEMA_UTENTES,
    update_geom
)
from actividades_schema import ActividadeSchema


class ActividadesCultivos(Base):
    __tablename__ = 'actividades_cultivos'
    __table_args__ = {u'schema': PGSQL_SCHEMA_UTENTES}

    gid = Column(Integer, primary_key=True, server_default=text("nextval('utentes.actividades_cultivos_gid_seq'::regclass)"))
    cult_id = Column(Text, nullable=False, unique=True)
    actividade = Column(ForeignKey(u'utentes.actividades_agricultura_rega.gid', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    c_estimado = Column(Numeric(10, 2), nullable=False)
    cultivo = Column(Text, nullable=False)
    rega = Column(Text, nullable=False)
    eficiencia = Column(Numeric(10, 2), nullable=False)
    area = Column(Numeric(10, 2), nullable=False)
    observacio = Column(Text)
    the_geom = Column(Geometry('MULTIPOLYGON', '32737'), index=True)

    @staticmethod
    def create_from_json(json):
        cultivo = ActividadesCultivos()
        cultivo.update_from_json(json)
        return cultivo

    def update_from_json(self, json):
        # actividade - handled by sqlalchemy relationship
        self.gid        = json.get('id')
        self.cult_id    = json.get('cult_id')
        self.c_estimado = json.get('c_estimado')
        self.cultivo    = json.get('cultivo')
        self.rega       = json.get('rega')
        self.eficiencia = json.get('eficiencia')
        self.area       = json.get('area')
        self.observacio = json.get('observacio')
        self.the_geom   = update_geom(self.the_geom, json)
        if self.the_geom is None:
            self.area = None
        else:
            self.area = self.the_geom.ST_Area() / 10000

    def __json__(self, request):
        the_geom = None
        if self.the_geom is not None:
            import json
            the_geom = json.loads(request.db.query(self.the_geom.ST_Transform(4326).ST_AsGeoJSON()).first()[0])

        return {
            'type': 'Feature',
            'properties': {
                'id':         self.gid,
                'cult_id':    self.cult_id,
                'actividade': self.actividade,
                'c_estimado': self.c_estimado,
                'cultivo':    self.cultivo,
                'rega':       self.rega,
                'eficiencia': self.eficiencia,
                'area':       self.area,
                'observacio': self.observacio,
            },
            'geometry': the_geom

        }

    def validate(self, json):
        validator = Validator(ActividadeSchema['Cultivos'])
        return validator.validate(json)
