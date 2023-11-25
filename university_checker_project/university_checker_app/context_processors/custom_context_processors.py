
from university_checker_app.models import Profile  # Import your Profile model

def university_link(request):
    # Get the path of the request
    path_components = request.path.split('/')

    # Check if the path contains "overview,"or "comparison
    if 'overview' in path_components:
        index = path_components.index('overview')
    elif 'comparison' in path_components:
        index = path_components.index('comparison')
    else:
        # If none of the keywords are found, set index to -1
        index = -1

    # Extract everything coming after the keyword (if found)
    if index != -1 and index + 1 < len(path_components):
        university_link = path_components[index + 1]
    else:
        university_link = None

    # Get the user's profile picture
    user_profile_pic = None
    if request.user.is_authenticated:
        try:
            user_profile = Profile.objects.get(user=request.user)
            user_profile_pic = user_profile.profile_pic.url if user_profile.profile_pic else None
        except Profile.DoesNotExist:
            pass

    # Return a dictionary with the variables url and profile pic
    return {'university_link': university_link, 'user_profile_pic': user_profile_pic}
