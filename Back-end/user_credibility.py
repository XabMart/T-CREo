from datetime import datetime, date

class UserCredibility:
    def __init__(self, twitter_creation_year=2006):
        self.twitter_creation_year = twitter_creation_year

    def verification(self, verified):
        if verified:
            result = 50
        else:
            result = 0
        return result

    def creation_weight(self, account_creation):
        creation = datetime.strptime(account_creation, '%Y-%m-%dT%H:%M:%S.000Z')
        current_year = date.today().year
        result = ((current_year - creation.date().year) / (current_year - self.twitter_creation_year)) * 50
        return result

    def user_credibility(self, verified, account_creation):
        verification_result = self.verification(verified)
        creation_weight_result = self.creation_weight(account_creation)
        return verification_result + creation_weight_result