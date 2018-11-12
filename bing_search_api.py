# it has code to devolpe the bing_search api in python using the microsoft azure account in this i just created for box manufacturer heidelberg
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

# -*- coding: utf-8 -*-

import http.client, urllib.parse, json
import pandas as pd

# **********************************************
# *** Update or verify the following values. ***
# **********************************************

# Replace the subscriptionKey string value with your valid subscription key.
subscriptionKey = "655c468ee39e4e2ba3314956af875cba"

# Verify the endpoint URI.  At this writing, only one endpoint is used for Bing
# search APIs.  In the future, regional endpoints may be available.  If you
# encounter unexpected authorization errors, double-check this value against
# the endpoint for your Bing Web search instance in your Azure dashboard.
host = "api.cognitive.microsoft.com"
path = "/bing/v7.0/search"

term = "box manufacturer Heidelberg"


def BingWebSearch(search):
    "Performs a Bing Web search and returns the results."

    headers = {"Ocp-Apim-Subscription-Key": subscriptionKey}
    conn = http.client.HTTPSConnection(host)
    query = urllib.parse.quote(search)
    conn.request("GET", path + "?q=" + query, headers=headers)
    response = conn.getresponse()
    headers = [
        k + ": " + v
        for (k, v) in response.getheaders()
        if k.startswith("BingAPIs-") or k.startswith("X-MSEdge-")
    ]
    return headers, response.read().decode("utf8")


if len(subscriptionKey) == 32:

    print("Searching the Web for: ", term)

    headers, result = BingWebSearch(term)
    print("\nRelevant HTTP Headers:\n")
    print("\n".join(headers))
    print("\nJSON Response:\n")
    with open("output.json", "w") as f:
        f.write(json.dumps(json.loads(result), indent=4))

    data = json.loads(result)
    final_data = [
        {
            "name": i["name"],
            "url": i["url"],
            "desc": i.get("snippet", i.get("description")),
        }
        for i in data["webPages"]["value"]
    ]

    df = pd.DataFrame(final_data, columns=["name", "desc", "url"])
    print(df.head())
    df.to_csv("output.csv", index=False)
else:

    print("Invalid Bing Search API subscription key!")
    print("Please paste yours into the source code.")

