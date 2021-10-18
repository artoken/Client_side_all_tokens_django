from django.shortcuts import render
import requests
from web3 import Web3
import json
from .forms import *
import datetime

ganache_url = "http://ganache_artoken:8545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

with open("config.json", "r") as read_file:
    config = json.load(read_file)

connect = web3.isConnected()
with open("./contracts/ART_CONTRACT.json") as f:
    abi = json.loads(f.read())

art_token = web3.eth.contract(address=config["address_token"], abi=abi["abi"])

with open("./contracts/AuctionBox.json") as f:
    abi = json.loads(f.read())


def landing(request):
    tokens_in_system = art_token.functions.totalSupply().call()
    share_ids_in_system = [
        art_token.functions.ids_external(i).call() for i in range(tokens_in_system)
    ]
    share_ids_in_system = list(set(share_ids_in_system))

    token_ids = [
        art_token.functions.share_to_token(i).call() for i in share_ids_in_system
    ]
    token_ids = list(set(token_ids))
    a = [art_token.functions.get_art_by_share_id(i).call() for i in share_ids_in_system]

    token_ids_in_system = [int(part[0]) for part in a]

    keys_list = [str(part) for part in token_ids_in_system]
    values_list = share_ids_in_system
    zip_iterator = zip(keys_list, values_list)
    a_dictionary = dict(zip_iterator)

    token_ids_in_system = list(set(token_ids_in_system))
    tokens_in_system = len(token_ids_in_system)

    info_about_tokens = []
    for i in token_ids_in_system:
        info_about_tokens.append(
            art_token.functions.get_art_by_share_id(a_dictionary[str(i)]).call()
        )

    links_for_tokens = [
        art_token.functions.get_link_by_token_id(int(i)).call()
        for i in token_ids_in_system
    ]

    for i in range(len(info_about_tokens)):
        part = info_about_tokens[i]
        part.append("https://ipfs.io/ipfs/" + links_for_tokens[i])
    code_names = [
        "ID",
        "Owner",
        "Entity",
        "Name",
        "Author",
        "License",
        "Year",
        "Orig",
        "Extra",
        "Link",
    ]

    info_to_render = []
    for info in info_about_tokens:
        info_to_render.append(dict(zip(code_names, info)))

    style = "color:#fff; background-color:#B22222"
    return render(request, "artproject_owner/index.html", locals())
