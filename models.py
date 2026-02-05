from datetime import datetime

from sqlalchemy import Column, String, Integer, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Movies(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable = False)
    type = Column(String(200), nullable = False)
    year = Column(Integer, nullable = True)
    finished = Column(Boolean, nullable = False)
    points = Column(Integer, nullable = False)
    attempts = Column(Text, nullable = False)
    hints = Column(Text, nullable = False)
    image_file = Column(String(200), nullable = True, default='default.jpg')

    def get_hints(self):
        return self.hints.split('|') if self.hints else []

    def add_hints(self, hints):
        if self.hints:
            self.hints += f"|{hints}"
        else:
            self.hints = hints

    def get_attempts(self):
        return self.attempts.split('|') if self.attempts else []

    def add_attempts(self, attempts):
        if self.attempts:
            self.attempts += f"|{attempts}"
        else:
            self.attempts = attempts

class Songs(Base):
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable = False)
    type = Column(String(200), nullable = False)
    year = Column(Integer, nullable = True)
    finished = Column(Boolean, nullable = False)
    points = Column(Integer, nullable = False)
    attempts = Column(Text, nullable = False)
    hints = Column(Text, nullable = False)

    def get_hints(self):
        return self.hints.split('|') if self.hints else []

    def add_hints(self, hints):
        if self.hints:
            self.hints += f"|{hints}"
        else:
            self.hints = hints

    def get_attempts(self):
        return self.attempts.split('|') if self.attempts else []

    def add_attempts(self, attempts):
        if self.attempts:
            self.attempts += f"|{attempts}"
        else:
            self.attempts = attempts