""" This file is for getting the assesment of feasibility
from xml and saving them to a csv file. """

import requests
from bs4 import BeautifulSoup
import pandas as pd

DEFAULT_TIMEOUT = 5

def extract_assesment_of_feasibility(url_df: list[str]):
    """Function to extract assesment of feasibility from the xml."""

    # initialize lists
    list_of_lists = []

    # loop through the urls in the csv
    for url in url_df:
        # get project_id from url and save to the list
        project_id = url.split("id=", 1)[1]
        assesment_list = [project_id]

        # get the url content
        url = requests.get(url, DEFAULT_TIMEOUT)
        soup = BeautifulSoup(url.content, "html.parser")

        # extract the assement from xml and save to the list

        if soup.find("div", {"id": "project-block-reaction"}):
            assesment_xml = soup.find("div", {"id": "project-block-reaction"})
            assesment_xml = assesment_xml.find("tbody")
            assesment_xml = assesment_xml.find_all("td")
            # count to check what part of the assesment we are in currently,
            # it's not specified in xml
            count = 0
            # there can be multiple assesments for one project
            for td in assesment_xml:
                if len(td.text) > 0:
                    assesment_list.append(td.text)
                # sometimes "Odůvodnění" part of assesment is missing
                # so we need to add "EMPTY" to list
                else:
                    assesment_list.append("EMPTY")

                count += 1
                if count == 3:
                    list_of_lists.append(assesment_list)
                    assesment_list = [project_id]
                    count = 0
        # if the assesment is missing, save "missing assesment of feasibility"
        else:
            assesment_list.extend(["missing assesment of feasibility"] * 3)
            list_of_lists.append(assesment_list)

    return list_of_lists


def save_to_csv(list_of_lists, output_path):
    """Function to save the assesments to a csv file."""
    # convert lists to dataframe
    output_df = pd.DataFrame(
        list_of_lists, columns=["ID", "Subject", "Reasoning", "Conclusion"]
    )

    # save the dataframe to a csv file
    output_df.to_csv(output_path, sep=",", encoding="utf-8")

if __name__ == '__main__':
    # convert csv to df
    df = pd.read_csv("data/ProjektyPARO_5358953113614861487.csv")

    # extract the url list
    url_list = df["properties.detail"]

    save_to_csv(extract_assesment_of_feasibility(url_list), "data/assesment_of_feasibility.csv")
