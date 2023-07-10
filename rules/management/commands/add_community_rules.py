from django.core.management.base import BaseCommand
from rules.models import Rule
from ips_server.settings import IPS_SERVER_SNORT_RULES_PATH
import os


class Command(BaseCommand):
    help = "Add all comunity rules"
    
    def handle(self, *args, **options):
        rules = [rule.name for rule in Rule.objects.all()]
        
        for dirpath,dnames,fnames in os.walk(IPS_SERVER_SNORT_RULES_PATH):
            for name in fnames:
                name = name.replace(".rules","")
                if name in rules:
                    pass
                else:
                    with open(IPS_SERVER_SNORT_RULES_PATH+f"{name}.rules") as rule_file:
                        code = rule_file.read()
                        new_rule = Rule(name=name,code=code,description=f'this is the predefined rules for {name}',is_verified=True,is_public=True)
                        new_rule.save()
                        rule_file.close()
                        