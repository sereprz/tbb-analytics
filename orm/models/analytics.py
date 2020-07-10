from .base import Base
from geoalchemy2 import Geography
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, String, Text, Integer, Date, DateTime, ForeignKey

from datetime import datetime


class AnalyticsTasks(Base):
    __tablename__ = 'analytics_tasks'
    id = Column(Integer, primary_key=True)
    rider_notes = Column(Text)
    submitted_on = Column(Date)
    organiation_name = Column(String)  # TODO: fix typo
    onfleet_pickup_id = Column(String)
    onfleet_dropoff_id = Column(String)
    request_type = Column(String)
    other_items = Column(String)
    size = Column(Integer)
    delivery_date = Column(Date)
    delivery_window = Column(String)
    delivery_distance = Column(Integer)
    rider_id = Column(Integer, ForeignKey('analytics_riders.id'))
    pickup_contact_id = Column(Integer, ForeignKey('analytics_contacts.id'))
    pickup_address = Column(Integer, ForeignKey('analytics_addresses.id'))
    dropoff_contact_id = Column(Integer, ForeignKey('analytics_contacts.id'))
    dropoff_address = Column(Integer, ForeignKey('analytics_addresses.id'))
    inserted_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __init__(self, rider_notes, submitted_on , organiation_name, onfleet_pickup_id, onfleet_dropoff_id, request_type, other_items, size, delivery_date, delivery_window, delivery_distance, rider_id, pickup_contact_id, pickup_address, dropoff_contact_id, dropoff_address):
    
        self.rider_notes = rider_notes
        self.submitted_on = submitted_on
        self.organiation_name = organiation_name
        self.onfleet_pickup_id = onfleet_pickup_id
        self.onfleet_dropoff_id = onfleet_dropoff_id
        self.request_type = request_type
        self.other_items = other_items
        self.size = size
        self.delivery_date = delivery_date
        self.delivery_window = delivery_window
        self.delivery_distance = delivery_distance
        self.rider_id = rider_notes
        self.pickup_contact_id = pickup_contact_id
        self.pickup_address = pickup_address
        self.dropoff_contact_id = dropoff_contact_id
        self.dropoff_address = dropoff_address
    

class AnalyticsRiders(Base):
    __tablename__ = 'analytics_riders'
    id = Column(Integer, primary_key=True)
    onfleet_id = Column(String)
    onfleet_account_status = Column(String)
    pronouns = Column(String)
    availability = Column(JSONB)  # TODO: check docs for JSONB
    capacity = Column(Integer)
    max_distance = Column(Integer)
    mailchimp_id = Column(String)
    mailchimp_status = Column(String)
    contact_id = Column(Integer, ForeignKey('analytics_contact.id'))
    signed_up_on = Column(Date)  # FIXME: missing in schema
    inserted_at = Column(DateTime)
    updated_at = Column(DateTime)


class AnalyticsCampaigns(Base):
    __tablename__ = 'analytics_campaigns'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    delivery_date = Column(Date)
    inserted_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, id, name, delivery_date):
        
        self.id = id
        self.name = name
        self.delivery_date = delivery_date


class AnalyticsCampaignTasks(Base):
    __tablename__ = 'analytics_campaign_tasks'
    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('analytics_campaigns.id'))
    task_id = Column(Integer, ForeignKey('analytics_tasks.id'))
    inserted_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __init__(self, campaign_id, task_id, inserted_at, updated_at):
        
        self.campaign_id = campaign_id
        self.task_id = task_id
    

class AnalyticsCampaignRider(Base):
    __tablename__='analytics_campaign_riders'
    id = Column(Integer, primary_key=True)
    capacity = Column(Integer)
    pickup_window = Column(String)
    campaign_id = Column(Integer)
    rider_id = Column(Integer, ForeignKey('analytics_riders.id'))
    inserted_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __init_(self, capacity , pickup_window, campaign_id, rider_id):
        
        self.capacity = capacity
        self.pickup_window = pickup_window
        self.campaign_id = campaign_id
        self.rider_id = rider_id

class AnalyticsAddresses(Base):
    __tablename__='analytics_addresses'
    id = Column(Integer, primary_key=True)
    line1 = Column(String)
    line2 = Column(String)
    city = Column(String)
    province = Column(String)
    postal = Column(String)
    country = Column(String)
    geo = Column(Geography(from_text='ST_GeogFromText'))
    inserted_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __init__(self, line1, city, province, postal, country, geo, line2=None):
        
        self.line1 = line1
        self.line2 = line2
        self.city = city
        self.province = province
        self.postal = postal
        self.country = country
        self.geo = geo


class AnalyticsContacts(Base):
    __tablename__='analytics_contacts'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(Integer, ForeignKey('analytics_addresses.id'))
    inserted_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __init__(self, name, email, phone, address):
        
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address

class AnalyticsCampaignSummaries(Base):
    __tablename__='analytics_campaign_summaries'
    id = Column(Integer, primary_key=True)
    delivery_window = Column(String)
    tasks_count = Column(Integer)
    riders_count = Column(Integer)
    distance_covered = Column(Integer)
    failed_count = Column(Integer)
    campaign_id = Column(Integer, ForeignKey('analytics_campaigns.id'))
    inserted_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __init__(self, delivery_window, tasks_count, riders_count, distance_covered, failed_count, campaign_id):
        
        self.delivery_window = delivery_window
        self.tasks_count = tasks_count
        self.riders_count = riders_count
        self.distance_covered = distance_covered
        self.failed_count = failed_count
        self.campaign_id = campaign_id
