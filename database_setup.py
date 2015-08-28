# Beginning configuration section
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
# Create a base class for our class code to inherit
Base = declarative_base()

# Class section
class Restaurant(Base):
    # Define the table called 'restaurant'
    __tablename__ = 'restaurant'

    # Define the column mappers
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)

    @property
    def serialize(self):
        # Returns object data in easily serializable format, i.e., JSON.
        return {
            'name' : self.name,
            'id' : self.id,
        }


class MenuItem(Base):
    # Define the table called 'menu_item'
    __tablename__ = 'menu_item'

    # Define the column mappers
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    # Create a variable representing a relationship with the Restaurant class
    # so that our foreign key will work
    restaurant = relationship(Restaurant)

    @property
    def serialize(self):
        # Returns object data in easily serializable format, i.e., JSON.
        return {
            'name' : self.name,
            'description' : self.description,
            'id' : self.id,
            'price' : self.price,
            'course' : self.course,
        }


# Ending configuration section
####### Insert at end of file #######
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)
