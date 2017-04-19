import os
import json
import requests
from urllib.parse import urlencode

CLIENT_NAME='my-mstdn-app'
SCOPE = "read write follow"
STORE_FILE_NAME = "client_id.json"

def get_client_id():
    """
    認証済みアプリのためのclient_id, client_secretの発行
    :return: (client_id, client_secret)
    """

    # すでに作成ずみで保存してあればそれを利用
    if os.path.exists(STORE_FILE_NAME):
        with open(STORE_FILE_NAME) as f:
            store = json.load(f)
            return store["client_id"], store["client_secret"]

    # 未作成であれば新規に発行
    res = requests.post('https://mstdn.jp/api/v1/apps',
                        dict(client_name=CLIENT_NAME,
                             redirect_uris="urn:ietf:wg:oauth:2.0:oob",
                             scopes="read write follow")).json()

    # ファイルに保存
    with open(STORE_FILE_NAME, "w") as f:
        json.dump(res, f)

    return res["client_id"], res["client_secret"]

def get_authorize_url(client_id):
    """
    認証済みアプリに権限を与えるための承認ページのURLを作成する
    :return: url
    """
    params = urlencode(dict(
        client_id=client_id,
        response_type="code",
        redirect_uri="urn:ietf:wg:oauth:2.0:oob",   # ブラウザ上にcode表示
        scope=SCOPE
    ))
    return 'https://mstdn.jp/oauth/authorize?'+params

def get_access_token(client_id, client_secret, code):
    """
    client_idと認証コードを利用してアクセストークンを取得する
    :param client_id:
    :param client_secret:
    :param code: ブラウザに表示された認証コード
    :return: access_token
    """
    res = requests.post('https://mstdn.jp/oauth/token', dict(
        grant_type="authorization_code",
        redirect_uri="urn:ietf:wg:oauth:2.0:oob",
        client_id=client_id,
        client_secret=client_secret,
        code=code
    )).json()

    return res["access_token"]

def main():
    # client_idの取得
    client_id, client_secret = get_client_id()

    print("client id:    ", client_id)
    print("client secret:", client_secret)

    # 承認ページURLの取得
    url = get_authorize_url(client_id)


    # ブラウザでurlを開いてもらって認証コードの取得と入力
    print("open browser ", url)
    code = input("input code > ")

    # アクセストークンの取得
    accress_token = get_access_token(client_id, client_secret, code)

    print("access token :", accress_token)


if __name__ == "__main__":
    main()
