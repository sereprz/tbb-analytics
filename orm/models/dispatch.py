from .base import Base
from geoalchemy2 import Geography
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, String, Text, Integer, DateTime, Date, ForeignKey


class Riders(Base):
    __tablename__ = 'riders'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    address = Column(String)
    address2 = Column(String)
    city = Column(String)
    province = Column(String)
    postal = Column(String)
    country = Column(String)
    phone = Column(String)
    pronouns = Column(String)
    availability = Column(JSONB)
    capacity = Column(Integer)
    max_distance = Column(Integer)
    signed_up_on = Column(Date)
    inserted_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    onfleet_id = Column(String)
    onfleet_account_status = Column(String)
    deliveries_completed = Column(Integer)
    location = Column(Geography(from_text='ST_GeogFromText'))
    mailchimp_id = Column(String)
    mailchimp_status = Column(String)


class CampaignsTasks(Base):
    __tablename__ = 'campaigns_tasks'
    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))
    task_id = Column(Integer, ForeignKey('tasks.id'))
    inserted_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Campaigns(Base):
    __tablename__ = 'campaigns'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    inserted_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    instructions_template_id = Column(Integer, ForeignKey('message_templates.id'))
    welcome_template_id = Column(Integer, ForeignKey('message_templates.id'))
    welcome_template = Column(Integer)
    rider_spreadsheet_id = Column(Integer, ForeignKey('spreadsheets.id'))
    delivery_date = Column(Date)
    pickup_address = Column(String)
    pickup_address2 = Column(String)
    pickup_city = Column(String)
    pickup_province = Column(String)
    pickup_postal = Column(String)
    pickup_country = Column(String)
    pickup_location = Column(Geography(from_text='ST_GeogFromText'))


class CampaignsRiders(Base):
    __tablename__ = 'campaigns_riders'
    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))
    rider_id = Column(Integer, ForeignKey('riders.id'))
    rider_capacity = Column(Integer)
    inserted_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    notes = Column(Text)
    pickup_window = Column(String)


class Tasks(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    submitted_on = Column(DateTime)
    organization_name = Column(String)
    contact_name = Column(String)
    contact_email = Column(String)
    contact_phone = Column(String)
    request_type = Column(String)
    other_items = Column(String)
    size = Column(Integer)
    delivery_date = Column(Date)
    delivery_window = Column(String)
    dropoff_organization = Column(String)
    dropoff_name = Column(String)
    dropoff_email = Column(String)
    dropoff_address = Column(String)
    dropoff_address2 = Column(String)
    dropoff_city = Column(String)
    dropoff_province = Column(String)
    dropoff_postal = Column(String)
    dropoff_location = Column(Geography(from_text='ST_GeogFromText'))
    rider_notes = Column(String)  # TODO: tell Max this is NOT Text
    logistics_notes = Column(String)
    pickup_address = Column(String)
    pickup_address2 = Column(String)
    pickup_city = Column(String)
    pickup_province = Column(String)
    pickup_postal = Column(String)
    pickup_country = Column(String)
    pickup_location = Column(Geography(from_text='ST_GeogFromText'))
    inserted_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    onfleet_pickup_id = Column(String)
    onfleet_dropoff_id = Column(String)
    delivery_distance = Column(Integer)
    dropoff_phone = Column(String)
    assigned_rider_id = Column(Integer, ForeignKey('riders.id'))
