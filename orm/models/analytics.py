from .base import Base
from geoalchemy2 import Geography
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, String, Text, Integer, Date, DateTime, ForeignKey


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
    inserted_at = Column(DateTime)
    updated_at = Column(DateTime)


class AnalyticsCampaignTasks(Base):
    __tablename__ = 'analytics_campaign_tasks'
    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('analytics_campaigns.id'))
    task_id = Column(Integer, ForeignKey('analytics_tasks.id'))
    inserted_at = Column(DateTime)
    updated_at = Column(DateTime)
    

class AnalyticsCampaignRider(Base):
    __tablename__='analytics_campaign_riders'
    id = Column(Integer, primary_key=True)
    capacity = Column(Integer)
    pickup_window = Column(String)
    campaign_id = Column(Integer)
    rider_id = Column(Integer, ForeignKey('analytics_riders.id'))
    inserted_at = Column(DateTime)
    updated_at = Column(DateTime)


class AnalyticsAddresses(Base):
    __tablename__='analytics_addresses'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    line1 = Column(String)
    line2 = Column(String)
    city = Column(String)
    province = Column(String)
    postal = Column(String)
    country = Column(String)
    geo = Column(Column(Geography(from_text='ST_GeogFromText'))
    inserted_at = Column(DateTime)
    updated_at = Column(DateTime)


class AnalyticsContacts(Base):
    __tablename__='analytics_contacts'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(Integer, ForeignKey('analytics_addresses.id'))
    inserted_at = Column(DateTime)
    updated_at = Column(DateTime)


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
