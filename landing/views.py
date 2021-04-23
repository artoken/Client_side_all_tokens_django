from django.shortcuts import render
import requests
from web3 import Web3
import json
from .forms import *
import datetime 

url = "https://data-seed-prebsc-1-s1.binance.org:8545"
web3 = Web3(Web3.HTTPProvider(url))
connect = web3.isConnected()
with open('C:/Users/Administrator/Desktop/NFT_kovan/client_auctions_deploy/client/src/contracts/ART_CONTRACT.json') as f:
    abi = json.loads(f.read())

address_token = '0x28A27786C12D801d1E70c92ab26392aDB9b85937'
art_token = web3.eth.contract(address=address_token, abi=abi["abi"])

with open('C:/Users/Administrator/Desktop/NFT_kovan/client_auctions_deploy/client/src/contracts/AuctionBox.json') as f:
    abi = json.loads(f.read())

address_box = '0xf11bB3DcE3FF244AD22969cDC03060Ac43D4600a'
auction_box = web3.eth.contract(address=address_box, abi=abi["abi"])

account_owner = "0xf0DCad9BE520765ecc6eeb0d565DED94Da7305A6"



def landing(request):    
    tokens_in_system = art_token.functions.totalSupply().call()
    share_ids_in_system = [art_token.functions.ids_external(i).call() for i in range(tokens_in_system)]
    share_ids_in_system = list(set(share_ids_in_system))

    token_ids = [art_token.functions.share_to_token(i).call() for i in share_ids_in_system]
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
        info_about_tokens.append(art_token.functions.get_art_by_share_id(a_dictionary[str(i)]).call())

    links_for_tokens = [art_token.functions.get_link_by_token_id(int(i)).call() for i in token_ids_in_system]

    for i in range(len(info_about_tokens)):
        part = info_about_tokens[i]
        part.append('https://ipfs.io/ipfs/'+ links_for_tokens[i])

    code_names = ['ID', 'Owner','Entity', 'Name', 'Author', 'License', 'Year', 'Orig', 'Extra', 'Link']

    info_to_render = []
    for info in info_about_tokens:
        info_to_render.append(dict(zip(code_names, info)))

    style = 'color:#fff; background-color:#277cfd'
    return render(request, 'artproject_owner/index.html', locals())

