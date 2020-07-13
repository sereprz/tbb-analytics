from settings import TBB_DB
from orm.database import Database
from orm.models.dispatch import Campaigns, Riders
from orm.models.analytics import AnalyticsCampaigns, AnalyticsRiders, AnalyticsContacts, AnalyticsAddresses

from geoalchemy2 import functions
from datetime import datetime


def get_address_if_exists(db, table, line1, line2, city, province, postal, country):

    existing_address = db.session.query(table)\
        .filter(table.line1 == line1,
                table.line2 == line2,
                table.city == city,
                table.province == province,
                table.postal == postal,
                table.country == country)\
        .one_or_none()
    
    return existing_address if existing_address else None


db = Database(TBB_DB)

# Take campaigns turn them into analytics_campaigns

campaigns = db.get_latest(AnalyticsCampaigns, Campaigns)

for campaign in campaigns:
    existing_campaign = db.session.query(AnalyticsCampaigns).filter(AnalyticsCampaigns.id == campaign.id).first()
    
    if existing_campaign:
        existing_campaign.name = campaign.name
        existing_campaign = campaign.delivery_date
    else:
        db.session.add(
            AnalyticsCampaigns(campaign.id, campaign.name, campaign.delivery_date)
        )

db.commit_session()

print(f'Added {len(campaigns)} records to Analytics')

# get Riders and push info into AnalyticsContacts, AnalyticsRiders, AnalythicsAddress

riders = db.get_latest(AnalyticsRiders, Riders)

print(f'{len(riders)} new riders found')

added = 0
edited = 0

for rider in riders:
    existing_rider = db.session.query(AnalyticsRiders).filter(AnalyticsRiders.id == rider.id).one_or_none()

    if existing_rider:
        print(f'Editing rider {rider.id} in AnalyticsRiders')
        # modify contacts, address, riders
        existing_contact = db.session.query(AnalyticsContacts)\
            .filter(
                AnalyticsContacts.id == existing_rider.contact_id
            ).one()

        existing_contact.name = rider.name
        existing_contact.email = rider.email
        existing_contact.phone = rider.phone

        existing_address = get_address_if_exists(
            db, AnalyticsAddresses, rider.address, rider.address2, rider.city,
            rider.province, rider.postal, rider.country)
        
        if not existing_address:
            new_address = AnalyticsAddresses(
                rider.address, rider.address2, rider.city, rider.province,
                rider.postal, rider.country,
                functions.ST_GeogFromWKB(rider.location))
            
            db.session.add(new_address)
            db.commit_session()
            
            existing_contact.address = new_address.id
        
        existing_rider.onfleet_id = rider.onfleet_id
        existing_rider.onfleet_account_status = rider.onfleet_account_status
        existing_rider.pronouns = rider.pronouns
        existing_rider.availability = rider.availability
        existing_rider.capacity = rider.capacity
        existing_rider.max_distance = rider.max_distance
        existing_rider.mailchimp_id = rider.mailchimp_id
        existing_rider.mailchimp_status = rider.mailchimp_status
        existing_rider.contact_id = existing_rider.contact_id
        existing_rider.updated_at = datetime.now()

        edited += 1
    else:
        print(f'* Adding rider {rider.id} to AnalyticsRider')
        # Add new rider + contact (and address if not exists)
        existing_address = get_address_if_exists(
            db, AnalyticsAddresses, rider.address, rider.address2, rider.city,
            rider.province, rider.postal, rider.country)
        
        if existing_address:
            address_id = existing_address.id
        else:
            # add new address
            new_address = AnalyticsAddresses(
                rider.address, rider.address2, rider.city, rider.province,
                rider.postal, rider.country,
                functions.ST_GeogFromWKB(rider.location))
            
            db.session.add(new_address)
            db.commit_session()
            
            address_id = new_address.id
        
        # add new contact if not already existing
        existing_contact = db.session.query(AnalyticsContacts)\
            .filter(
                AnalyticsContacts.name == rider.name,
                AnalyticsContacts.email == rider.email,
                AnalyticsContacts.phone == rider.phone
            ).one_or_none()
        
        if existing_contact:
            contact_id = existing_contact.id
        else:
            new_contact = AnalyticsContacts(rider.name, rider.email, rider.phone, address_id)
            
            db.session.add(new_contact)
            db.commit_session()
            
            contact_id = new_contact.id
        
        # add rider

        db.session.add(
            AnalyticsRiders(
                rider.id, rider.onfleet_id, rider.onfleet_account_status,
                rider.pronouns, rider.availability, rider.capacity,
                rider.max_distance, rider.mailchimp_id, rider.mailchimp_status,
                contact_id
            )
        )
        added += 1

db.commit_session()
print(f'Processed {added + edited} riders, added {added}, edited {edited}')
db.close_session()
print('** Done')
