from typing import Any, Optional
from rules.models import Rule
from ips_server.settings import IPS_SERVER_SNORT_RULES_PATH
from django.core.management.base import BaseCommand
import os 

class Command(BaseCommand):
    help = "backup and write all rules from database to rules path"
    
    def handle(self, *args: Any, **options: Any):
        dir_exists=os.path.exists(IPS_SERVER_SNORT_RULES_PATH)
        if dir_exists:
            pass
        else:
            os.mkdir(IPS_SERVER_SNORT_RULES_PATH)
        db_rules = Rule.objects.all()
        written_rules = []
        for dirpath,dnames,fname in os.walk(IPS_SERVER_SNORT_RULES_PATH):
            written_rules.append(str(fname).replace('.rules',""))
        for rule in db_rules:
            rule_name = rule.name
            rule_name = rule_name.replace("/",'-')
            rule_name = rule_name.replace(" ",'-')
            if rule_name not in written_rules:
                with open(IPS_SERVER_SNORT_RULES_PATH+f"{rule_name}.rules",'+w') as new_rule:
                    new_rule.write(rule.code)
                    new_rule.close()
            else:
                pass
        