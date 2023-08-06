from aclib import web

r = web.get('http://www.baidu.com')
print(r)
print(r.content)

print(web.getwebtime())

# cookie = 'sensorsdata2015jssdkchannel=%7B%22prop%22%3A%7B%22_sa_channel_landing_url%22%3A%22%22%7D%7D; oschina_new_user=false; remote_way=http; yp_riddler_id=60160549-a30f-401b-aec7-5afc3a1350fe; user_locale=zh-CN; Hm_lvt_70121d39e19f0c5f075ca3160555557f=1669082399; slide_id=9; remember_user_token=BAhbCFsGaQMyy3VJIiIkMmEkMTAkVGc1VnZiUUUzbUp2Ym1Ec25ldC4zTwY6BkVUSSIWMTY4NjM4Njk3MC41NzAwMDUGOwBG--d60512b84901c7461d44a8b3be40183f1675cc2c; gitee_user=true; Hm_lvt_24f17767262929947cc3631f99bfd274=1685001401,1686374054,1686463223,1686607025; tz=Asia%2FShanghai; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%227719730%22%2C%22first_id%22%3A%22188a3b9f7ad87-0ad6f75c7f43368-7e56547b-2073600-188a3b9f7aed7e%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E5%BC%95%E8%8D%90%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22http%3A%2F%2Flocalhost%2F%22%2C%22%24latest_utm_source%22%3A%22alading%22%2C%22%24latest_utm_campaign%22%3A%22repo%22%7D%2C%22%24device_id%22%3A%221756cff369051b-0f9afb90e442e-7e647c6c-2073600-1756cff3691618%22%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTg2NGMxYzI4YTZiMzgtMGJmZjJjYmQxMTU4ZmM4LTc0NTI1NDc2LTIwNzM2MDAtMTg2NGMxYzI4YTdjMjgiLCIkaWRlbnRpdHlfbG9naW5faWQiOiI3NzE5NzMwIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%227719730%22%7D%7D; visit-gitee--2023-05-29=1; csrf_token=sWuUkAJE4XuWopqjDZ2YlC3112d%2F2J4o5dpdl1ZEbSt8HJcbdXut%2F4x0uLhrS%2BZhoijYz9xy72rHakbAkz8GdA%3D%3D; Hm_lpvt_24f17767262929947cc3631f99bfd274=1686703224; gitee-session-n=eTA0WmxnUHJTRnlpYVhhbDAxWGNNdDRpNDkyNWMvVFlwMXpLTTFOWU9scUNxQjMrQXZiUnhsUzh6bEZsaUowSWM4elZWNnpzeDlCQVZYWWxkWHpLMGdNR2xwcHUvQXJXRUVGVHN1aXhlT0kxSG9LWjZIbEd4OHpsZnRldDVVUDNGTGRqajY2OTM2NzR2dTdtcDRLS1ljaDY4bCtoK0l1cVo1NUhlQThWcXYvSzhocmZ1Ymt0TDUrSEpTU2Zvb0VTVzBIKzYyWmlkVGRpQlcvOERYN1ZiSGRxM0pGdUNkeTBEams3dTEyQmM3VjgxSWNZaFUxbkt3enBzd09CSGJPUURJcXVPVWE3dkNQeWgyb2lMaGJNdmQ1cWsxTUpCc3p0WWFPaVVRMTJJV3E4ODhPTzlscFlqYXJscEdvWWN0WnFTT2pLaHA4TFJ2YllTNkREVThNODBteXUva3dUd1BzQnJKbmMvSWNJcUtvPS0tRkJHRFZTMXVpV3RaMlU4TjdOakwwQT09--589b8e3739c332275c1ee1afb498bcf9afbdb992'
# token = 'kc0IsJ9mYu8Jwqv5cHwyEKgq/etl5c0IBtYvYC54Cmxcugs76FkuaxMUieIWqkzlJ/fyQ8ZPvEokZjQ36wNhMw=='
# page = web.GiteePages(
#     'https://gitee.com/anschaser/acnav',
#     'main', 'dist', cookie, token, 'tests/updatetime'
# )
# print(page.updatetime)
# print(page.updatecd)

# res = page.update()
# print(res)
