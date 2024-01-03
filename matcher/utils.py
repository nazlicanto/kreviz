# matcher/utils.py

from account.models import Account
from django.db.models import Count

def find_matches_for_user(user):
    user_interests = user.interests.all()
    potential_matches = Account.objects.filter(
        interests__in=user_interests
    ).exclude(
        id=user.id
    ).annotate(
        shared_interests_count=Count('interests')
    ).order_by('-shared_interests_count')

    matches_with_shared_interests = []
    for match in potential_matches:
        shared_interests = match.interests.filter(id__in=user_interests)
        if shared_interests.exists():
            matches_with_shared_interests.append({
                'user': match,
                'shared_interests': shared_interests,
                'score': match.shared_interests_count
            })

    return matches_with_shared_interests
