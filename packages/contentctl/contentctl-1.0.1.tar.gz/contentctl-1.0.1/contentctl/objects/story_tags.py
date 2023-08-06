

from pydantic import BaseModel, validator, ValidationError
from contentctl.objects.mitre_attack_enrichment import MitreAttackEnrichment


class StoryTags(BaseModel):
    # story spec
    name: str
    analytic_story: str
    category: list
    product: list
    usecase: str

    # enrichment
    mitre_attack_enrichments: list[MitreAttackEnrichment] = []
    mitre_attack_tactics: list = []
    datamodels: list = []
    kill_chain_phases: list = []


    @validator('product')
    def tags_product(cls, v, values):
        valid_products = [
            "Splunk Enterprise", "Splunk Enterprise Security", "Splunk Cloud",
            "Splunk Security Analytics for AWS", "Splunk Behavioral Analytics"
        ]

        for value in v:
            if value not in valid_products:
                raise ValueError('product is not valid for ' + values['name'] + '. valid products are ' + str(valid_products))
        return v