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
with open("./contracts/Diamond.json") as f:
    abi = json.loads(f.read())

art_token = web3.eth.contract(address=config["address_token"], abi=abi["abi"])

with open("./contracts/AuctionBox.json") as f:
    abi = json.loads(f.read())


def landing(request):

    tokens_in_system = art_token.functions.totalSupply().call()

    tokenIds = art_token.functions.getTokenIds().call()
    tokensInSystem = len(tokenIds)

    infoAboutTokens = []
    for index in tokenIds:
        infoAboutTokens.append([index]+art_token.functions.getArtToken(index).call())

    links_for_tokens = [art_token.functions.tokenURI(index).call() for index in tokenIds]
    print(links_for_tokens)
    for i in range(len(infoAboutTokens)):
        part = infoAboutTokens[i]
        part.append('https://ipfs.io/ipfs/'+ links_for_tokens[i])

    code_names = ['ID', 'Entity', 'Name', 'Author', 'Year', 'Extra', 'Link']

    info_to_render = []
    for info in infoAboutTokens:
        info_to_render.append(dict(zip(code_names, info)))

    style = 'color:#fff; background-color:#277cfd'
    return render(request, 'artproject_owner/index.html', locals())
