# university_checker_app/context_processors/custom_context_processors.py

def university_link(request):
    # Get the path of the request
    path_components = request.path.split('/')

    # Check if the path contains "overview," "comparison," or "ranking"
    if 'overview' in path_components:
        index = path_components.index('overview')
    elif 'comparison' in path_components:
        index = path_components.index('comparison')
    elif 'ranking' in path_components:
        index = path_components.index('ranking')
    else:
        # If none of the keywords are found, set index to -1
        index = -1

    # Extract everything coming after the keyword (if found)
    if index != -1 and index + 1 < len(path_components):
        university_link = path_components[index + 1]
    else:
        university_link = None

    # Print for debugging
    print("Request Path:", request.path)
    print("University Link:", university_link)

    # Return a dictionary with the variable you want to make available in templates
    return {'university_link': university_link}


# def site_settings(request):
#     university_link = request.path.split('/')[-1]
#     # print("University Link:", university_link)
#     print("Request Path:", request.path)

#     return  {'site_name': university_link, 'site_creation_date': '12/12/12'}
