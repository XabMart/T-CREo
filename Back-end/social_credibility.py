
def followersImpact(followers_count,friends_count):
    max_followers = 2000000
    result = (min(followers_count, max_followers) / max_followers) * 50
    return result

    
def followerProportion(followers_count,friends_count):
    result = (followers_count / (followers_count + friends_count)) * 50
    return result
    
def socialCredibility(followers_count,friends_count):
    socialCredibility = followersImpact(followers_count,friends_count) + followerProportion(followers_count,friends_count)
    return socialCredibility
