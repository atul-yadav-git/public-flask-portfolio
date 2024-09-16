#this logic is to help search functionality to get keyworsd from projects and blogs for prepoulated data

# utils.py
# This module contains utility functions for the Flask web portfolio app.
# Specifically, it includes logic to extract and aggregate unique keywords from the Post and Project models.
# These keywords are used for search functionality and pre-populating search fields.

###########################################################################

'''
Purpose: To aggregate and return all unique keywords used in blog posts and projects for search functionality and pre-populated search fields.

How It Works:
Queries each keyword column (from keyword1 to keyword10) in both Post and Project models.
Collects and aggregates distinct keywords into a set to ensure uniqueness.
Returns the sorted list of unique keywords.

Where It's Used: This function is used in search-related features of the app to provide a comprehensive list of keywords for user interaction, such as search suggestions or filtering options.
'''

################################################################################
from app import db
from models import Post, Project

###########################################################################
def get_all_keywords():

    """
    Retrieve all unique keywords from the Post and Project models.

    This function aggregates keywords from both the Post and Project models by querying each keyword column
    (keyword1 to keyword10) for distinct values. The collected keywords are then returned as a sorted list.

    Process:
        1. Initialize an empty set to hold unique keywords.
        2. For each keyword column (keyword1 to keyword10) in the Post model:
            - Query distinct values from the database.
            - Add non-null keywords to the set.
        3. Repeat the above process for the Project model.
        4. Convert the set of keywords to a sorted list and return it.

    Returns:
        list: A sorted list of unique keywords aggregated from both Post and Project models.
    """

    keywords = set()
    
    # Fetch and aggregate keywords from the Post model
    for i in range(1, 11):
        column_name = f'keyword{i}'
        result = db.session.query(getattr(Post, column_name)).distinct().all()
        # Update the set with non-null keywords
        keywords.update([keyword[0] for keyword in result if keyword[0]])

    # Fetch and aggregate keywords from the Project model
    for i in range(1, 11):
        column_name = f'keyword{i}'
        result = db.session.query(getattr(Project, column_name)).distinct().all()
        # Update the set with non-null keywords
        keywords.update([keyword[0] for keyword in result if keyword[0]])

    # Return the sorted list of unique keywords
    return sorted(keywords)

