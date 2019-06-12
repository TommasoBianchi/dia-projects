def prettify_super_arm(environment, super_arm):
    return str([(environment.get_subcampaign(subcampaign_id).get_classes_ids(), arm) for (subcampaign_id, arm) in super_arm])