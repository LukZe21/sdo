import numpy as np

def search_engine(query, users, groups):
    query = query.split(" ")
    users_scores = {}
    groups_scores = {}
    for user in users:
        user_score = 0
        for word in query:
            if word in user.unique_id:
                user_score += 1
                break
            elif word in user.firstname:
                user_score += 1
            elif word in user.lastname:
                user_score += 1
            elif word in user.nickname:
                user_score += 1
        if user_score >= 1:
            users_scores[user] = user_score


    for group in groups:
        group_score = 0
        for word in query:
            if word in group.name:
                group_score += 1
        if group_score >= 1:
            groups_scores[group] = group_score
    
    users, groups = [user for user in dict(sorted(users_scores.items(), key=lambda item: item[1])).keys()], [user for user in dict(sorted(groups_scores.items(), key=lambda item: item[1])).keys()]
    return users, groups
            