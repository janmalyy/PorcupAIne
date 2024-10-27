""" This file is for getting the project descriptions and 
public interests from xml and save them to a csv file. """

import time
import re
from settings import DATA_DIR

import requests
from bs4 import BeautifulSoup
import pandas as pd

DELAY = 1


def extract_project_description_and_public_interest(url_df: list[str]):
    """Extract project description and public interest from the PARO xml"""

    list_of_project_ids = []
    list_of_project_descriptions = []
    list_of_public_interest = []

    # loop through the urls in the csv
    for url in url_df:
        #get project_id from url and save to the list
        project_id = url.split("id=", 1)[1]
        list_of_project_ids.append(project_id)

        # get the url content
        url = requests.get(url, timeout=5)
        soup = BeautifulSoup(url.content, "html.parser")

        # extract the project description from xml and save to the list
        project_description = soup.find("div", class_="project-description").text
        #remove the titles "Hlasovací video" and "Realizační video" from the description
        project_description = re.sub(
            "(Hlasovací|Realizační) video", "", project_description
        )
        #remove leading and trailing whitespaces
        project_description = project_description.strip()
        list_of_project_descriptions.append(project_description)

        # extract the public interest from xml and save to the list
        project_public_interest = soup.find(
            "div", class_="col-xs-12 col-sm-offset-2 col-sm-8"
        )
        project_public_interest = project_public_interest.find("p")
        project_public_interest = project_public_interest.find("i").text
        # remove leading and trailing whitespaces
        project_public_interest = project_public_interest.strip()
        list_of_public_interest.append(project_public_interest)

        time.sleep(DELAY)

    return list_of_project_ids, list_of_project_descriptions, list_of_public_interest


def save_to_csv(
    list_of_project_ids,
    list_of_project_descriptions,
    list_of_public_interest,
    output_file,
):
    """Function to save the lists to a csv file."""
    # convert lists to dataframe
    output_df = pd.DataFrame(
        {
            "project_id": list_of_project_ids,
            "project_description": list_of_project_descriptions,
            "public_interest": list_of_public_interest,
        }
    )

    # save the dataframe to a csv file
    output_df.to_csv(output_file, sep=",", encoding="utf-8")


if __name__ == "__main__":
    # convert csv to df
    df = pd.read_csv(DATA_DIR / "ProjektyPARO_5358953113614861487.csv")

    # extract the url list
    url_list = df["properties.detail"]

    # call the extract function
    id_description_interest = extract_project_description_and_public_interest(url_list)

    save_to_csv(
        id_description_interest[0],
        id_description_interest[1],
        id_description_interest[2],
        "descriptions_and_interests.csv",
    )
