from settings import TBB_DB
from orm.database import Database
from orm.models.dispatch import Campaigns
from orm.models.analytics import AnalyticsCampaigns

from sqlalchemy.sql.expression import func

db = Database(TBB_DB)

# Take campaigns turn them into analytics_campaigns

latest = db.session.query(func.max(AnalyticsCampaigns.updated_at)).first()[0]
if latest:
    campaigns = db.session.query(Campaigns).filter(Campaigns.updated_at > latest).all()
else:
    campaigns = db.session.query(Campaigns).all()

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
